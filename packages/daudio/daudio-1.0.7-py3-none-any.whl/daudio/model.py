# coding = utf-8
# @Time    : 2025-03-12  16:52:12
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: DGuard Lite model.
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('daudio')
logger.setLevel(logging.INFO)

import torchaudio # torchaudio should be imported before torch
from torchaudio.compliance import kaldi
import os
import time
import torch
try:
    # for HUAWEI Ascend NPU
    import torch_npu
except ImportError:
    logger.error("[ERROR] torch_npu not found, please install it first.")
    logger.error("[ERROR] if you are not using NPU, please ignore.")
import numpy as np
import onnxruntime as ort
from daudio.diarize import subsegment, cluster, merge_segments
from torch.nn import functional as F


MAX_AUDIO_DURATION = 600
MIN_AUDIO_DURATION = 0.5

# set seed for onnxruntime
ort.set_seed(1)
np.random.seed(1)
torch.manual_seed(1)

logger.info(f"MAX_AUDIO_DURATION: {MAX_AUDIO_DURATION}")
logger.info(f"MIN_AUDIO_DURATION: {MIN_AUDIO_DURATION}")
logger.info(f"torch version: {torch.__version__}")
logger.info(f"torchaudio version: {torchaudio.__version__}")
logger.info(f"onnxruntime version: {ort.__version__}")

class VADIterator:
    """
    Voice Activity Detection (VAD) Iterator
    """
    def __init__(
        self,
        sample_rate: int = 8000,
        frame_length: int = 1024,
        hop_length: int = 512,
        min_speech_duration_s: int = 0.25,
        merge_close_segments_s: int = 0.1,
        energy_threshold: float = 0.1,
    ):
        self.sample_rate = sample_rate
        self.frame_length = frame_length
        self.hop_length = hop_length
        self.min_speech_duration_s = min_speech_duration_s
        self.merge_close_segments_s = merge_close_segments_s
        self.energy_threshold = energy_threshold
        self.segments = []
        self.speech_data = np.array([])
        
    def __call__(self, data):
        assert isinstance(data, np.ndarray)
        now_start_time_s = len(self.speech_data) / self.sample_rate
        self.speech_data = np.concatenate([self.speech_data, data])
        # Calculate energy
        energy = np.array([
            np.sum(np.abs(data[i:i + self.frame_length]**2))
            for i in range(0, len(data) - self.frame_length + 1, self.hop_length)
        ])
        is_speech = energy > self.energy_threshold
        speech_frames = np.where(is_speech)[0]
        for i in speech_frames:
            start_time = now_start_time_s + (i * self.hop_length / self.sample_rate)
            end_time = start_time + (self.frame_length / self.sample_rate)
            logger.info(f"[VAD] Speech frame: {start_time:.2f}s - {end_time:.2f}s")
            self.segments.append((start_time, end_time))
        return is_speech
    
    def smooth(self):
        if len(self.segments) == 0:
            return
        merged_segments = []
        current_start, current_end = self.segments[0]
        for start, end in self.segments[1:]:
            if start - current_end <= self.merge_close_segments_s:
                current_end = end
            else:
                merged_segments.append((current_start, current_end))
                current_start, current_end = start, end
        merged_segments.append((current_start, current_end))
        # Filter segments shorter than min_speech_duration_s
        formatted_segments = []
        self.segments = merged_segments
        for start, end in self.segments:
            if end - start >= self.min_speech_duration_s:
                formatted_segments.append((start, end))
        self.segments = formatted_segments

    def get_data(self):
        self.smooth()
        combined_audio = []
        if len(self.segments) == 0:
            return None
        for start, end in self.segments:
            start_sample = int(start * self.sample_rate)
            end_sample = int(end * self.sample_rate)
            segment_audio = self.speech_data[start_sample:end_sample]
            combined_audio.append(segment_audio)
        combined_audio = np.concatenate(combined_audio)
        return combined_audio

