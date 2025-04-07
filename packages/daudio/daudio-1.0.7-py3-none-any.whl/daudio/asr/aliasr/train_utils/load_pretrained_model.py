from io import BytesIO
import logging
import torch
import torch.nn
import torch.optim
import copy

def load_pretrained_model(
    path: str,
    model: torch.nn.Module,
    ignore_init_mismatch: bool = True,
    map_location: str = "cpu",
    oss_bucket=None,
    scope_map=None,
    excludes=None,
    **kwargs
):
    """Load a model state and set it to the model."""
    logging.info(f"Loading checkpoint from: {path}")
    dst_state = model.state_dict()

    # 读取模型参数
    ori_state = _load_checkpoint(path, map_location, oss_bucket)
    src_state = _extract_model_state(ori_state)

    scope_map = _parse_scope_map(scope_map)
    excludes = _parse_excludes(excludes)

    # 进行参数匹配并加载
    mapped_state = _map_parameters(dst_state, src_state, scope_map, excludes, ignore_init_mismatch)

    # 加载参数
    flag = model.load_state_dict(mapped_state, strict=True)
    logging.info(f"Checkpoint {path} loaded successfully, status: {flag}")

def _load_checkpoint(path, map_location, oss_bucket):
    """加载 checkpoint"""
    if oss_bucket is None:
        return torch.load(path, map_location=map_location)
    buffer = BytesIO(oss_bucket.get_object(path).read())
    return torch.load(buffer, map_location=map_location)

def _extract_model_state(ori_state):
    """提取模型的 state_dict"""
    for key in ["state_dict", "model_state_dict", "model"]:
        if key in ori_state:
            return ori_state[key]
    return ori_state

def _parse_scope_map(scope_map):
    """解析 scope_map"""
    if isinstance(scope_map, str):
        return scope_map.split(",") + ["module.", "None"]
    return (scope_map or []) + ["module.", "None"]

def _parse_excludes(excludes):
    """解析排除参数"""
    if isinstance(excludes, str):
        return excludes.split(",")
    return excludes or []

def _map_parameters(dst_state, src_state, scope_map, excludes, ignore_init_mismatch):
    """匹配参数并加载"""
    mapped_state = copy.deepcopy(dst_state)

    for dst_key in dst_state.keys():
        if any(dst_key.startswith(ex) for ex in excludes):
            logging.info(f"Excluding key: {dst_key}")
            continue

        src_key = _find_matching_key(dst_key, src_state, scope_map)
        if src_key and src_key in src_state:
            if ignore_init_mismatch and dst_state[dst_key].shape != src_state[src_key].shape:
                logging.info(f"Shape mismatch, ignoring key: {dst_key} ({dst_state[dst_key].shape} != {src_state[src_key].shape})")
            else:
                mapped_state[dst_key] = src_state[src_key]
        else:
            logging.warning(f"Missing key in checkpoint: {dst_key}")

    return mapped_state

def _find_matching_key(dst_key, src_state, scope_map):
    """查找匹配的 key"""
    for i in range(0, len(scope_map), 2):
        src_prefix = scope_map[i] if scope_map[i].lower() != "none" else ""
        dst_prefix = scope_map[i + 1] if scope_map[i + 1].lower() != "none" else ""

        if dst_prefix == "" and src_prefix + dst_key in src_state:
            return src_prefix + dst_key
        if dst_key.startswith(dst_prefix):
            new_key = dst_key.replace(dst_prefix, src_prefix, 1)
            if new_key in src_state:
                return new_key
    return dst_key if dst_key in src_state else None
