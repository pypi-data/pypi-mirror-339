import os
import argparse
import torch
import torch.nn as nn
import json
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Union, Optional
import requests
from torch.nn import Sequential as Seq, Linear as Lin, ReLU
from torch_geometric.utils import scatter
from torch_geometric.nn import MetaLayer
from torch_geometric.loader import DataLoader
from torch_geometric.data import Data
from graph_games_proto import *
from pyrsistent import PClass, field
from pyrsistent import v, pvector, PVector
from multipledispatch import dispatch

MAX_SCORE = 1023
MIN_SCORE = -1024

class BoardNode(PClass):
    num = field(type=int)
    point_num = field(type=(int, type(None)), initial=None)  # Optional[int]
    point_uuid = field(type=str)
    path_num = field(type=(int, type(None)), initial=None)  # Optional[int]
    path_segment_num_a = field(type=(int, type(None)), initial=None)  # Optional[int]
    path_segment_num_b = field(type=(int, type(None)), initial=None)  # Optional[int]


class BoardEdge(PClass):
    num = field(type=int)
    src = field(type=int)
    dst = field(type=int)
    path_num = field(type=int)
    path_segment_num = field(type=int)
    segment_num = field(type=int)


class BoardGraph(PClass):
    nodes = field(type=list)  # List[BoardNode]
    edges = field(type=list)  # List[BoardEdge]
    adj = field(type=object)


def run_gql(url, api_key, gql, variables):
    headers = {"Authorization": api_key}
    payload = {"query": gql, "variables": variables}
    return requests.post(url, headers=headers, json=payload).json()


@dataclass(frozen=True)
class QModelDomainConfig:
    pointuuid2idx: Dict[str, int]


def getpointfanin(s: QModelDomainConfig) -> int:
    return len(set(s.pointuuid2idx.values()))


def getglobalfanin(s: QModelDomainConfig) -> int:
    return 1


def getnodefanin(s: QModelDomainConfig) -> int:
    return (
        1  # Captured by me
        + 1  # Captured by other
        + 1  # Not captured and available to me
        + 1  # Not captured and not available to me
        + getpointfanin(s)  # 1-hot point index
    )


def getnodefanout(s: QModelDomainConfig) -> int:
    return 1


def getglobalfanout(s: QModelDomainConfig) -> int:
    # 2^11 = -1024(MIN_SCORE) - 1023(MAX_SCORE)
    return 11


def getuuid2idx(uuids):
    return {uuid: i + 1 for i, uuid in enumerate(uuids)}


def getuuid2idx(uuids):
    return {uuid: i + 1 for i, uuid in enumerate(uuids)}


def getqmodeldomainconfig(d):
    return QModelDomainConfig(
        pointuuid2idx=getuuid2idx(d["point_uuids"]),
    )


def getuuid2idxallownothing(args):
    original = getuuid2idx(args)
    return original

    d = dict(original)
    # Assign None the maximum value plus 1
    d[None] = max(original.values()) + 1
    return d


def getgroupeduuid2idxallownothing(args):
    original = getgroupeduuid2idx(args)
    return original
    # Create a new dict with Union[None, str] keys, copying original
    d = dict(original)
    # Assign None the maximum value plus 1
    d[None] = max(original.values()) + 1
    return d


def get_net_version(url, api_key, net_version_uuid):
    query = """query GetNetVersion($uuid: ID!) {
      getNetVersion(uuid: $uuid){
        uuid
        net_uuid
        net {
            feed {
                targeta_uuid
                targetb_uuid
            }
        }
        config {
          context
          architecture
          domain_config_json
        }
        q_model_config{
            point_uuids
        }
      }
    }"""
    variables = {"uuid": net_version_uuid}
    net_version = run_gql(url, api_key, query, variables)
    return net_version["data"]["getNetVersion"]


def uuid2item(items):
    return {item.uuid: item for item in items}


def get_static_board_config(url, api_key, uuid):
    query = """query GetStaticBoardConfig($uuid: ID!) {
        getStaticBoardConfig(uuid: $uuid){
            uuid
            json
        }
    }"""
    variables = {"uuid": uuid}
    res = run_gql(url, api_key, query, variables)
    return res["data"]["getStaticBoardConfig"]