class DGuardLite:
    """
    DGuard Lite model
    """
    def __init__(
        self,
        embedding_model_names, # string(split by ,) or list
        device="cpu", # Device: "cpu", "cuda", "npu"
        length=-1, # -1 means no split
        max_split_num=5, # only split to max_split_num segments
        start_time=0, # start time in seconds
        mean=False, # get mean of embeddings from all segments
        channel=0, # channel of audio
        sample_rate=16000, # sample rate of model !Note: this is the sample rate of model, not the sample rate of audio
        # vad
        apply_vad=False, # apply vad to audio before embedding
        vad_min_duration=0.25, # minimum duration of speech
        vad_smooth_threshold=0.25, # merge close segments
        # diar
        diar_num_spks=None,
        diar_min_num_spks=1,
        diar_max_num_spks=20,
        diar_min_duration=0.255,
        diar_window_secs=1.5,
        diar_period_secs=0.75,
        diar_frame_shift=10,
        diar_batch_size=4,
        diar_subseg_cmn=True,
        diar_max_split_num=999,
        load_spoof=True, # Load ASV-Spoof model
        spoof_model_name="dguard_asv_20250210.onnx", # Load ASV-Spoof model
        sv_pad_data_to_length=False, # Pad data to length before embedding
        spoof_pad_data_to_length=False, # Pad data to length before ASV-Spoof
    ):
        if not sv_pad_data_to_length:
            logger.warning(f"[Lite] PAD_DATA is off, please make sure you control audio lengh before \
                    input to dguard. (if length not same, your may meet OOM!!")
        if not mean:
            logger.warning(f"[Lite] MEAN is off, please make sure you know what you are doing.")
        # GPU Onnx model config
        if "npu" in device:
            if "ASCEND_DEVICE_ID" not in os.environ:
                logger.error("[Lite] Please set ENV: ASCEND_DEVICE_ID")
                raise ValueError("Please set ENV: ASCEND_DEVICE_ID")
            _config = {'device_id': int(os.environ['ASCEND_DEVICE_ID'])}
        else:
            _config = {"cudnn_conv_use_max_workspace": '0'}
        self.sample_rate = sample_rate
        self.length = length
        self.device = device
        self.sv_pad_data_to_length = sv_pad_data_to_length
        self.spoof_pad_data_to_length = spoof_pad_data_to_length
        if isinstance(embedding_model_names, str):
            if "," in embedding_model_names:
                embedding_model_names = embedding_model_names.split(",")
            else:
                embedding_model_names = [embedding_model_names]
        DGUARD_MODEL_PATH = os.getenv("DGUARD_MODEL_PATH", "~/.dguard'")
        if DGUARD_MODEL_PATH == "~/.dguard":
            logger.warning(f"[Lite] DGUARD_MODEL_PATH is not set, using default path: {DGUARD_MODEL_PATH}")
            DGUARD_MODEL_PATH = os.path.expanduser(DGUARD_MODEL_PATH)
        if DGUARD_MODEL_PATH is not None:
            sv_model_paths = [os.path.join(DGUARD_MODEL_PATH, model_name+".onnx") for model_name in embedding_model_names]
        else:
            logger.error(f"[Lite] DGUARD_MODEL_PATH is not set")
            raise ValueError("DGUARD_MODEL_PATH is not set")
        for model_path in sv_model_paths:
            if not os.path.exists(model_path):
                logger.error(f"[Lite] Model not found: {model_path}")
                raise ValueError(f"Model not found: {model_path}")
            else:
                logger.info(f"[Lite] __init__: Model found: {model_path}")
        spoof_model_path = os.path.join(DGUARD_MODEL_PATH, spoof_model_name)
        if os.path.exists(spoof_model_path):
            logger.info(f"[Lite] __init__: ASVSpoof Model found: {spoof_model_path}")
        else:
            spoof_model_path = None
        if isinstance(sv_model_paths, str):
            sv_model_paths = [sv_model_paths]
        sv_sessions = []
        self.sv_model_names = []
        for model_path in sv_model_paths:
            if "cuda" in device:
                if _config:
                    session = ort.InferenceSession(model_path, providers=[('CUDAExecutionProvider', _config)])
                else:
                    session = ort.InferenceSession(model_path, providers=['CUDAExecutionProvider'])
            elif "npu" in device:
                if _config:
                    session = ort.InferenceSession(model_path, providers=[('CANNExecutionProvider', _config)])
                else:
                    session = ort.InferenceSession(model_path, providers=['CANNExecutionProvider'])
            elif "cpu" in device:
                session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
            else:
                session = ort.InferenceSession(model_path)
            sv_sessions.append(session)
            self._warm_up_session(session)
            logger.info(f"[Lite] __init__: SV Model loaded: {model_path}, Providers: {session.get_providers()}")
            self.sv_model_names.append(os.path.basename(model_path))
        if spoof_model_path and load_spoof:
            if "cuda" in device:
                asv_session = ort.InferenceSession(spoof_model_path, providers=[("CUDAExecutionProvider", _config)])
            elif "npu" in device:
                asv_session = ort.InferenceSession(spoof_model_path, providers=[("CANNExecutionProvider", _config)])
            elif "cpu" in device:
                asv_session = ort.InferenceSession(spoof_model_path, providers=['CPUExecutionProvider'])
            else:
                asv_session = ort.InferenceSession(spoof_model_path)
            self._warm_up_session(asv_session)
            logger.info(f"[Lite] __init__: ASVSpoof Model loaded: {spoof_model_path}, Providers: {asv_session.get_providers()}")
        else:
            logger.warning(f"[Lite] __init__: ASVSpoof Model not loaded")
            asv_session = None
        # sv
        input_name = sv_sessions[0].get_inputs()[0].name
        output_name = sv_sessions[0].get_outputs()[0].name
        self.input_name = input_name
        self.output_name = output_name
        self.sv_sessions = sv_sessions
        self.session = sv_sessions[0] # default session for speaker diarization
        # asv
        if asv_session:
            asv_input_name = asv_session.get_inputs()[0].name
            asv_output_name = asv_session.get_outputs()[0].name
            self.asv_input_name = asv_input_name
            self.asv_output_name = asv_output_name
            self.asv_session = asv_session
        else:
            self.asv_input_name = None
            self.asv_output_name = None
            self.asv_session = None
        # vad
        self.channel = channel
        self.start_time = start_time
        self.apply_vad = apply_vad
        self.vad_min_duration = vad_min_duration
        self.vad_smooth_threshold = vad_smooth_threshold
        self.max_split_num = max_split_num
        self.mean = mean
        # diar
        self.diar_num_spks = diar_num_spks
        self.diar_min_num_spks = diar_min_num_spks
        self.diar_max_num_spks = diar_max_num_spks
        self.diar_min_duration = diar_min_duration
        self.diar_window_secs = diar_window_secs
        self.diar_period_secs = diar_period_secs
        self.diar_frame_shift = diar_frame_shift
        self.diar_batch_size = diar_batch_size
        self.diar_subseg_cmn = diar_subseg_cmn
        self.diar_max_split_num = diar_max_split_num
        self.resampler_8000 = torchaudio.transforms.Resample(orig_freq=8000, new_freq=self.sample_rate)
        self.resampler_8000.to(self.device)
        for k, v in self.__dict__.items():
            logger.info(f"[Lite] __init__: {k}: {v}")
        
    def _warm_up_session(self, session, times=5):
        if self.length <= 0: # no need to warm up
            logger.warning(f"[Lite] _warm_up_session: No need to warm up, because length is {self.length}")
            return
        # warm onnxruntime session, by using a dummy input
        # dummy input shape should be (1, num_frames)
        # num_frames should be self.sample_rate * self.length
        for _ in range(times):
            start_time = time.time()
            dummy_input = torch.randn(self.sample_rate * self.length)
            dummy_fbank = self._fbank(dummy_input.reshape(1,-1))
            dummy_fbank = dummy_fbank.cpu().numpy()
            result = session.run([session.get_outputs()[0].name], {session.get_inputs()[0].name: dummy_fbank})
            end_time = time.time()
            logger.info(f"[Lite] _warm_up_session: Warm up time (#{_}): {end_time - start_time:.2f}s")
        return result

    def _load_file(self, file_path):
        # Accepts: file_path (str)
        # Read audio file
        # Return: waveform (Tensor, shape=(num_samples))
        waveform, sr = torchaudio.load(file_path)
        waveform = waveform[self.channel, self.start_time*sr:self.start_time*sr+sr*MAX_AUDIO_DURATION]
        if sr == 8000:
            waveform = waveform.to(self.device)
            waveform = self.resampler_8000(waveform)
        elif sr != self.sample_rate:
            logger.error(f"[Lite] _load_file: Sample rate not supported: {sr}, only support 8000 or {self.sample_rate}")
            raise ValueError(f"Sample rate not supported: {sr}")
        return waveform.reshape(-1)

    def _split_data(self, data, pad_data_to_length=False):
        # Accepts: data (Tensor, shape=(num_samples))
        # Split audio data into segments
        # Return: data_list (List[Tensor, shape=(1,num_samples)])
        if self.length <= 0:
            return [data.reshape(1,-1)]
        L = self.sample_rate * self.length
        split_num = min(len(data) // L, self.max_split_num)
        if split_num == 0:
            if pad_data_to_length:
                append_data = torch.zeros(L - len(data))
                append_data = append_data.to(data.device)
                data = torch.cat([data, append_data]).reshape(1,-1)
                return [data]
            else:
                return [data.reshape(1,-1)]
        return [data[i*L : (i+1)*L].reshape(1,-1) 
                for i in range(split_num)] if split_num > 0 else []

    def _vad(self, data,
            energy_threshold: float = 0.1,
            frame_length: int = 1024,
            hop_length: int = 512,
            min_speech_duration_ms: int = 250,
            merge_close_segments_ms: int = 100,
            return_seconds: bool = True,
            max_speech_duration_s: int = 9999
        ):
        # Accepts: data (Tensor, shape=(num_samples))
        # Perform Voice Activity Detection (VAD) on audio data
        # Return: segments (List[Dict]), combined_audio (Tensor, shape=(num_samples))
        data = data.cpu().numpy()
        frame_duration_ms = (frame_length / self.sample_rate) * 1000
        energy = np.array([
            np.sum(np.abs(data[i:i + frame_length]**2))
            for i in range(0, len(data) - frame_length + 1, hop_length)
        ])
        is_speech = energy > energy_threshold
        speech_frames = np.where(is_speech)[0]
        if len(speech_frames) == 0:
            return [], None
        segments = []
        start = speech_frames[0]
        for i in range(1, len(speech_frames)):
            if speech_frames[i] != speech_frames[i - 1] + 1:
                end = speech_frames[i - 1]
                segments.append((start, end))
                start = speech_frames[i]
        segments.append((start, speech_frames[-1]))
        # Filter segments shorter than min_speech_duration_ms
        min_speech_frames = int((min_speech_duration_ms / frame_duration_ms))
        formatted_segments = []
        for start, end in segments:
            if end - start + 1 >= min_speech_frames:
                start_time = start * hop_length / self.sample_rate
                end_time = (end + 1) * hop_length / self.sample_rate
                formatted_segments.append((start_time, end_time))
        # Merge close segments
        merged_segments = []
        current_start, current_end = formatted_segments[0]
        for start, end in formatted_segments[1:]:
            if start - current_end <= merge_close_segments_ms / 1000:
                current_end = end
            else:
                merged_segments.append((current_start, current_end))
                current_start, current_end = start, end
        merged_segments.append((current_start, current_end))
        result_segments = [
            {
                "segment": i,
                "start": round(start if return_seconds else start * 1000, 3),
                "end": round(end if return_seconds else end * 1000, 3),
            }
            for i, (start, end) in enumerate(merged_segments)
        ]
        # Save combined audio segments to file if save_path is specified
        combined_audio = []
        for start, end in merged_segments:
            start_sample = int(start * self.sample_rate)
            end_sample = int(end * self.sample_rate)
            segment_audio = data[start_sample:end_sample]
            combined_audio.append(segment_audio)
        combined_audio = np.concatenate(combined_audio)
        return result_segments, combined_audio

    def _fbank(self, data,
                n_mels=80,
                frame_length=25, frame_shift=10, dither=0.0): # dither should be 0.0
        # Accepts: data (Tensor, shape=(1, num_samples))
        # Compute filterbank features (FBank) from audio data
        # Return: fbank (Tensor, shape=(1,num_frames,num_mels))
        data = data.to(self.device) # Fbank should be calculated on device
        # data = data.reshape(1, -1) # Fbank should be calculated on 2D data
        data = data * (1 << 15)
        fbank = kaldi.fbank(
            data,
            num_mel_bins=n_mels,
            frame_length=frame_length,
            frame_shift=frame_shift,
            sample_frequency=self.sample_rate,
            window_type='hamming',
            dither=dither,
            use_energy=False
        )
        fbank = fbank - torch.mean(fbank, dim=0) # CMN
        return fbank.unsqueeze(0) # Add channel dimension, and still on device

    def _encode(self, fbank):
        # Accepts: fbank (Tensor, shape=(1,num_frames,num_mels))
        # Extract speaker embedding from FBank features
        # Return: emb (np.array, shape=(num_dims))
        fbank = fbank.cpu().numpy()
        output_data = self.session.run([self.session.get_outputs()[0].name], {self.session.get_inputs()[0].name: fbank})[0]
        output_data = output_data.reshape(-1)
        output_data = output_data / np.linalg.norm(output_data)
        return output_data
    
    def _encode_by_session(self, fbank, session):
        # Accepts: fbank (Tensor, shape=(1,num_frames,num_mels))
        # Extract speaker embedding from FBank features
        # Return: emb (np.array, shape=(num_dims))
        if isinstance(fbank, torch.Tensor):
            fbank = fbank.cpu().numpy()
        if len(fbank.shape) == 2:
            fbank = fbank.reshape(1, fbank.shape[0], fbank.shape[1])
        # change data to float
        fbank = fbank.astype(np.float32)
        output_data = session.run([session.get_outputs()[0].name], {session.get_inputs()[0].name: fbank})[0]
        output_data = output_data.reshape(-1)
        output_data = output_data / np.linalg.norm(output_data)
        return output_data

    def _asv(self, fbank):
        # Accepts: fbank (Tensor, shape=(1,num_frames,num_mels))
        # Extract ASV embedding from FBank features
        # Return: emb (np.array, shape=(num_dims))
        if not self.asv_session:
            logger.error("[Lite] _asv: ASV model not loaded")
            raise ValueError("ASV model not loaded")
        fbank = fbank.cpu().numpy()
        output_data = self.asv_session.run([self.asv_output_name], {self.asv_input_name: fbank})[0]
        output_data = output_data.reshape(-1)
        return output_data

    def asv(self, wav_path):
        # Accepts: wav_path (str)
        # Perform Anti-Spoofing Verification (ASV) on audio file
        # Return: result (Dict)
        data = self._load_file(wav_path) # shape=(num_samples)
        data_list = self._split_data(data, self.spoof_pad_data_to_length) # List[Tensor, shape=(1,num_samples)]
        data = data_list[0] # shape=(1,num_samples)
        fbank = self._fbank(data) # shape=(1,num_frames,num_mels)
        emb = self._asv(fbank) # shape=(num_dims)
        emb = torch.tensor(emb).to(self.device)
        probs = F.softmax(emb, dim=-1)
        pred = torch.argmax(probs, dim=-1)
        # pred = 1 is fake
        label = "fake" if pred.item() == 1 else "real"
        if label == "fake":
            confidence = probs[1].item()
        else:
            confidence = probs[0].item()
        return {"label": label, "score": confidence}

    def encode(self, wav_path, apply_vad=False):
        # Accepts: wav_path (str)
        # Extract speaker embedding from audio file
        # Return: result (Dict)
        data = self._load_file(wav_path) # shape=(num_samples)
        if apply_vad:
            segments, data = self._vad(data)
        else:
            if self.apply_vad:
                segments, data = self._vad(data) # List[Dict], shape=(num_samples)
        if not isinstance(data, torch.Tensor):
            data = torch.from_numpy(data)
        data_list = self._split_data(data, self.sv_pad_data_to_length) # List[Tensor, shape=(1,num_samples)]
        output = {}
        output["emb"] = {}
        output["embs"] = []
        feature = []
        _fbank_list = []
        for _data in data_list:
            fbank = self._fbank(_data) # shape=(1,num_frames,num_mels)
            _fbank_list.append(fbank)
            if not self.mean and len(_fbank_list) > 0:
                break
            elif len(_fbank_list) >= self.max_split_num:
                break
        logger.info(f"[Lite] encode: {len(_fbank_list)} segments, mean: {self.mean}")
        for _index, now_session in enumerate(self.sv_sessions): 
            now_model_name = self.sv_model_names[_index]
            if self.mean:
                embs = []
                for fbank in _fbank_list:
                    emb = self._encode_by_session(fbank, now_session)
                    embs.append(emb)
                embs = np.array(embs) # shape=(num_segments,num_dims)
                emb = embs.mean(axis=0) # shape=(num_dims)
                emb = emb / np.linalg.norm(emb)
                output["emb"][now_model_name] = emb
                feature.append(emb)
                output["embs"].append(emb)
            else:
                fbank = _fbank_list[0] # shape=(1,num_frames,num_mels)
                emb = self._encode_by_session(fbank, now_session) # shape=(num_dims)
                output["emb"][now_model_name] = emb
                feature.append(emb)
        output["feature"] = np.concatenate(feature).reshape(-1)
        output["feature"] = output["feature"] / np.linalg.norm(output["feature"])
        if self.mean:
            return output
        return {
            "emb": output["emb"],
            "feature": output["feature"]
        }

    def vad_file(self, wav_path):
        # Accepts: wav_path (str)
        # Perform Voice Activity Detection (VAD) on audio file
        # Return: result (Dict)
        data = self._load_file(wav_path)
        segments, data = self._vad(data) # List[Dict], shape=(num_samples)
        return {
            "pcm": data,
            "segments": segments,
            "sample_rate": self.sample_rate,
        }

    def cosine_similarity(self, e1, e2):
        if isinstance(e1, dict) and isinstance(e2, dict):
            assert len(e1) == len(e2), "Length of embeddings should be the same"
            if "emb" in e1:
                e1 = e1["emb"]
            if "emb" in e2:
                e2 = e2["emb"]
            scores = []
            for model_name in e1.keys():
                assert model_name in e2, f"Model {model_name} not found in e2"
                e1_now = e1[model_name]
                e2_now = e2[model_name]
                if not isinstance(e1_now, torch.Tensor):
                    e1_now = torch.tensor(e1_now)
                if not isinstance(e2_now, torch.Tensor):
                    e2_now = torch.tensor(e2_now)
                assert e1_now.shape == e2_now.shape, f"Shape of {model_name} should be the same"
                cosine_score = torch.dot(e1_now.reshape(-1), e2_now.reshape(-1))
                cosine_score = cosine_score.item()
                scores.append(cosine_score)
            mean_scores = sum(scores) / len(scores)
            logger.info(f"[Lite] cosine_similarity: Get mean cosine similarity: {mean_scores} from {scores}")
            return (mean_scores + 1)/2
        assert e1.shape == e2.shape
        # if is numpy -> torch
        if not isinstance(e1, torch.Tensor):
            e1 = torch.tensor(e1)
        if not isinstance(e2, torch.Tensor):
            e2 = torch.tensor(e2)
        score = torch.dot(e1.reshape(-1), e2.reshape(-1))
        score = score.item()
        return (score + 1)/2

    def extract_embedding_feats(self, fbanks, batch_size, subseg_cmn):
        fbanks_array = np.stack(fbanks)
        if subseg_cmn:
            fbanks_array = fbanks_array - np.mean(fbanks_array, axis=1, keepdims=True)
        embeddings = []
        for i in range(0, fbanks_array.shape[0], batch_size):
            batch_feats = fbanks_array[i : i + batch_size]
            batch_embs = self.session.run(
                input_feed={self.session.get_inputs()[0].name: batch_feats}, output_names=[self.session.get_outputs()[0].name]
            )[0].squeeze()
            batch_embs = batch_embs[-1] if isinstance(batch_embs, tuple) else batch_embs
            embeddings.append(batch_embs)
        embeddings = np.vstack(embeddings)
        return embeddings

    def _diarize(self, vad_segments, pcm, utt: str = "dguard"):
        pcm = torch.from_numpy(pcm).to(self.device)
        pcm = pcm.reshape(1, -1)
        subsegs, subseg_fbanks = [], []
        window_fs = int(self.diar_window_secs * 1000) // self.diar_frame_shift
        period_fs = int(self.diar_period_secs * 1000) // self.diar_frame_shift
        split_num = 0
        for _, item in enumerate(vad_segments):
            try:
                begin, end = item["start"], item["end"]
                if end - begin >= self.diar_min_duration:
                    begin_idx = int(begin * self.sample_rate)
                    end_idx = int(end * self.sample_rate)
                    tmp_wavform = pcm[0, begin_idx:end_idx].unsqueeze(0).to(torch.float)
                    fbank = self._fbank(tmp_wavform)
                    tmp_subsegs, tmp_subseg_fbanks = subsegment(
                        fbank=fbank,
                        seg_id="{:08d}-{:08d}".format(
                            int(begin * 1000), int(end * 1000)
                        ),
                        window_fs=window_fs,
                        period_fs=period_fs,
                        frame_shift=self.diar_frame_shift,
                    )
                    subsegs.extend(tmp_subsegs)
                    subseg_fbanks.extend(tmp_subseg_fbanks)
                    split_num += 1
                    if split_num >= self.diar_max_split_num:
                        break
            except Exception as e:
                logger.error(f"[Lite] _diarize Error: {e}")
                continue
        # 3. extract embedding
        embeddings = self.extract_embedding_feats(
            subseg_fbanks, self.diar_batch_size, self.diar_subseg_cmn
        )
        # 4. cluster
        subseg2label = []
        labels = cluster(
            embeddings,
            num_spks=self.diar_num_spks,
            min_num_spks=self.diar_min_num_spks,
            max_num_spks=self.diar_max_num_spks,
        )
        for _subseg, _label in zip(subsegs, labels):
            begin_ms, end_ms, begin_frames, end_frames = _subseg.split("-")
            begin = (int(begin_ms) + int(begin_frames) * self.diar_frame_shift) / 1000.0
            end = (int(begin_ms) + int(end_frames) * self.diar_frame_shift) / 1000.0
            subseg2label.append([begin, end, _label])
        # 5. merged segments
        # [[utt, ([begin, end, label], [])], [utt, ([], [])]]
        merged_segment_to_labels = merge_segments({utt: subseg2label})
        return merged_segment_to_labels

    def diarize(self, wav_path):
        vad_result = self.vad_file(wav_path)
        diar_result = self._diarize(vad_result["segments"], vad_result["pcm"])
        return diar_result
    
    def _load_data(self, wav_data, sample_rate):
        # assert is npy or tensor and shape is (num_samples,)
        if len(wav_data.shape) == 2:
            if wav_data.shape[0] < self.channel:
                logger.error(f"[Lite] _load_data: No channel {self.channel} in wav_data")
                raise ValueError(f"No channel {self.channel} in wav_data")
            if len(wav_data[self.channel]) < sample_rate*self.start_time:
                logger.error(f"[Lite] _load_data: Audio too short, your audio should be at least {self.start_time} seconds")
                raise ValueError(f"Audio too short, your audio should be at least {self.start_time} seconds")
            if len(wav_data[self.channel]) > sample_rate*MAX_AUDIO_DURATION:
                logger.warning(f"[Lite] _load_data: Audio too long, only use first {MAX_AUDIO_DURATION} seconds")
            if len(wav_data[self.channel]) < sample_rate*MIN_AUDIO_DURATION:
                logger.error(f"[Lite] _load_data: Audio too short, your audio should be at least {self.start_time} seconds")
                raise ValueError(f"Audio too short, your audio should be at least {self.start_time} seconds")
            wav_data = wav_data[self.channel, self.start_time*sample_rate:self.start_time*sample_rate+sample_rate*MAX_AUDIO_DURATION]
        else:
            if len(wav_data) < sample_rate*self.start_time:
                logger.error(f"[Lite] _load_data: Audio too short, your audio should be at least {self.start_time} seconds")
                raise ValueError(f"Audio too short, your audio should be at least {self.start_time} seconds")
            if len(wav_data) > sample_rate*MAX_AUDIO_DURATION:
                logger.warning(f"[Lite] _load_data: Audio too long, only use first {MAX_AUDIO_DURATION} seconds")
            if len(wav_data) < sample_rate*MIN_AUDIO_DURATION:
                logger.error(f"[Lite] _load_data: Audio too short, your audio should be at least {self.start_time} seconds")
                raise ValueError(f"Audio too short, your audio should be at least {self.start_time} seconds")
            wav_data = wav_data[self.start_time*sample_rate:self.start_time*sample_rate+sample_rate*MAX_AUDIO_DURATION]
        if sample_rate != self.sample_rate:
            if isinstance(wav_data, np.ndarray):
                wav_data_resample = torch.from_numpy(wav_data).to(self.device)
                del wav_data
                wav_data = self.resampler_8000(wav_data_resample).view(1,-1)
                del wav_data_resample
            else:
                wav_data = self.resampler_8000(wav_data.to(self.device)).view(1,-1)
        if isinstance(wav_data, np.ndarray):
            wav_data = torch.from_numpy(wav_data).view(-1)
        else:
            if not isinstance(wav_data, torch.Tensor):
                logger.error(f"[Lite] _load_data: wav_data should be np.ndarray or torch.Tensor")
                raise ValueError("wav_data should be np.ndarray or torch.Tensor")
            else:
                wav_data = wav_data.view(-1)
        return wav_data

    def vad_data(self, wav_data, sample_rate):
        wav_data = self._load_data(wav_data, sample_rate)
        segments, data = self._vad(wav_data) # List[Dict], shape=(num_samples)
        return {
            "pcm": data,
            "segments": segments,
            "sample_rate": self.sample_rate,
        }

    def encode_data(self, wav_data, sample_rate, apply_vad=False):
        if apply_vad:
            segments, data = self.vad_data(wav_data, sample_rate)
        else:
            if self.apply_vad:
                segments, data = self._vad(wav_data, sample_rate)
            else:
                data = self._load_data(wav_data, sample_rate)
        if not isinstance(data, torch.Tensor):
            data = torch.from_numpy(data)
        data_list = self._split_data(data, self.sv_pad_data_to_length) # List[Tensor, shape=(1,num_samples)]
        output = {}
        output["emb"] = {}
        output["embs"] = []
        feature = []
        _fbank_list = []
        for _data in data_list:
            fbank = self._fbank(_data) # shape=(1,num_frames,num_mels)
            _fbank_list.append(fbank)
            if not self.mean and len(_fbank_list) > 0:
                break
            elif len(_fbank_list) >= self.max_split_num:
                break
        logger.info(f"[Lite] encode_data: {len(_fbank_list)} segments, mean: {self.mean}")
        for _index, now_session in enumerate(self.sv_sessions): 
            now_model_name = self.sv_model_names[_index]
            if self.mean:
                embs = []
                for fbank in _fbank_list:
                    emb = self._encode_by_session(fbank, now_session)
                    embs.append(emb)
                embs = np.array(embs) # shape=(num_segments,num_dims)
                emb = embs.mean(axis=0) # shape=(num_dims)
                emb = emb / np.linalg.norm(emb)
                output["emb"][now_model_name] = emb
                feature.append(emb)
                output["embs"].append(emb)
            else:
                fbank = _fbank_list[0] # shape=(1,num_frames,num_mels)
                emb = self._encode_by_session(fbank, now_session) # shape=(num_dims)
                output["emb"][now_model_name] = emb
                feature.append(emb)
        output["feature"] = np.concatenate(feature).reshape(-1)
        output["feature"] = output["feature"] / np.linalg.norm(output["feature"])
        if self.mean:
            return output
        return {
            "emb": output["emb"],
            "feature": output["feature"]
        }

    def diarize_data(self, wav_data, sample_rate):
        vad_result = self.vad_data(wav_data, sample_rate)
        diar_result = self._diarize(vad_result["segments"], vad_result["pcm"])
        return diar_result

    def asv_data(self, wav_data, sample_rate, apply_vad=False):
        if apply_vad:
            vad_result = self.vad_data(wav_data, sample_rate)
            data = vad_result["pcm"]
            data = torch.from_numpy(data).to(self.device)
        else:
            data = self._load_data(wav_data, sample_rate)
        data_list = self._split_data(data, self.spoof_pad_data_to_length) # List[Tensor, shape=(1,num_samples)]
        data = data_list[0] # shape=(1,num_samples)
        fbank = self._fbank(data) # shape=(1,num_frames,num_mels)
        emb = self._asv(fbank) # shape=(num_dims)
        emb = torch.tensor(emb).to(self.device)
        probs = F.softmax(emb, dim=-1)
        pred = torch.argmax(probs, dim=-1)
        # pred = 1 is fake
        label = "fake" if pred.item() == 1 else "real"
        if label == "fake":
            confidence = probs[1].item()
        else:
            confidence = probs[0].item()
        return {"label": label, "score": confidence}
