import json
import logging
import os.path
import random
import string
import time
import torch
from omegaconf import ListConfig
from tqdm import tqdm
from typing import List, Tuple, Union

from daudio.asr.aliasr.train_utils.load_pretrained_model import load_pretrained_model
from daudio.asr.aliasr.train_utils.set_all_random_seed import set_all_random_seed
from daudio.asr.aliasr.utils import misc
from daudio.asr.aliasr.utils.misc import deep_update
from daudio.asr.aliasr.frontends.wav_frontend import WavFrontend
from daudio.asr.aliasr.tokenizer.sentencepiece_tokenizer import SentencepiecesTokenizer
from daudio.asr.aliasr.models.sense_voice.model import SenseVoiceSmall
from daudio.asr.aliasr.info import my_config

def generate_random_key() -> str:
    chars = string.ascii_letters + string.digits
    return 'rand_key_' + ''.join(random.choice(chars) for _ in range(13))

def process_file(data_in: str) -> Tuple[List[str], List[str]]:
    filelist = {'.scp', '.txt', '.json', '.jsonl', '.text'}
    key_list, data_list = [], []

    (_, file_extension) = os.path.splitext(data_in)
    file_extension = file_extension.lower()

    if file_extension in filelist:
        with open(data_in, encoding='utf-8') as fin:
            for line in fin:
                key = generate_random_key()
                if file_extension == '.jsonl':
                    data = json.loads(line.strip()).get('source', {})
                    key = data.get('key', key)
                else:
                    parts = line.strip().split(maxsplit=1)
                    key = parts[0] if len(parts) > 1 else key
                    data = parts[1] if len(parts) > 1 else parts[0]

                key_list.append(key)
                data_list.append(data)
    else:
        key = misc.extract_filename_without_extension(data_in)
        return [key], [data_in]

    return key_list, data_list

def prepare_data_iterator(
    data_in: Union[str, List[str]], 
    data_type: Union[None, List[str]] = None, 
    key: str = None
) -> Tuple[List[str], List[str]]:
    if isinstance(data_in, str) and os.path.exists(data_in):
        return process_file(data_in)

    key_list, data_list = [], []

    if isinstance(data_in, (list, tuple)):
        if data_type and isinstance(data_type, (list, tuple)):
            data_list_tmp = [prepare_data_iterator(d, t)[1] for d, t in zip(data_in, data_type)]
            data_list = list(zip(*data_list_tmp))
        else:
            for data_i in data_in:
                key = misc.extract_filename_without_extension(data_i) if isinstance(data_i, str) and os.path.exists(data_i) else generate_random_key()
                key_list.append(key)
            data_list = data_in
    else:
        key = key or generate_random_key()
        key_list = [key]
        data_list = [data_in]

    return key_list, data_list


class AutoModel:

    def __init__(self, device="cuda"):
        (model, kwargs) = self.build_model(device)
        self.kwargs = kwargs
        self.model = model
        self.model_path = kwargs.get('model_path')

    @staticmethod
    def build_model(device=None):
        kwargs = my_config
        if device is not None:
            kwargs['device'] = device
        set_all_random_seed(kwargs.get('seed', 0))
        torch.set_num_threads(kwargs.get('ncpu', 4))
        tokenizer = kwargs.get('tokenizer', None)
        kwargs['tokenizer'] = tokenizer
        kwargs['vocab_size'] = -1
        tokenizer_class = SentencepiecesTokenizer
        tokenizer_conf = kwargs.get('tokenizer_conf', None)
        tokenizers_build = tokenizer_class(**tokenizer_conf)
        vocab_size = tokenizers_build.get_vocab_size()
        token_lists = kwargs.get('token_lists', [])
        kwargs['tokenizer'] = tokenizers_build
        kwargs['vocab_size'] = vocab_size
        kwargs['token_list'] = token_lists
        frontend = kwargs.get('frontend', None)
        kwargs['input_size'] = None
        frontend_class = WavFrontend
        frontend = frontend_class(**kwargs.get('frontend_conf', {}))
        kwargs['input_size'] = frontend.output_size() if hasattr(frontend, 'output_size') else None
        kwargs['frontend'] = frontend
        model_class = SenseVoiceSmall
        assert model_class is not None, f"{kwargs['model']} is not registered"
        model_conf = {}
        deep_update(model_conf, kwargs.get('model_conf', {}))
        deep_update(model_conf, kwargs)
        model = model_class(**model_conf)
        init_param = kwargs.get('init_param', None)
        load_pretrained_model(model=model, path=init_param, 
                ignore_init_mismatch=kwargs.get('ignore_init_mismatch', True), 
                oss_bucket=kwargs.get('oss_bucket', None), 
                scope_map=kwargs.get('scope_map', []), 
                excludes=kwargs.get('excludes', None))
        model.to(device)
        return (model, kwargs)

    def __call__(self, *args, **cfg):
        kwargs = self.kwargs
        deep_update(kwargs, cfg)
        res = self.model(*args, kwargs)
        return res

    def generate(self, input, input_len=None, **cfg):
        return self.inference(input, input_len=input_len, **cfg)

    def inference(self, input, input_len=None, model=None, kwargs=None, key=None, **cfg):
        kwargs = self.kwargs if kwargs is None else kwargs
        if 'cache' in kwargs:
            kwargs.pop('cache')
        deep_update(kwargs, cfg)
        model = self.model if model is None else model
        model.eval()
        batch_size = kwargs.get('batch_size', 1)
        (key_list, data_list) = prepare_data_iterator(input, data_type=kwargs.get('data_type', None), key=key)
        speed_stats = {}
        asr_result_list = []
        num_samples = len(data_list)
        disable_pbar = self.kwargs.get('disable_pbar', False)
        pbar = tqdm(colour='blue', total=num_samples, dynamic_ncols=True) if not disable_pbar else None
        time_speech_total = 0.0
        time_escape_total = 0.0
        for beg_idx in range(0, num_samples, batch_size):
            end_idx = min(num_samples, beg_idx + batch_size)
            data_batch = data_list[beg_idx:end_idx]
            key_batch = key_list[beg_idx:end_idx]
            batch = {'data_in': data_batch, 'key': key_batch}
            if end_idx - beg_idx == 1 and kwargs.get('data_type', None) == 'fbank':
                batch['data_in'] = data_batch[0]
                batch['data_lengths'] = input_len
            time1 = time.perf_counter()
            with torch.no_grad():
                res = model.inference(**batch, **kwargs)
                if isinstance(res, (list, tuple)):
                    results = res[0] if len(res) > 0 else [{'text': ''}]
                    meta_data = res[1] if len(res) > 1 else {}
            time2 = time.perf_counter()
            asr_result_list.extend(results)
            batch_data_time = meta_data.get('batch_data_time', -1)
            time_escape = time2 - time1
            speed_stats['load_data'] = meta_data.get('load_data', 0.0)
            speed_stats['extract_feat'] = meta_data.get('extract_feat', 0.0)
            speed_stats['forward'] = f'{time_escape:0.3f}'
            speed_stats['batch_size'] = f'{len(results)}'
            speed_stats['rtf'] = f'{time_escape / batch_data_time:0.3f}'
            description = f'{speed_stats}, '
            if pbar:
                pbar.update(end_idx - beg_idx)
                pbar.set_description(description)
            time_speech_total += batch_data_time
            time_escape_total += time_escape
        if pbar:
            pbar.set_description(f'rtf_avg: {time_escape_total / time_speech_total:0.3f}')
        torch.cuda.empty_cache()
        return asr_result_list
