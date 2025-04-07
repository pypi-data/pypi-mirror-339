import os
import io
import shutil
import logging
from collections import OrderedDict
import numpy as np
from omegaconf import DictConfig, OmegaConf

def deep_update(original, update):
    for (key, value) in update.items():
        if isinstance(value, dict) and key in original:
            if len(value) == 0:
                original[key] = value
            deep_update(original[key], value)
        else:
            original[key] = value

def extract_filename_without_extension(file_path):
    """
    从给定的文件路径中提取文件名（不包含路径和扩展名）
    :param file_path: 完整的文件路径
    :return: 文件名（不含路径和扩展名）
    """
    filename_with_extension = os.path.basename(file_path)
    (filename, extension) = os.path.splitext(filename_with_extension)
    return filename