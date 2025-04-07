import os
from io import BytesIO
import kaldiio
import numpy as np
import torch
import torchaudio
from torch.nn.utils.rnn import pad_sequence
import subprocess
import os
import torch
import torchaudio
import numpy as np
import kaldiio

def load_audio(data_path, fs, audio_fs, **kwargs):
    """加载音频文件"""
    data, audio_fs = torchaudio.load(data_path)
    if kwargs.get('reduce_channels', True):
        data = data.mean(0)
    if audio_fs != fs:
        resampler = torchaudio.transforms.Resample(audio_fs, fs)
        data = resampler(data[None, :])[0, :]
    
    return data

def load_text(data, tokenizer):
    """处理文本数据"""
    return tokenizer.encode(data) if tokenizer else data

def load_kaldi_ark(data_path):
    """加载 Kaldi ark 格式数据"""
    data_mat = kaldiio.load_mat(data_path)
    mat = data_mat if not isinstance(data_mat, tuple) else data_mat[1]

    if mat.dtype in ('int16', 'int32'):
        mat = mat.astype(np.float64) / 32768
    return mat[:, 0] if mat.ndim == 2 else mat

def load_audio_text_image_video(data, fs=16000, audio_fs=16000, data_type='sound', tokenizer=None, **kwargs):
    """加载不同类型的数据"""
    if isinstance(data, (list, tuple)):
        return [load_audio_text_image_video(d, fs, audio_fs, data_type, tokenizer, **kwargs) for d in data]

    if isinstance(data, str):
        if os.path.exists(data):
            loader_map = {
                'sound': load_audio,
                'text': load_text,
                'kaldi_ark': load_kaldi_ark,
                'image': lambda x, **kw: x,  # 未来可扩展
                'video': lambda x, **kw: x   # 未来可扩展
            }
            return loader_map.get(data_type, lambda x, **kw: x)(data, fs=fs, audio_fs=audio_fs, tokenizer=tokenizer, **kwargs)
        elif data_type == 'text' and tokenizer:
            return load_text(data, tokenizer)

    if isinstance(data, np.ndarray):
        return torch.from_numpy(data)
    
    return data


def extract_fbank(data, data_len=None, data_type: str='sound', frontend=None, **kwargs):
    if isinstance(data, np.ndarray):
        data = torch.from_numpy(data)
        if len(data.shape) < 2:
            data = data[None, :]
        data_len = [data.shape[1]] if data_len is None else data_len
    elif isinstance(data, torch.Tensor):
        if len(data.shape) < 2:
            data = data[None, :]
        data_len = [data.shape[1]] if data_len is None else data_len
    elif isinstance(data, (list, tuple)):
        (data_list, data_len) = ([], [])
        for data_i in data:
            if isinstance(data_i, np.ndarray):
                data_i = torch.from_numpy(data_i)
            data_list.append(data_i)
            data_len.append(data_i.shape[0])
        data = pad_sequence(data_list, batch_first=True)
    (data, data_len) = frontend(data, data_len, **kwargs)
    if isinstance(data_len, (list, tuple)):
        data_len = torch.tensor([data_len])
    return (data.to(torch.float32), data_len.to(torch.int32))