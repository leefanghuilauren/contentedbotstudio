import streamlit as st
import os
import subprocess
import json

# ── 1. Page Configuration ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="ContentedBot Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 2. Custom Branding Styles ──────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(90deg, #6C63FF, #FF6584);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0rem;
    }
    .sub-header { 
        color: #888; 
        font-size: 1.1rem; 
        margin-bottom: 2rem; 
        font-style: italic;
    }
    .card {
        background: #1e1e2e; border-radius: 12px; padding: 1.5rem;
        margin-bottom: 1rem; border: 1px solid #2e2e3e;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6C63FF, #FF6584);
        color: white; border: none; border-radius: 8px;
        padding: 0.5rem 2rem; font-weight: 600; width: 100%;
    }
    .stButton>button:hover { opacity: 0.9; transform: translateY(-1px); }
</style>
""", unsafe_allow_html=True)

# ── 3. Main Header Branding ───────────────────────────────────────────────────
st.markdown('<div class="main-header">ContentedBot Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Digital Transformation through AI Video Synthesis</div>', unsafe_allow_html=True)

# ── 4. Optimized Pipeline Status Logic ────────────────────────────────────────
@st.cache_resource(ttl=300)  # Cache for 5 mins to prevent UI lag
def check_pipeline_status():
    def _ok(cmd):
        try:
            # Increased timeout to 5s to account for system load
            return subprocess.run(cmd, capture_output=True, timeout=5).returncode == 0
        except Exception:
            return False

    results = {
        "ollama": _ok(["curl", "-sf", "http://localhost:11434"]),
        "tts": _ok(["tts", "--version"]),
        "ffmpeg": _ok(["ffmpeg", "-version"]),
        "whisper": False
    }

    # Internal import check for Whisper
    try:
        import whisper
        results["whisper"] = True
    except ImportError:
        try:
            from faster_whisper import WhisperModel
            results["whisper"] = True
        except ImportError:
            results["whisper"] = False
            
    return results

# ── 5. Sidebar Navigation & Status ───────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎬 ContentedBot Studio")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "🏠 Home",
            "👤 Character Builder",
            "🎨 Scene Selector",
            "🎙️ Voice Profile",
            "👄 Lip Sync",
            "💬 Auto-Captions",
            "📚 Context Packs",
            "📊 My Dataset",
            "🎬 Generate Video",
            "📁 My Videos",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**Pipeline Status**")

    # Run the cached status check
    status = check_pipeline_status()

    # Lip sync configuration check
    ls_cfg = {}
    if os.path.exists("data/lipsync_config.json"):
        with open("data/lipsync_config.json") as f:
            ls_cfg = json.load(f)
    
    ls_backend = ls_cfg.get("backend", "sadtalker")
    ls_dir_map = {
        "sadtalker": "lib/SadTalker",
        "wav2lip": "lib/Wav2Lip",
        "latentsync": "lib/LatentSync"
    }
    lipsync_ok = os.path.exists(ls_dir_map.get(ls_backend, ""))
    ls_label = ls_backend.title() if ls_cfg.get("enabled", True) else "OFF"

    # Status Display Grid
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"{'🟢' if status['ollama']  else '🔴'} Ollama")
        st.markdown(f"{'🟢' if status['tts']     else '🔴'} Coqui TTS")
        st.markdown(f"{'🟢' if status['whisper'] else '🟡'} Whisper")
    with col2:
        st.markdown(f"{'🟢' if status['ffmpeg']  else '🔴'} FFmpeg")
        st.markdown(f"{'🟢' if lipsync_ok       else '🟡'} {ls_label}")

    st.markdown("---")
    st.caption("ContentedBot Studio v0.3 · 🇸🇬 Singapore")

# ── 6. Routing Logic ──────────────────────────────────────────────────────────
# Mapping pages to their respective render functions
if page == "🏠 Home":
    from pages import home; home.render()
elif page == "👤 Character Builder":
    from pages import character_builder; character_builder.render()
elif page == "🎨 Scene Selector":
    from pages import scene_selector; scene_selector.render()
elif page == "🎙️ Voice Profile":
    from pages import voice_profile; voice_profile.render()
elif page == "👄 Lip Sync":
    from pages import lip_sync_settings; lip_sync_settings.render()
elif page == "💬 Auto-Captions":
    from pages import captions_settings; captions_settings.render()
elif page == "📚 Context Packs":
    from pages import context_packs; context_packs.render()
elif page == "📊 My Dataset":
    from pages import dataset; dataset.render()
elif page == "🎬 Generate Video":
    from pages import generate; generate.render()
elif page == "📁 My Videos":
    from pages import my_videos; my_videos.render()