def get_static_board_configs(url, api_key, uuids):
    query = """query GetStaticBoardConfigs($uuids: [ID]!){
        getStaticBoardConfigs(uuids:$uuids){
            uuid
            json
        }
    }"""
    variables = {"uuids": uuids}
    res = run_gql(url, api_key, query, variables)
    return res["data"]["getStaticBoardConfigs"]


def get_raw_samples(url, api_key, uuids):
    query = """query GetMultipointSamples($uuids: [ID]!){
        getNetSamples(uuids:$uuids){
            uuid
            x_json
            y_json
        }
    }"""
    variables = {"uuids": uuids}
    res = run_gql(url, api_key, query, variables)
    return res["data"]["getNetSamples"]


def get_dataset(url, api_key, dataset_uuid):
    query = """query GetNetSamplesByDataset($uuid: ID!) {
        getNetSamplesByDataset(uuid: $uuid) {
            uuid
            x_json
            y_json
        }
    }"""
    variables = {"uuid": dataset_uuid}
    res = run_gql(url, api_key, query, variables)
    return res["data"]["getNetSamplesByDataset"]


def forceminmax(x, min_se=0, max_se=150):
    """Clamp a value between min_se and max_se."""
    return min(max_se, max(min_se, x))


def encodecomponentfeatures(domain_config, component, augmentation=False):
    """
    Encode features for a component's readings in a multipoint context, version 2 using PyTorch.

    Parameters:
    - domain_config: Object containing configuration data, including UUID-to-index mappings and fan-in values.
    - component: Dictionary with 'readings', a list of reading dictionaries.
    - augmentation: Boolean flag to enable sound energy augmentation (default: False).

    Returns:
    - A PyTorch tensor where each row corresponds to a reading and columns are concatenated feature encodings.
    """
    # Process sound energies with optional augmentation
    soundenergies = []
    for r in component["readings"]:
        if r["se"] is None:
            se = -1
        elif augmentation:
            capped_se = forceminmax(r["se"])
            se_min = forceminmax(capped_se * 0.95)
            se_max = forceminmax(capped_se * 1.05)
            # PyTorch triangular distribution (left, mode, right)
            se = torch.distributions.Triangular(
                torch.tensor(se_min), torch.tensor(capped_se), torch.tensor(se_max)
            ).sample()
        else:
            se = forceminmax(r["se"])
        soundenergies.append(int(round(se.item() if torch.is_tensor(se) else se)) + 1)

    # Extract evaluation levels
    eval_levels = [r["evalLevel"] for r in component["readings"]]

    # Encode measurement indices, using None for missing UUIDs
    encoded_measurement_idxs = [
        domain_config.measurementuuid2idx.get(r["measurementUuid"], None)
        for r in component["readings"]
    ]

    # Encode signatures as lists of indices
    encoded_reading_signatures = [
        [
            domain_config.signatureuuid2idx[x]
            for x in reading["signatureUuids"]
            if x in domain_config.signatureuuid2idx
        ]
        for reading in component["readings"]
    ]

    # Encode actions as lists of indices
    encoded_reading_actions = [
        [
            domain_config.actionuuid2idx[x]
            for x in reading["actionUuids"]
            if x in domain_config.actionuuid2idx
        ]
        for reading in component["readings"]
    ]

    # Get fan-in values from domain_config (assuming they are attributes; adjust if they are methods)

    # Convert lists to PyTorch tensors
    soundenergies = torch.tensor(soundenergies, dtype=torch.long)
    eval_levels = (
        torch.tensor(eval_levels, dtype=torch.long) - 1
    )  # Shift to 0-based indexing

    # One-hot encode sound energies (0 to se_fanin-1)
    soundenergies_onehot = torch.nn.functional.one_hot(
        soundenergies, num_classes=se_fanin
    ).float()

    # One-hot encode evaluation levels (1 to eval_fanin, already shifted)
    eval_levels_onehot = torch.nn.functional.one_hot(
        eval_levels, num_classes=eval_fanin
    ).float()

    # One-hot encode measurement indices, with zeros for None
    measurement_onehot = torch.zeros(len(encoded_measurement_idxs), measurement_fanin)
    for i, idx in enumerate(encoded_measurement_idxs):
        if idx is not None:
            measurement_onehot[i, idx - 1] = 1  # Indices are 1-based

    # Multi-hot encode signatures and actions
    def multihotbatch(lists, num_classes):
        """Convert lists of indices into a multi-hot encoded tensor."""
        matrix = torch.zeros(len(lists), num_classes)
        for i, idxs in enumerate(lists):
            for idx in idxs:
                matrix[i, idx - 1] = 1  # Indices are 1-based
        return matrix

    signatures_multihot = multihotbatch(encoded_reading_signatures, signature_fanin)
    actions_multihot = multihotbatch(encoded_reading_actions, action_fanin)

    # Concatenate all feature tensors horizontally
    features = torch.cat(
        [
            soundenergies_onehot,
            eval_levels_onehot,
            measurement_onehot,
            signatures_multihot,
            actions_multihot,
        ],
        dim=1,
    )

    return features


