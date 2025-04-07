# coding = utf-8
# @Time    : 2025-04-02  12:29:36
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: ASR Model.

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dguard_lite')
logger.setLevel(logging.INFO)

import os
from daudio.asr.aliasr.auto.auto_model import AutoModel
from daudio.asr.aliasr.utils.postprocess_utils import rich_transcription_postprocess

class DguardASR:
    def __init__(self, device='cuda:0'):
        DGUARD_MODEL_PATH = os.getenv('DGUARD_MODEL_PATH', None)
        if DGUARD_MODEL_PATH is not None:
            model_dir = os.path.join(DGUARD_MODEL_PATH, 'aliasr')
        else:
            logger.warning(f"[ASR] DGUARD_MODEL_PATH is not set and default path {os.path.expanduser('~/.dguard')} will be used.")
            DGUARD_MODEL_PATH = os.path.expanduser('~/.dguard')
            model_dir = os.path.join(DGUARD_MODEL_PATH, 'aliasr')
            if not os.path.exists(DGUARD_MODEL_PATH):
                logger.error(f'[ASR] Default path {DGUARD_MODEL_PATH} does not exist.')
                raise FileNotFoundError(f'DGUARD_MODEL_PATH is not set, and default path {DGUARD_MODEL_PATH} does not exist.')
            if not os.path.exists(model_dir):
                logger.error(f'[ASR] Model file {model_dir} does not exist in default path {DGUARD_MODEL_PATH}.')
                raise FileNotFoundError(f'Model file {model_dir} does not exist in default path {DGUARD_MODEL_PATH}.')
        self.model = AutoModel(device=device)

    def infer(self, audio_path, language='zh'):
        res = self.model.generate(input=audio_path, cache={}, language=language, use_itn=True, batch_size_s=60, merge_vad=True, merge_length_s=15)
        text = rich_transcription_postprocess(res[0]['text'])
        return text

if __name__ == '__main__':
    asr = DguardASR(device='cpu')
    audio_path = '/home/zhaosheng/Documents/dguard_project/dguard_home/aliasr/example/zh.mp3'
    text = asr.infer(audio_path)
    print(text)