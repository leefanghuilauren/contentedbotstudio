# 🎬 ContentedBot Studio

A fully offline, data-driven video generation pipeline. Build characters, pick scenes,
clone your voice, animate lips, and auto-generate videos from your own datasets.

---

## 🚀 Quick Start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install & start Ollama

```bash
# Install (Mac/Linux)
curl -fsSL https://ollama.com/install.sh | sh

ollama pull llama3   # or mistral, gemma2, etc.
ollama serve
```

### 3. Install FFmpeg

```bash
brew install ffmpeg          # Mac
sudo apt install ffmpeg      # Ubuntu/Debian
```

### 4. Install a lip sync backend (pick one)

#### Option A — SadTalker *(CPU-friendly, portrait → talking head)*

```bash
git clone https://github.com/OpenTalker/SadTalker lib/SadTalker
cd lib/SadTalker
pip install -r requirements.txt
bash scripts/download_models.sh
```

#### Option B — Wav2Lip *(fastest, needs GPU)*

```bash
git clone https://github.com/Rudrabha/Wav2Lip lib/Wav2Lip
cd lib/Wav2Lip
pip install -r requirements.txt
# Download wav2lip_gan.pth into lib/Wav2Lip/checkpoints/
# https://github.com/Rudrabha/Wav2Lip#getting-the-weights
```

#### Option C — LatentSync *(best quality, ~10 GB VRAM)*

```bash
git clone https://github.com/bytedance/LatentSync lib/LatentSync
cd lib/LatentSync
pip install -r requirements.txt
python -m scripts.download_models
```

### 5. Run the app

```bash
cd video_agent
streamlit run app.py
```

---

## 🔄 Full Pipeline

```
Your Dataset (CSV / JSON)
        │
        ▼
  Ollama LLM  ──────────►  Script (.txt)
        │
        ▼
  Coqui TTS  ───────────►  Cloned Voice (.wav)
        │
        ▼
  Lip Sync Engine         Avatar Image (.png)
  SadTalker / Wav2Lip  ►  Animated Avatar (.mp4)
  LatentSync
        │
        ▼
  FFmpeg  ──────────────►  Final Video (.mp4)
  (avatar + scene + audio)
```

---

## 📁 Project Structure

```
video_agent/
├── app.py                       # Streamlit app + navigation
├── pages/
│   ├── home.py                  # Dashboard
│   ├── character_builder.py     # RPG character creator
│   ├── scene_selector.py        # Background picker
│   ├── voice_profile.py         # Voice clone manager
│   ├── lip_sync_settings.py     # Lip sync config + avatar upload  ← NEW
│   ├── context_packs.py         # Domain context loader
│   ├── dataset.py               # Dataset upload + field mapping
│   ├── generate.py              # Generation launcher (lip sync toggle)
│   └── my_videos.py             # Video gallery + downloads
├── pipeline/
│   ├── script_generator.py      # Ollama → scripts
│   ├── voice_synthesizer.py     # Coqui TTS → voice cloning
│   ├── lip_sync.py              # SadTalker / Wav2Lip / LatentSync  ← NEW
│   ├── video_assembler.py       # FFmpeg → final video
│   └── batch_runner.py          # Full pipeline orchestration
├── lib/
│   ├── SadTalker/               # Clone here (git clone …)
│   ├── Wav2Lip/                 # Clone here
│   └── LatentSync/              # Clone here
├── assets/
│   ├── avatars/                 # Character portrait images
│   ├── scenes/                  # Custom backgrounds
│   └── voices/                  # Voice clips
├── data/                        # JSON configs + dataset
├── outputs/                     # Generated videos
│   └── lipsync/                 # Intermediate animated avatars
└── requirements.txt
```

---

## 👄 Lip Sync Backends Comparison

| Backend     | Quality   | Speed  | GPU Needed | Best For |
|-------------|-----------|--------|------------|----------|
| SadTalker   | ⭐⭐⭐     | ⚡⚡    | Optional   | Portrait image → talking head |
| Wav2Lip     | ⭐⭐⭐     | ⚡⚡⚡  | Yes        | Existing video → re-synced |
| LatentSync  | ⭐⭐⭐⭐⭐  | ⚡      | Yes (~10GB)| Highest quality, temporal consistency |

**Recommendation:** Start with SadTalker (no GPU needed). Upgrade to LatentSync when you need broadcast quality.

---

## 👥 Multi-User Deployment

### Local network
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### Docker
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg git
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```
```bash
docker build -t videoagent .
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/lib:/app/lib \
  videoagent
```

---

## 🗺️ Roadmap

- [x] Character builder
- [x] Scene selector
- [x] Voice cloning (Coqui TTS)
- [x] Lip sync (SadTalker / Wav2Lip / LatentSync)
- [x] Data-driven batch generation
- [ ] Auto-captions (Whisper)
- [ ] Avatar image generation (Stable Diffusion)
- [ ] Supabase cloud storage
- [ ] User auth (multi-tenant)
- [ ] Video templates / presets