def gensampleinput(config, sample, augmentation=False):

    domain_config = config["domain_config"]

    # Encode reading features for the first node
    reading_features = encodecomponentfeatures(
        domain_config, sample["x"]["nodes"][0], augmentation=augmentation
    )

    # Determine number of components from reading features
    n = reading_features.shape[1]

    # Create adjacency matrices
    # Fully connected graph for readings
    reading_adj_mat = torch.ones((n, n), dtype=torch.float32)
    # 1x1 adjacency matrix for component (hard-coded for 1-component equipment)
    component_adj_mat = torch.ones((1, 1), dtype=torch.float32)

    # Get model number character to vocabulary index mapping
    modelnumchar2vocabidx = getmodelnumchar2vocabidx()

    # Convert model number to vocabulary indices
    model_num_idxs = getvocabidxs(
        getnummodelmaxchars(),
        sample["x"]["nodes"][0]["modelNum"],
        modelnumchar2vocabidx,
    )
    model_num_idxs = torch.tensor(model_num_idxs, dtype=torch.long)

    # Retrieve system and make indices from domain configuration
    system_idx = domain_config.systemuuid2idx.get(
        sample["x"]["nodes"][0]["systemUuid"], None
    )
    make_idx = domain_config.makeuuid2idx.get(sample["x"]["nodes"][0]["makeUuid"], None)

    # Get fan-in sizes for systems and makes
    system_fanin = getsystemfanin(domain_config)
    make_fanin = getmakefanin(domain_config)

    # Create one-hot encodings for system_idx
    system_onehot = torch.zeros(system_fanin)
    if system_idx is not None:
        system_onehot[system_idx - 1] = 1  # Adjust for 0-based indexing
    else:
        system_onehot[-1] = 1  # Set last element for default case

    # Create one-hot encodings for make_idx
    make_onehot = torch.zeros(make_fanin)
    if make_idx is not None:
        make_onehot[make_idx - 1] = 1
    else:
        make_onehot[-1] = 1

    # Concatenate one-hot encodings and reshape to column vector
    component_x = torch.concatenate([system_onehot, make_onehot])
    component_x = torch.tensor(component_x, dtype=torch.float32).unsqueeze(1)

    # Return processed data as a dictionary
    return {
        "reading_adj_mat": reading_adj_mat,
        "component_adj_mat": component_adj_mat,
        "model_num_idxs": model_num_idxs,
        "component_x": component_x.t(),
        "reading_features": reading_features,
    }


def gensampletarget(config, sample):
    domain_config = config["domain_config"]

    actionUuids = sample["y"]["nodes"][0]["actionUuids"]
    tagUuids = sample["y"]["nodes"][0]["tagUuids"]
    evalLevel = sample["y"]["nodes"][0]["evalLevel"]

    # Filter and map actionUuids to indices
    # In Julia: filter then map; in Python: list comprehension
    action_idxs = [
        domain_config.figactionuuid2idx[x]
        for x in actionUuids
        if x in domain_config.figactionuuid2idx
    ]

    # Filter and map tagUuids to indices
    tag_idxs = [
        domain_config.figtaguuid2idx[x]
        for x in tagUuids
        if x in domain_config.figtaguuid2idx
    ]

    # One-hot encoding for evalLevel
    eval_range = getevaloutrange(domain_config)  # List of possible eval levels
    eval_index = eval_range.index(evalLevel)  # Find 0-based index
    onehot_vec = torch.nn.functional.one_hot(
        torch.tensor(eval_index), num_classes=len(eval_range)
    ).float()  # Convert to float32 as in Julia

    # Multi-hot encoding for tags
    n_tags = len(domain_config.figtaguuid2idx)
    multihot_tag = torch.zeros(n_tags, dtype=torch.float32)
    tag_indices = torch.tensor(
        [i - 1 for i in tag_idxs],  # Convert 1-based to 0-based indices
        dtype=torch.long,
    )
    multihot_tag[tag_indices] = 1  # Set positions to 1

    # Multi-hot encoding for actions
    n_actions = len(domain_config.figactionuuid2idx)
    multihot_action = torch.zeros(n_actions, dtype=torch.float32)
    action_indices = torch.tensor(
        [i - 1 for i in action_idxs],  # Convert 1-based to 0-based indices
        dtype=torch.long,
    )
    multihot_action[action_indices] = 1  # Set positions to 1

    # Concatenate all vectors and reshape to column vector (n, 1)
    nf = torch.cat([onehot_vec, multihot_tag, multihot_action], dim=0).unsqueeze(1)

    # Create ef as a 1x1 tensor (kept despite TODO note in Julia code)
    ef = torch.ones(1, 1, dtype=torch.float32)

    # Return as a dictionary (Python equivalent of Julia's named tuple)
    return {"nf": nf.t(), "ef": ef.t()}


