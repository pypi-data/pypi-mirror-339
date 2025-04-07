# coding = utf-8
# @Time    : 2024-12-16  17:26:28
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Mos model.

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('daudio')
logger.setLevel(logging.INFO)

import os
import uuid
import librosa
import numpy as np
import onnxruntime as ort
import soundfile as sf
import torchaudio
import torch
import subprocess
import io
import base64

SAMPLING_RATE = 16000
INPUT_LENGTH = 9.01
logger.info(f"[DNS] Sampling rate: {SAMPLING_RATE}, Input length: {INPUT_LENGTH}")

DGUARD_MODEL_PATH = os.environ.get("DGUARD_MODEL_PATH")
if DGUARD_MODEL_PATH is None:
    # use default path ~/.dguard
    DGUARD_MODEL_PATH = os.path.expanduser("~/.dguard")
    if not os.path.exists(DGUARD_MODEL_PATH):
        logger.error("[DNS] Default path ~/.dguard does not exist.")
        raise FileNotFoundError("Default path ~/.dguard does not exist.")
    else:
        logger.info(f"[DNS] Using default path: {DGUARD_MODEL_PATH}")

def load_wav(
    wav_file, sr, channel=0, wavform_normalize=True, saveto=None, start_time=None
):
    """
    Enhanced load_wav function to support .wav, .npy, numpy.ndarray, torch.Tensor,
    binary, and Base64 encoded formats.
    """
    logger.warning("[DNS] load_wav: It is not recommended to use file reading.")
    pcm, orig_sr = torchaudio.load(wav_file, normalize=wavform_normalize)
    if pcm.dim() == 1:
        pcm = pcm.unsqueeze(0)
    else:
        pcm = pcm[channel].unsqueeze(0)
    if orig_sr != sr:
        resampler = torchaudio.transforms.Resample(orig_freq=orig_sr, new_freq=sr)
        pcm = resampler(pcm)
    pcm = pcm.reshape(-1).numpy()
    return pcm, sr

def remove_file(filepath):
    """Remove file if it exists."""
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            raise e
        else:
            print(f"Removed file: {filepath}")
    else:
        print(f"File not found: {filepath}")

class ComputeScore:
    def __init__(self, primary_model_path, p808_model_path, device) -> None:
        self.device = device
        if "cuda" in device:
            _config = {"cudnn_conv_use_max_workspace": '0'}
            self.onnx_sess = ort.InferenceSession(primary_model_path, providers=[('CUDAExecutionProvider', _config)])
            self.p808_onnx_sess = ort.InferenceSession(p808_model_path, providers=[('CUDAExecutionProvider', _config)])
        elif "npu" in device:
            if "ASCEND_DEVICE_ID" not in os.environ:
                logger.error("[Lite] Please set ENV: ASCEND_DEVICE_ID")
                raise ValueError("Please set ENV: ASCEND_DEVICE_ID")
            _config = {'device_id': int(os.environ['ASCEND_DEVICE_ID'])}
            self.onnx_sess = ort.InferenceSession(primary_model_path, providers=[('CANNExecutionProvider', _config)])
            self.p808_onnx_sess = ort.InferenceSession(p808_model_path, providers=[('CANNExecutionProvider', _config)])
        else:   
            self.onnx_sess = ort.InferenceSession(primary_model_path, providers=['CPUExecutionProvider'])
            self.p808_onnx_sess = ort.InferenceSession(p808_model_path, providers=['CPUExecutionProvider'])
        logger.info(f"[DNS] ONNX session created with provider: {self.onnx_sess.get_providers()}")
        self.resample_8000 = torchaudio.transforms.Resample(orig_freq=8000, new_freq=SAMPLING_RATE).to(self.device)

    def audio_melspec(
        self, audio, n_mels=120, frame_size=320, hop_length=160, sr=16000, to_db=True
    ):
        mel_spec = librosa.feature.melspectrogram(
            y=audio, sr=sr, n_fft=frame_size + 1, hop_length=hop_length, n_mels=n_mels
        )
        if to_db:
            mel_spec = (librosa.power_to_db(mel_spec, ref=np.max) + 40) / 40
        return mel_spec.T

    def get_polyfit_val(self, sig, bak, ovr, is_personalized_MOS):
        if is_personalized_MOS:
            p_ovr = np.poly1d([-0.00533021, 0.005101, 1.18058466, -0.11236046])
            p_sig = np.poly1d([-0.01019296, 0.02751166, 1.19576786, -0.24348726])
            p_bak = np.poly1d([-0.04976499, 0.44276479, -0.1644611, 0.96883132])
        else:
            p_ovr = np.poly1d([-0.06766283, 1.11546468, 0.04602535])
            p_sig = np.poly1d([-0.08397278, 1.22083953, 0.0052439])
            p_bak = np.poly1d([-0.13166888, 1.60915514, -0.39604546])

        sig_poly = p_sig(sig)
        bak_poly = p_bak(bak)
        ovr_poly = p_ovr(ovr)

        return sig_poly, bak_poly, ovr_poly

    def __call__(self, audio, fs, sampling_rate, is_personalized_MOS):
        if fs != SAMPLING_RATE:
            if isinstance(audio, np.ndarray):
                audio = torch.tensor(audio)
            audio = audio.to(self.device)
            audio = self.resample_8000(audio).cpu().numpy().reshape(-1)
            fs = SAMPLING_RATE
        else:
            if isinstance(audio, np.ndarray):
                audio = torch.tensor(audio)
            audio = audio.to(self.device)
            resampler = torchaudio.transforms.Resample(orig_freq=fs, new_freq=SAMPLING_RATE)
            audio = resampler(audio).reshape(-1).cpu().numpy()
            fs = SAMPLING_RATE
        audio = audio.astype("float32")
        fs = int(fs)
        actual_audio_len = len(audio)
        len_samples = int(INPUT_LENGTH * fs)
        while len(audio) < len_samples:
            audio = np.append(audio, audio)
        num_hops = int(np.floor(len(audio) / fs) - INPUT_LENGTH) + 1
        hop_len_samples = fs
        predicted_mos_sig_seg_raw = []
        predicted_mos_bak_seg_raw = []
        predicted_mos_ovr_seg_raw = []
        predicted_mos_sig_seg = []
        predicted_mos_bak_seg = []
        predicted_mos_ovr_seg = []
        predicted_p808_mos = []
        num_hops = min(1, num_hops) # Only one hop
        for idx in range(num_hops):
            audio_seg = audio[
                int(idx * hop_len_samples) : int((idx + INPUT_LENGTH) * hop_len_samples)
            ]
            if len(audio_seg) < len_samples:
                continue
            input_features = np.array(audio_seg).astype("float32")[np.newaxis, :]
            p808_input_features = np.array(
                self.audio_melspec(audio=audio_seg[:-160])
            ).astype("float32")[np.newaxis, :, :]
            oi = {"input_1": input_features}
            p808_oi = {"input_1": p808_input_features}
            p808_mos = self.p808_onnx_sess.run(None, p808_oi)[0][0][0]
            mos_sig_raw, mos_bak_raw, mos_ovr_raw = self.onnx_sess.run(None, oi)[0][0]
            mos_sig, mos_bak, mos_ovr = self.get_polyfit_val(
                mos_sig_raw, mos_bak_raw, mos_ovr_raw, is_personalized_MOS
            )
            predicted_mos_sig_seg_raw.append(mos_sig_raw)
            predicted_mos_bak_seg_raw.append(mos_bak_raw)
            predicted_mos_ovr_seg_raw.append(mos_ovr_raw)
            predicted_mos_sig_seg.append(mos_sig)
            predicted_mos_bak_seg.append(mos_bak)
            predicted_mos_ovr_seg.append(mos_ovr)
            predicted_p808_mos.append(p808_mos)
        fpath = f"{DGUARD_MODEL_PATH}/tmp/{str(uuid.uuid1())}.wav"
        clip_dict = {"filename": fpath, "len_in_sec": actual_audio_len / fs, "sr": fs}
        clip_dict["num_hops"] = num_hops
        clip_dict["OVRL_raw"] = np.mean(predicted_mos_ovr_seg_raw)
        clip_dict["SIG_raw"] = np.mean(predicted_mos_sig_seg_raw)
        clip_dict["BAK_raw"] = np.mean(predicted_mos_bak_seg_raw)
        clip_dict["OVRL"] = np.mean(predicted_mos_ovr_seg)
        clip_dict["SIG"] = np.mean(predicted_mos_sig_seg)
        clip_dict["BAK"] = np.mean(predicted_mos_bak_seg)
        clip_dict["P808_MOS"] = np.mean(predicted_p808_mos)
        return clip_dict

