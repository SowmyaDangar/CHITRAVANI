# app.py - Chitra Vani (full-page gradient, adaptive, clean UI)
import streamlit as st
from PIL import Image
import io, sys, os

# --- make sure src is importable ---
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.utils import make_payload, b64_to_bytes
from src.hf_dataset import push_file

# --- page config ---
st.set_page_config(page_title="🪷 Chitra Vani", page_icon="🌈", layout="wide")

# --- full-page gradient background and styles ---
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        height: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #FFD3E0, #FDE2FF, #C8F1FF, #D1FFD4, #FFFACD) !important;
        background-size: 400% 400%;
        animation: gradientBG 30s ease infinite;
    }
    @keyframes gradientBG {
        0% {background-position:0% 50%;}
        50% {background-position:100% 50%;}
        100% {background-position:0% 50%;}
    }

    .stApp, .main, .block-container {
        background: transparent !important;
    }

    .stButton button {
        background: linear-gradient(90deg, #a1c4fd, #c2e9fb);
        color: #333;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        border: none;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        font-weight: bold;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #c2e9fb, #a1c4fd);
    }

    h1, h2, h3 {
        font-weight: 600;
        color: #1e1b4b;
    }

    hr {
        border: 1px solid rgba(30,27,75,0.3);
        margin: 1rem 0;
    }

    @media only screen and (max-width: 768px) {
        body, .main {
            padding: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --- title ---
st.markdown("<h1 style='text-align: center;'>🌈 Chitra Vani</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Bring your images and videos to life with your words.</p>", unsafe_allow_html=True)

# --- initialize session state ---
if "queue" not in st.session_state:
    st.session_state.queue = []
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "uploaded_video" not in st.session_state:
    st.session_state.uploaded_video = None

# ---------------- Image Upload ----------------
st.subheader("📷 Upload Image")
uploaded_img = st.file_uploader("Upload an image (png/jpg)", type=["png","jpg","jpeg"])
if uploaded_img:
    st.session_state.uploaded_image = uploaded_img

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- Video Upload ----------------
st.subheader("🎬 Upload Short Video (optional)")
uploaded_vid = st.file_uploader("Upload a video (mp4, webm, mov)", type=["mp4","webm","mov"])
if uploaded_vid:
    st.session_state.uploaded_video = uploaded_vid

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- Caption & Metadata ----------------
st.subheader("✏️ Add Caption & Info")
caption = st.text_area("Write caption / proverb / description:", height=120, placeholder="Type your caption here...")
language = st.selectbox("Language", ["","hi","bn","ta","te","kn","ml","gu","pa","en"])
region = st.text_input("Region (optional, e.g., IN-UP)")
category = st.selectbox("Category", ["meme","proverb","song","story","other"])
license_choice = st.selectbox("License", ["CC-BY-4.0","CC0-1.0"])

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- Preview ----------------
st.subheader("👁 Preview")
if st.session_state.uploaded_image:
    st.image(Image.open(st.session_state.uploaded_image))
else:
    st.info("No image uploaded yet.")

if st.session_state.uploaded_video:
    st.video(st.session_state.uploaded_video)
else:
    st.info("No video uploaded yet.")

st.write("**Caption preview:**", caption if caption else "— type caption above —")

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- Save ----------------
if st.button("💾 Submit Content"):
    if not (st.session_state.uploaded_image or st.session_state.uploaded_video):
        st.error("Please upload an image or video first.")
    else:
        if st.session_state.uploaded_video:
            payload = make_payload(st.session_state.uploaded_video.read(), "video", caption, language, region, category, license_choice)
        else:
            payload = make_payload(st.session_state.uploaded_image.read(), "image", caption, language, region, category, license_choice)
        st.session_state.queue.append(payload)
        st.success(f"✅ Saved! Queue length: {len(st.session_state.queue)}")