def create_edge_index_from_adj_mat(adj_mat):
    """
    Create edge index from adjacency matrix.
    """
    sources, targets = adj_mat.nonzero(as_tuple=True)
    edge_index = torch.stack([sources, targets], dim=0)
    return edge_index


def create_edge_index_with_self_loops(n):
    sources = [i for i in range(n) for _ in range(n)]
    targets = [j for j in range(n) for j in range(n)]
    edge_index = torch.tensor([sources, targets], dtype=torch.int64)
    return edge_index


@dispatch(StaticBoardConfig, PlayerState, AltAction, str, object)
def gensample(static_board_config, player_state, action, net_sample_uuid, y_json):
    board_config = static_board_config.board_config
    imagined_state = get_imagined_state(static_board_config, player_state)
    imagined_next_state = getnextstate(imagined_state, action)
    imagined_player_state = getplayerstate(imagined_next_state, action.player_idx)
    next_public_state = imagined_player_state.public
    next_private_state = imagined_player_state.private
    my_hand = next_private_state.hand
    my_points = my_hand.points
    my_legal_actions = next_private_state.legal_actions

    def is_captured_by_me(point):
        return point.uuid in my_points

    def is_captured(point):
        return point.uuid in next_public_state.captured_points

    def is_available_to_me(point):
        for legal_action in my_legal_actions:
            if point.uuid in legal_action.points:
                return True
        return False

    def get_status_feature(point):
        # "captured_by_me
        # "captured_by_other
        # "available_to_me
        # "not_available_to_me
        status = torch.zeros(4, dtype=torch.float32)
        if is_captured_by_me(point):
            status[0] = 1
        elif is_captured(point):
            status[1] = 1
        elif is_available_to_me(point):
            status[2] = 1
        else:
            status[3] = 1
        return status

    status_features_vec = [get_status_feature(point) for point in board_config.points]
    # vertically concat, result is (num_points, 4)
    status_features = torch.stack(status_features_vec, dim=0)

    num_points = len(board_config.points)
    input_labels = torch.tensor(range(0, num_points))
    position_enc = torch.nn.functional.one_hot(
        input_labels,
        num_classes=num_points,
    ).float()

    # vertically concat status_features with position_enc
    x_features = torch.cat([position_enc, status_features], dim=1)
    
    board_graph = get_board_graph(board_config)
    edge_index = create_edge_index_from_adj_mat(board_graph.adj)
    num_edges = len(board_graph.edges)

    if y_json is not None:
        adjusted_global_y_binary = qvalue2multihot(int(y_json))
        y_global = adjusted_global_y_binary.unsqueeze(0)
    else:
        y_global = None

    return Data(
        x=x_features,
        y_global=y_global,
        edge_index=edge_index,
        edge_attr=torch.ones(num_edges,1),
        x_global=torch.ones(1).unsqueeze(0),
        net_sample_uuid=net_sample_uuid,
    )


@dispatch(StaticBoardConfig, str, str, object)
def gensample(static_board_config, net_sample_uuid, x_json, y_json):
    x = json.loads(x_json)
    action = AltAction.__fromdict__(x["action"])
    player_state_dict = json.loads(x["serialized_player_state"])
    player_state = PlayerState.__fromdict__(player_state_dict)
    return gensample(static_board_config, player_state, action, net_sample_uuid, y_json)


