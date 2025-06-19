from transformers import Wav2Vec2Model, Wav2Vec2Processor
import torch
import librosa
import numpy as np
import io

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h")

def get_embedding(audio, sr=16000):
    if sr != 16000:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)

    inputs = processor(audio, return_tensors="pt", sampling_rate=16000).input_values
    with torch.no_grad():
        outputs = model(inputs).last_hidden_state.mean(dim=1)
    return outputs.squeeze().numpy()

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def compute_similarity_from_files(user_audio_file, ref_audio_file):
    y1, sr1 = librosa.load(io.BytesIO(user_audio_file.read()), sr=None)
    y2, sr2 = librosa.load(io.BytesIO(ref_audio_file.read()), sr=None)

    emb1 = get_embedding(y1, sr1)
    emb2 = get_embedding(y2, sr2)

    return cosine_similarity(emb1, emb2)
