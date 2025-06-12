import soundfile as sf
from kimia_infer.api.kimia import KimiAudio

# --- 1. Load Model ---
model_path = "moonshotai/Kimi-Audio-7B-Instruct" 
model = KimiAudio(model_path=model_path, load_detokenizer=True)

# --- 2. Define Sampling Parameters ---
sampling_params = {
    "audio_temperature": 0.8,
    "audio_top_k": 10,
    "text_temperature": 0.0,
    "text_top_k": 5,
    "audio_repetition_penalty": 1.0,
    "audio_repetition_window_size": 64,
    "text_repetition_penalty": 1.0,
    "text_repetition_window_size": 16,
}

# --- 3. Example 1: Audio-to-Text (ASR) ---
messages_asr = [
    # You can provide context or instructions as text
    {"role": "user", "message_type": "text", "content": "Please transcribe the following audio:"},
    # Provide the audio file path
    {"role": "user", "message_type": "audio", "content": "test_audios/asr_example.wav"}
]

# Generate only text output
_, text_output = model.generate(messages_asr, **sampling_params, output_type="text")
print(">>> ASR Output Text: ", text_output) # Expected output: "这并不是告别，这是一个篇章的结束，也是新篇章的开始。"