@dispatch(dict, dict)
def gensample(static_board_config_map, sample_raw):
    x = json.loads(sample_raw["x_json"])
    net_sample_uuid = sample_raw["uuid"]
    x_json = sample_raw["x_json"]
    y_json = sample_raw["y_json"]
    static_board_config = static_board_config_map[x["static_board_config_uuid"]]
    return gensample(static_board_config, net_sample_uuid, x_json, y_json)


def qvalue2multihot(q_value):
    assert MIN_SCORE <= q_value <= MAX_SCORE, "q_value out of range"
    global_y_decimal = q_value
    adjusted_global_decimal = global_y_decimal + 1024  # Adjust to range [0, 2047]
    # Convert to binary and pad with zeros to 11 bits
    adjusted_global_y_binary = torch.tensor(
        [int(bit) for bit in format(adjusted_global_decimal, "011b")], dtype=torch.float32
    )
    return adjusted_global_y_binary


def multihot2qvalue(binary_arr):
    # Convert binary array to decimal
    binary_str = ''.join([str(int(bit)) for bit in binary_arr.tolist()])
    adjusted_global_decimal = int(binary_str, 2)
    # Adjust back to original range [-1024, 1023]
    global_y_decimal = adjusted_global_decimal - 1024
    return global_y_decimal
    


class EdgeModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.edge_mlp = Seq(Lin(2 * 13 + 4 + 1, 32), ReLU(), Lin(32, 32))

    def forward(self, src, dst, edge_attr, u, batch):
        out = torch.cat([src, dst, edge_attr, u[batch]], 1)
        return self.edge_mlp(out)


class NodeModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.node_mlp_1 = Seq(Lin(32 + 13, 32), ReLU(), Lin(32, 32))
        self.node_mlp_2 = Seq(Lin(32 + 13 + 1, 64), ReLU(), Lin(64, 64))

    def forward(self, x, edge_index, edge_attr, u, batch):
        row, col = edge_index
        out = torch.cat([x[row], edge_attr], dim=1)
        out = self.node_mlp_1(out)
        out = scatter(out, col, dim=0, dim_size=x.size(0), reduce="mean")
        out = torch.cat([x, out, u[batch]], dim=1)
        return self.node_mlp_2(out)


class GlobalModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.global_mlp = Seq(Lin(1 + 64, 512), ReLU(), Lin(512, 300))

    def forward(self, x, edge_index, edge_attr, u, batch):
        out = torch.cat(
            [
                u,
                scatter(x, batch, dim=0, reduce="mean"),
            ],
            dim=1,
        )
        return self.global_mlp(out)


class EdgeModel(torch.nn.Module):
    def __init__(
        self,
        node_fan_in,
        node_fan_out,
        edge_fan_in,
        edge_fan_out,
        global_fan_in,
        global_fan_out,
    ):
        super().__init__()
        self.edge_mlp = Seq(
            Lin(2 * node_fan_in + edge_fan_in + global_fan_in, 32), ReLU(), Lin(32, 32)
        )

    def forward(self, src, dst, edge_attr, u, batch):
        out = torch.cat([src, dst, edge_attr, u[batch]], 1)
        return self.edge_mlp(out)


class NodeModel(torch.nn.Module):
    def __init__(
        self,
        node_fan_in,
        node_fan_out,
        edge_fan_in,
        edge_fan_out,
        global_fan_in,
        global_fan_out,
    ):
        super().__init__()
        self.node_mlp_1 = Seq(Lin(32 + node_fan_in, 32), ReLU(), Lin(32, 32))
        self.node_mlp_2 = Seq(
            Lin(32 + node_fan_in + global_fan_in, 64), ReLU(), Lin(64, node_fan_out)
        )

    def forward(self, x, edge_index, edge_attr, u, batch):
        row, col = edge_index
        out = torch.cat([x[row], edge_attr], dim=1)
        out = self.node_mlp_1(out)
        out = scatter(out, col, dim=0, dim_size=x.size(0), reduce="mean")
        out = torch.cat([x, out, u[batch]], dim=1)
        return self.node_mlp_2(out)


