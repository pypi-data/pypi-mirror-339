import numpy as np
from scipy.fft import fft
from sklearn.decomposition import PCA

### === Preprocessing === ###
def frackture_preprocess_universal_v2_6(data):
    try:
        if isinstance(data, str):
            vec = np.frombuffer(data.encode("utf-8"), dtype=np.uint8)
        elif isinstance(data, dict):
            flat = str(sorted(data.items()))
            vec = np.frombuffer(flat.encode("utf-8"), dtype=np.uint8)
        elif isinstance(data, bytes):
            vec = np.frombuffer(data, dtype=np.uint8)
        elif isinstance(data, list):
            vec = np.array(data, dtype=np.float32).flatten()
        elif isinstance(data, np.ndarray):
            vec = data.flatten()
        else:
            vec = np.frombuffer(str(data).encode("utf-8"), dtype=np.uint8)
        normed = vec.astype(np.float32)
        normed = (normed - np.min(normed)) / (np.ptp(normed) + 1e-8)
        padded = np.pad(normed, (0, 768 - len(normed) % 768), mode='wrap')
        return padded[:768]
    except Exception as e:
        return np.zeros(768, dtype=np.float32)

### === Symbolic Fingerprinting System === ###
def frackture_symbolic_fingerprint_f_infinity(input_vector, passes=4):
    bits = (input_vector * 255).astype(np.uint8)
    mask = np.array([(i**2 + i*3 + 1) % 256 for i in range(len(bits))], dtype=np.uint8)
    for p in range(passes):
        rotated = np.roll(bits ^ mask, p * 17)
        entropy_mixed = (rotated * ((p + 1) ** 2)) % 256
        chunks = np.array_split(entropy_mixed, 32)
        folded = [np.bitwise_xor.reduce(chunk) for chunk in chunks]
        fingerprint = ''.join(f"{x:02x}" for x in folded)
        bits = (entropy_mixed + folded[p % len(folded)]) % 256
    return fingerprint

def symbolic_channel_encode(input_vector):
    return frackture_symbolic_fingerprint_f_infinity(input_vector)

def symbolic_channel_decode(symbolic_hash):
    decoded = [int(symbolic_hash[i:i+2], 16) / 255.0 for i in range(0, len(symbolic_hash), 2)]
    return np.array((decoded * (768 // len(decoded) + 1))[:768], dtype=np.float32)

### === Entropy Channel System === ###
def entropy_channel_encode(input_vector):
    fft_vector = np.abs(fft(input_vector))
    pca = PCA(n_components=16)
    reduced = pca.fit_transform(fft_vector.reshape(1, -1)).flatten()
    return reduced.tolist()

def entropy_channel_decode(entropy_data):
    ent = np.array(entropy_data)
    expanded = np.tile(ent, 48)[:768]
    normed = (expanded - np.min(expanded)) / (np.ptp(expanded) + 1e-8)
    return normed

### === Reconstruction Combiner === ###
def merge_reconstruction(entropy_vec, symbolic_vec):
    merged = (np.array(entropy_vec) + np.array(symbolic_vec)) / 2
    return merged

### === Core Frackture Compression Functions === ###
def frackture_v3_3_safe(input_vector):
    return {
        "symbolic": symbolic_channel_encode(input_vector),
        "entropy": entropy_channel_encode(input_vector)
    }

def frackture_v3_3_reconstruct(payload):
    entropy_part = entropy_channel_decode(payload["entropy"])
    symbolic_part = symbolic_channel_decode(payload["symbolic"])
    return merge_reconstruction(entropy_part, symbolic_part)

### === Self-Optimization (Decoder Loss Feedback Loop) === ###
def optimize_frackture(input_vector, num_trials=5):
    best_payload = None
    best_mse = float("inf")
    for trial in range(num_trials):
        symbolic = frackture_symbolic_fingerprint_f_infinity(input_vector, passes=trial + 2)
        entropy = entropy_channel_encode(input_vector)
        payload = {"symbolic": symbolic, "entropy": entropy}
        recon = frackture_v3_3_reconstruct(payload)
        mse = np.mean((input_vector - recon) ** 2)
        if mse < best_mse:
            best_mse = mse
            best_payload = payload
    return best_payload, best_mse
