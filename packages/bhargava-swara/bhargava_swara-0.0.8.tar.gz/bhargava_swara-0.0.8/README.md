```markdown
# Bhargava Swara

A Python library for analyzing and visualizing Indian classical music, including spectrogram generation (Mel-frequency, Chroma, CQT, and Cent filterbank), raga, tala, tempo, tradition, ornaments, and full analysis.

## Prerequisites

- **Gemini API Key:**  
  This library uses Google's Gemini API for music analysis. To obtain a key:  
  1. Sign up for a Google Cloud account  
  2. Enable the Generative AI API in the Google Cloud Console  
  3. Create an API key in the "Credentials" section  
  Refer to [Google's Generative AI Docs](https://cloud.google.com/generative-ai/docs) for details

- **Audio Files:**  
  Supported formats include WAV and MP3 for analysis and spectrogram generation

## Installation

Install the library using pip:

```sh
pip install bhargava_swara
```

## Dependencies

- `google-generativeai>=0.1.0`  
- `librosa>=0.10.0`  
- `matplotlib>=3.7.0`  
- `numpy>=1.24.0`

## Spectrogram Generation

Generate various types of spectrograms to visualize different aspects of audio frequency content over time.

### Mel-Frequency Spectrogram
```python
from bhargava_swara import generate_mel_spectrogram

audio = "path/to/audio.wav"
output = "path/to/output_mel_spectrogram.png"
generate_mel_spectrogram(audio, output, n_mels=128, fmax=8000)
print("Mel spectrogram generated successfully!")
```

### Chroma Spectrogram
```python
from bhargava_swara import generate_chroma_spectrogram

audio = "path/to/audio.wav"
output = "path/to/output_chroma_spectrogram.png"
generate_chroma_spectrogram(audio, output, n_chroma=12, hop_length=512)
print("Chroma spectrogram generated successfully!")
```

### CQT Spectrogram
```python
from bhargava_swara import generate_cqt_spectrogram

audio = "path/to/audio.wav"
output = "path/to/output_cqt_spectrogram.png"
generate_cqt_spectrogram(audio, output, hop_length=512, n_bins=84)
print("CQT spectrogram generated successfully!")
```

### Cent Filterbank Spectrogram
```python
from bhargava_swara import generate_cent_spectrogram

audio = "path/to/audio.wav"
output = "path/to/output_cent_spectrogram.png"
generate_cent_spectrogram(audio, output, n_filters=128, fmax=8000)
print("Cent filterbank spectrogram generated successfully!")
```

#### Spectrogram Parameters:
- `audio`: Path to the input audio file (e.g., WAV or MP3)
- `output`: Path to save the PNG file
- Mel-specific: `n_mels` (default: 128), `fmax` (default: 8000)
- Chroma-specific: `n_chroma` (default: 12), `hop_length` (default: 512)
- CQT-specific: `hop_length` (default: 512), `n_bins` (default: 84)
- Cent-specific: `n_filters` (default: 128), `fmax` (default: 8000)

## Music Analysis

Analyze various aspects of Indian classical music using the Gemini API.

### Raga Analysis
```python
from bhargava_swara import analyze_raga

api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"
result = analyze_raga(audio, api_key)
print(f"Raga: {result}")
```

### Tala Analysis
```python
from bhargava_swara import analyze_tala

api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"
result = analyze_tala(audio, api_key)
print(f"Tala: {result}")
```

### Tempo Analysis
```python
from bhargava_swara import analyze_tempo

api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"
result = analyze_tempo(audio, api_key)
print(f"Tempo: {result}")
```

### Tradition Analysis
```python
from bhargava_swara import analyze_tradition

api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"
result = analyze_tradition(audio, api_key)
print(f"Tradition: {result}")
```

### Ornament Analysis
```python
from bhargava_swara import analyze_ornaments

api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"
result = analyze_ornaments(audio, api_key)
print(f"Ornaments: {result}")
```

### Full Music Analysis
```python
from bhargava_swara import analyze_music_full

api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"
result = analyze_music_full(audio, api_key)
print(f"Full Analysis:\n{result}")
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue on the GitHub repository (if available).

## License

This library is licensed under the MIT License. See the `LICENSE` file for details.
```