class GlobalModel(torch.nn.Module):
    def __init__(
        self,
        node_fan_in,
        node_fan_out,
        edge_fan_in,
        edge_fan_out,
        global_fan_in,
        global_fan_out,
    ):
        super().__init__()
        self.global_mlp = Seq(
            Lin(global_fan_in + node_fan_out, 512), ReLU(), Lin(512, global_fan_out)
        )

    def forward(self, x, edge_index, edge_attr, u, batch):
        out = torch.cat(
            [
                u,
                scatter(x, batch, dim=0, reduce="mean"),
            ],
            dim=1,
        )
        return self.global_mlp(out)


def parse_mat(d, mat_name, dims_name):
    return torch.tensor(d[mat_name]).reshape(d[dims_name][::-1]).t()


def parse_real_data(json_item):
    x = parse_mat(json_item, "x", "x_dims")
    y = parse_mat(json_item, "y", "y_dims")
    edge_attr = parse_mat(json_item, "edge_attr", "edge_attr_dims")
    edge_index = parse_mat(json_item, "edge_index", "edge_index_dims")
    x = parse_mat(json_item, "x", "x_dims")
    return Data(x=x, y=y, edge_attr=edge_attr, edge_index=edge_index)


def get_gnn_data(sample):
    return Data(
        x=sample["x"],
        y=sample["y"]["nf"],
        edge_attr=torch.ones(1, 1),
        edge_index=torch.ones(2, 1).int(),
        x_readings_adj_mat=sample["x_readings_adj_mat"],
        x_readings=sample["x_readings"],
    )


def gen_samples_from_uuids(url, api_key, uuids, model_config):
    raw_samples = get_raw_samples(url, api_key, uuids)
    return load_dataset(url, api_key, raw_samples, model_config)


def gen_samples_from_dataset(url, api_key, dataset_uuid, model_config):
    raw_samples = get_dataset(url, api_key, dataset_uuid)
    return load_dataset(url, api_key, raw_samples, model_config)


def load_dataset(url, api_key, raw_samples, model_config):
    all_static_board_config_uuids = [
        json.loads(a["x_json"])["static_board_config_uuid"] for a in raw_samples
    ]
    static_board_config_uuids = list(set(all_static_board_config_uuids))
    static_board_configs_raws = get_static_board_configs(
        url, api_key, static_board_config_uuids
    )
    static_board_configs = [
        StaticBoardConfig(
            uuid=a["uuid"],
            board_config=initboardconfig(json.loads(a["json"])),
        )
        for a in static_board_configs_raws
    ]
    static_board_config_map = uuid2item(static_board_configs)
    return [
        gensample(static_board_config_map, item)
        for item in raw_samples
    ]


def run_update_net_version(url, api_key, net_version_input):
    query = """mutation UpdateNetVersion($input: UpdateNetVersionInput!){
        updateNetVersion(input: $input){
            id
            uuid
            name
            created_at
            updated_at
            trained_at
            queued_at
            net_uuid
            training_failed_at
            training_started_at
            context
            train_checksum
            test_checksum
            source_size
            train_loss
            test_loss
            train_acc
            test_acc
            architecture    
            config_checksum
            is_latest
            is_default
        }
    }"""
    variables = {"input": net_version_input}
    run_gql(url, api_key, query, variables)


def run_net_version_training_started_gql(url, api_key, net_version_uuid):
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    net_version_input = {
        "uuid": net_version_uuid,
        "training_started_at": formatted_time,
    }
    return run_update_net_version(url, api_key, net_version_input)


def run_net_version_training_ended_gql(url, api_key, net_version_uuid):
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    net_version_input = {"uuid": net_version_uuid, "trained_at": formatted_time}
    return run_update_net_version(url, api_key, net_version_input)


def run_alert_training_progress_gql(url, api_key, net_uuid, net_version_uuid, progress):
    percentage = int(progress * 100)
    run_alert_training_msg_gql(
        url, api_key, net_uuid, net_version_uuid, f"Training progress: {percentage}%"
    )


def run_alert_training_msg_gql(url, api_key, net_uuid, net_version_uuid, msg):
    net_version_input = {
        "net_uuid": net_uuid,
        "net_version_uuid": net_version_uuid,
        "msg": msg,
    }
    query = """mutation AlertTrainingMsg($input: TrainingMsgInput!){
        alertTrainingMsg(input: $input){
            net_uuid
            net_version_uuid
            msg
        }
    }"""
    variables = {"input": net_version_input}
    run_gql(url, api_key, query, variables)


