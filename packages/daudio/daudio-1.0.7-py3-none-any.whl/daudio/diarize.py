# coding = utf-8
# @Time    : 2025-03-12  17:13:40
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Diarize.

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('daudio')
logger.setLevel(logging.INFO)

import torchaudio # torchaudio should be imported before torch
import torch
try:
    import torch_npu
    from torch_npu.contrib import transfer_to_npu
except Exception as e:
    logger.error("[ERROR] torch_npu not found, please install it first.")
    logger.error("[ERROR] if you are not using NPU, please ignore.")
import os
import numpy as np
import scipy.linalg
from torchaudio.compliance import kaldi
from sklearn.cluster._kmeans import k_means

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

def merge_segments(utt_to_subseg_labels):
    merged_segment_to_labels = []
    for utt, subseg_to_labels in utt_to_subseg_labels.items():
        if len(subseg_to_labels) == 0:
            continue
        (begin, end, label) = subseg_to_labels[0]
        e = end  # when there is only one subseg, we assign end to e
        for (b, e, la) in subseg_to_labels[1:]:
            if b <= end and la == label:
                end = e
            elif b > end:
                merged_segment_to_labels.append((utt, begin, end, label))
                begin, end, label = b, e, la
            elif b <= end and la != label:
                pivot = (b + end) / 2.0
                merged_segment_to_labels.append((utt, begin, pivot, label))
                begin, end, label = pivot, e, la
            else:
                raise ValueError
        merged_segment_to_labels.append((utt, begin, e, label))
    return merged_segment_to_labels

def cluster(embeddings, p=0.01, num_spks=None, min_num_spks=1, max_num_spks=20):
    # Define utility functions
    def cosine_similarity(M):
        M = M / np.linalg.norm(M, axis=1, keepdims=True)
        return 0.5 * (1.0 + np.dot(M, M.T))
    def prune(M, p):
        m = M.shape[0]
        if m < 1000:
            n = max(m - 10, 2)
        else:
            n = int((1.0 - p) * m)
        for i in range(m):
            indexes = np.argsort(M[i, :])
            low_indexes, high_indexes = indexes[0:n], indexes[n:m]
            M[i, low_indexes] = 0.0
            M[i, high_indexes] = 1.0
        return 0.5 * (M + M.T)
    def laplacian(M):
        M[np.diag_indices(M.shape[0])] = 0.0
        D = np.diag(np.sum(np.abs(M), axis=1))
        return D - M
    def spectral(M, num_spks, min_num_spks, max_num_spks):
        eig_values, eig_vectors = scipy.linalg.eigh(M)
        num_spks = (
            num_spks
            if num_spks is not None
            else np.argmax(np.diff(eig_values[: max_num_spks + 1])) + 1
        )
        num_spks = max(num_spks, min_num_spks)
        return eig_vectors[:, :num_spks]
    def kmeans(data):
        k = data.shape[1]
        # centroids, labels = scipy.cluster.vq.kmeans2(data, k, minit='++')
        _, labels, _ = k_means(data, k, random_state=None, n_init=10)
        return labels
    # Fallback for trivial cases
    if len(embeddings) <= 2:
        return [0] * len(embeddings)
    # Compute similarity matrix
    similarity_matrix = cosine_similarity(np.array(embeddings))
    # Prune matrix with p interval
    pruned_similarity_matrix = prune(similarity_matrix, p)
    # Compute Laplacian
    laplacian_matrix = laplacian(pruned_similarity_matrix)
    # Compute spectral embeddings
    spectral_embeddings = spectral(
        laplacian_matrix, num_spks, min_num_spks, max_num_spks
    )
    # Assign class labels
    labels = kmeans(spectral_embeddings)
    return labels

def subsegment(fbank, seg_id, window_fs, period_fs, frame_shift):
    subsegs = []
    subseg_fbanks = []
    seg_begin, seg_end = seg_id.split("-")[-2:]
    seg_length = (int(seg_end) - int(seg_begin)) // frame_shift
    # We found that the num_frames + 2 equals to seg_length, which is caused
    # by the implementation of torchaudio.compliance.kaldi.fbank.
    # Thus, here seg_length is used to get the subsegs.
    fbank = fbank.squeeze(0).cpu().numpy()
    num_frames, feat_dim = fbank.shape
    if seg_length <= window_fs:
        subseg = seg_id + "-{:08d}-{:08d}".format(0, seg_length)
        subseg_fbank = np.resize(fbank, (window_fs, feat_dim))
        subsegs.append(subseg)
        subseg_fbanks.append(subseg_fbank)
    else:
        max_subseg_begin = seg_length - window_fs + period_fs
        for subseg_begin in range(0, max_subseg_begin, period_fs):
            subseg_end = min(subseg_begin + window_fs, seg_length)
            subseg = seg_id + "-{:08d}-{:08d}".format(subseg_begin, subseg_end)
            subseg_fbank = np.resize(
                fbank[subseg_begin:subseg_end], (window_fs, feat_dim)
            )
            subsegs.append(subseg)
            subseg_fbanks.append(subseg_fbank)
    return subsegs, subseg_fbanks