class DguardMos:
    def __init__(self, personalized_MOS=False, channel=0, start_time=0, device="cpu"):
        self.device = device
        self.personalized_MOS = personalized_MOS
        dguard_model_path = os.environ.get("DGUARD_MODEL_PATH")
        self.dguard_model_path = dguard_model_path
        if dguard_model_path is None:
            logger.error("[DNS] Please set the DGUARD_MODEL_PATH environment variable.")
            raise ValueError("Please set the DGUARD_MODEL_PATH environment variable.")
        p808_model_path = f"{dguard_model_path}/model_v8.onnx"
        if not os.path.exists(p808_model_path):
            logger.error(
                f"[DNS] model_v8.onnx not found in {dguard_model_path}. Please download it first."
            )
            raise ValueError(
                f"model_v8.onnx not found in {dguard_model_path}. Please download it first."
            )
        if personalized_MOS:
            primary_model_path = f"{dguard_model_path}/p_sig_bak_ovr.onnx"
            if not os.path.exists(primary_model_path):
                logger.error(
                    f"[DNS] p_sig_bak_ovr.onnx not found in {dguard_model_path}. Please download it first."
                )
                raise ValueError(
                    f"p_sig_bak_ovr.onnx not found in {dguard_model_path}. Please download it first."
                )
        else:
            primary_model_path = f"{dguard_model_path}/sig_bak_ovr.onnx"
            if not os.path.exists(primary_model_path):
                logger.error(
                    f"[DNS] sig_bak_ovr.onnx not found in {dguard_model_path}. Please download it first."
                )
                raise ValueError(
                    f"sig_bak_ovr.onnx not found in {dguard_model_path}. Please download it first."
                )
        self.compute_score = ComputeScore(primary_model_path, p808_model_path, device)
        self.is_personalized_eval = personalized_MOS
        self.desired_fs = 16000
        self.channel = channel
        self.start_time = start_time

    def dnsmos(self, audio_path):
        pcm, sample_rate = load_wav(
            audio_path,
            sr=16000,
            channel=self.channel,
            wavform_normalize=True,
            saveto=None,
            start_time=self.start_time,
        )
        result = self.compute_score(
            pcm, sample_rate, self.desired_fs, self.is_personalized_eval
        )
        return result
    
    def dnsmos_data(self, pcm, sample_rate):
        result = self.compute_score(
            pcm, sample_rate, self.desired_fs, self.is_personalized_eval
        )
        return result