def hello():
    node_fan_in = 5
    node_fan_out = 27
    edge_fan_in = 1
    edge_fan_out = 32
    global_fan_in = 1
    global_fan_out = 64
    component_model = MetaLayer(
        EdgeModel(
            node_fan_in,
            node_fan_out,
            edge_fan_in,
            edge_fan_out,
            global_fan_in,
            global_fan_out,
        ),
        NodeModel(
            node_fan_in,
            node_fan_out,
            edge_fan_in,
            edge_fan_out,
            global_fan_in,
            global_fan_out,
        ),
        GlobalModel(
            node_fan_in,
            node_fan_out,
            edge_fan_in,
            edge_fan_out,
            global_fan_in,
            global_fan_out,
        ),
    )
    x = torch.randn(20, node_fan_in)
    edge_attr = torch.randn(40, edge_fan_in)
    u = torch.randn(2, global_fan_in)
    batch = torch.tensor([0] * 10 + [1] * 10)
    edge_index = torch.randint(0, high=10, size=(2, 20), dtype=torch.long)
    edge_index = torch.cat([edge_index, 10 + edge_index], dim=1)
    x_out, edge_attr_out, u_out = component_model(x, edge_index, edge_attr, u, batch)
    assert x_out.size() == (20, node_fan_out)
    assert edge_attr_out.size() == (40, edge_fan_out)
    assert u_out.size() == (2, global_fan_out)
    print(u_out[0].tolist())
    print("hello world7")


# Implement the following Julia function in Python:
# function getboardgraph(board_config::FrozenBoardConfig)
#     (; board_paths, points) = board_config

#     board_nodes = BoardNode[]
#     board_edges = BoardEdge[]

#     for board_point in points
#         (; num, uuid) = board_point
#         push!(board_nodes, BoardNode(num, num, uuid, nothing, nothing, nothing))
#     end

#     node_counter = length(board_nodes) + 1
#     edge_counter = 1
#     segment_counter = 1

#     for frozen_path in board_paths
#         num_path_segments = length(frozen_path.path.segments)
#         for (path_segment_num,segment) in enumerate(frozen_path.path.segments)

#             src = nothing
#             dst = nothing

#             if isone(num_path_segments)
#                 src = frozen_path.start_point_num
#                 dst = frozen_path.end_point_num
#             else
#                 if isone(path_segment_num)
#                     src = frozen_path.start_point_num
#                     dst = node_counter
#                     push!(board_nodes, BoardNode(node_counter, nothing, nothing, frozen_path.num, path_segment_num, path_segment_num+1))
#                     node_counter += 1
#                 elseif path_segment_num == num_path_segments
#                     dst = frozen_path.end_point_num
#                     src = node_counter
#                     push!(board_nodes, BoardNode(node_counter, nothing, nothing, frozen_path.num, path_segment_num-1, path_segment_num))
#                     node_counter += 1
#                 else
#                     src = node_counter
#                     push!(board_nodes, BoardNode(node_counter, nothing, nothing, frozen_path.num, path_segment_num, path_segment_num+1))
#                     node_counter += 1

#                     dst = node_counter
#                     push!(board_nodes, BoardNode(node_counter, nothing, nothing, frozen_path.num, path_segment_num, path_segment_num+1))
#                     node_counter += 1
#                 end
#             end

#             push!(board_edges, BoardEdge(edge_counter, src, dst, frozen_path.num, path_segment_num, segment_counter))
#             push!(board_edges, BoardEdge(edge_counter, dst, src, frozen_path.num, path_segment_num, segment_counter))

#             edge_counter += 2
#             segment_counter += 1

#         end
#     end

#     num_nodes = length(board_nodes)
#     adj_mat = zeros(Int, num_nodes, num_nodes)
#     edge_dict = Dict()
#     for edge in board_edges
#         adj_mat[edge.src, edge.dst] = 1
#         edge_dict[(edge.src, edge.dst)] = edge
#     end

#     edge_coords = [(i, j) for i in 1:size(adj_mat, 1), j in 1:size(adj_mat, 2) if isone(adj_mat[i, j])]
#     ordered_edges = [edge_dict[edge_coord] for edge_coord in edge_coords]


#     BoardGraph(
#         board_nodes,
#         ordered_edges,
#         adj_mat,
#     )
# end
def get_board_graph(board_config):
    board_paths = board_config.board_paths
    points = board_config.points

    board_nodes = []
    board_edges = []

    for board_point in points:
        num = board_point.num
        uuid = board_point.uuid
        board_nodes.append(
            BoardNode(
                num=num,
                point_num=num,
                point_uuid=uuid,
                path_num=None,
                path_segment_num_a=None,
                path_segment_num_b=None,
            )
        )

    node_counter = len(board_nodes) + 1
    edge_counter = 1
    segment_counter = 1

    for frozen_path in board_paths:
        num_path_segments = len(frozen_path.path.segments)
        for path_segment_num, segment in enumerate(frozen_path.path.segments):

            src = None
            dst = None

            if num_path_segments == 1:
                src = frozen_path.start_point_num
                dst = frozen_path.end_point_num
            else:
                if path_segment_num == 0:
                    src = frozen_path.start_point_num
                    dst = node_counter
                    board_nodes.append(
                        BoardNode(
                            num=node_counter,
                            point_num=None,
                            point_uuid=None,
                            path_num=frozen_path.num,
                            path_segment_num_a=path_segment_num + 1,
                            path_segment_num_b=path_segment_num + 2,
                        )
                    )
                    node_counter += 1
                elif path_segment_num == num_path_segments - 1:
                    dst = frozen_path.end_point_num
                    src = node_counter
                    board_nodes.append(
                        BoardNode(
                            num=node_counter,
                            point_num=None,
                            point_uuid=None,
                            path_num=frozen_path.num,
                            path_segment_num_a=path_segment_num - 1,
                            path_segment_num_b=path_segment_num,
                            # node_counter,
                            # None,
                            # None,
                            # frozen_path.num,
                            # path_segment_num - 1,
                            # path_segment_num,
                        )
                    )
                    node_counter += 1
                else:
                    src = node_counter
                    board_nodes.append(
                        BoardNode(
                            num=node_counter,
                            point_num=None,
                            point_uuid=None,
                            path_num=frozen_path.num,
                            path_segment_num_a=path_segment_num + 1,
                            path_segment_num_b=path_segment_num + 2,
                            # node_counter,
                            # None,
                            # None,
                            # frozen_path.num,
                            # path_segment_num + 1,
                            # path_segment_num + 2,
                        )
                    )
                    node_counter += 1

                    dst = node_counter
                    board_nodes.append(
                        BoardNode(
                            num=node_counter,
                            point_num=None,
                            point_uuid=None,
                            path_num=frozen_path.num,
                            path_segment_num_a=path_segment_num + 1,
                            path_segment_num_b=path_segment_num + 2,
                            # node_counter,
                            # None,
                            # None,
                            # frozen_path.num,
                            # path_segment_num + 1,
                            # path_segment_num + 2,
                        )
                    )
                    node_counter += 1

            board_edges.append(
                BoardEdge(
                    num = edge_counter,
                    src=src,
                    dst=dst,
                    path_num=frozen_path.num,
                    path_segment_num=path_segment_num + 1,
                    segment_num=segment_counter,
                    # edge_counter,
                    # src,
                    # dst,
                    # frozen_path.num,
                    # path_segment_num + 1,
                    # segment_counter,
                )
            )
            board_edges.append(
                BoardEdge(
                    num = edge_counter + 1,
                    src=dst,
                    dst=src,
                    path_num=frozen_path.num,
                    path_segment_num=path_segment_num + 1,
                    segment_num=segment_counter,
                    # edge_counter + 1,
                    # dst,
                    # src,
                    # frozen_path.num,
                    # path_segment_num + 1,
                    # segment_counter,
                )
            )

            edge_counter += 2
            segment_counter += 1

    num_nodes = len(board_nodes)
    adj_mat = torch.zeros((num_nodes, num_nodes), dtype=torch.int32)
    edge_dict = {}

    for edge in board_edges:
        adj_mat[edge.src - 1, edge.dst - 1] = 1
        edge_dict[(edge.src, edge.dst)] = edge
    edge_coords = [
        (i+1, j+1)
        for i in range(adj_mat.shape[0])
        for j in range(adj_mat.shape[1])
        if adj_mat[i, j] == 1
    ]

    ordered_edges = [edge_dict[edge_coord] for edge_coord in edge_coords]
    board_graph = BoardGraph(
        nodes=board_nodes,
        edges=ordered_edges,
        adj=adj_mat,
    )
    return board_graph
