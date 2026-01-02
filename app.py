"""
Lingo-Voice: Chat GUI with NLLB Translation
A simple translation chat interface powered by Meta's NLLB model
"""

import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

# Page configuration
st.set_page_config(
    page_title="Lingo-Voice",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .chat-message {
        display: flex;
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f0f0;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
    }
    .translator-message {
        background-color: #f3e5f5;
        margin-right: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Language mapping for NLLB
LANGUAGES = {
    "English": "eng_Latn",
    "Spanish": "spa_Latn",
    "French": "fra_Latn",
    "German": "deu_Latn",
    "Chinese (Simplified)": "zho_Hans",
    "Chinese (Traditional)": "zho_Hant",
    "Japanese": "jpn_Jpan",
    "Korean": "kor_Hang",
    "Arabic": "arb_Arab",
    "Hindi": "hin_Deva",
    "Portuguese": "por_Latn",
    "Russian": "rus_Cyrl",
    "Italian": "ita_Latn",
    "Dutch": "nld_Latn",
    "Turkish": "tur_Latn",
    "Vietnamese": "vie_Latn",
    "Thai": "tha_Thai",
    "Polish": "pol_Latn",
    "Swedish": "swe_Latn",
    "Norwegian": "nno_Latn",
}

@st.cache_resource
def load_model():
    """Load NLLB model and tokenizer"""
    try:
        model_name = "facebook/nllb-200-distilled-600M"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

def translate_text(text, source_lang, target_lang, tokenizer, model):
    """Translate text using NLLB"""
    try:
        source_lang_code = LANGUAGES.get(source_lang, "eng_Latn")
        target_lang_code = LANGUAGES.get(target_lang, "spa_Latn")
        
        # Set language tokens
        tokenizer.src_lang = source_lang_code
        inputs = tokenizer(text, return_tensors="pt")
        
        # Generate translation
        with torch.no_grad():
            translated_tokens = model.generate(
                **inputs,
                forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang_code)
            )
        
        translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return translation
    except Exception as e:
        st.error(f"Translation error: {e}")
        return None

# Main UI
st.title("🌍 Lingo-Voice")
st.subheader("Real-time Translation Chat")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False
    st.session_state.tokenizer = None
    st.session_state.model = None

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    source_lang = st.selectbox(
        "Source Language",
        list(LANGUAGES.keys()),
        index=0
    )
    
    target_lang = st.selectbox(
        "Target Language",
        list(LANGUAGES.keys()),
        index=1
    )
    
    if st.button("Load Model", use_container_width=True):
        with st.spinner("Loading NLLB model..."):
            tokenizer, model = load_model()
            if tokenizer and model:
                st.session_state.tokenizer = tokenizer
                st.session_state.model = model
                st.session_state.model_loaded = True
                st.success("✅ Model loaded successfully!")
            else:
                st.error("Failed to load model")
    
    if st.session_state.model_loaded:
        st.info("✅ Model is ready for translation")
    else:
        st.warning("⚠️ Click 'Load Model' to start translating")
    
    # Clear chat history
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Chat interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"📝 {source_lang}")
    user_input = st.text_area(
        "Type your message",
        height=100,
        key="user_input",
        label_visibility="collapsed"
    )

with col2:
    st.subheader(f"🗣️ {target_lang}")
    translation_output = st.empty()

# Translation button
if st.button("Translate", use_container_width=True, type="primary"):
    if not st.session_state.model_loaded:
        st.error("❌ Please load the model first!")
    elif not user_input.strip():
        st.error("❌ Please enter some text to translate")
    else:
        with st.spinner("Translating..."):
            translation = translate_text(
                user_input,
                source_lang,
                target_lang,
                st.session_state.tokenizer,
                st.session_state.model
            )
            
            if translation:
                # Store in session
                st.session_state.messages.append({
                    "source": source_lang,
                    "target": target_lang,
                    "original": user_input,
                    "translation": translation
                })
                
                # Display translation
                translation_output.text_area(
                    "Translation",
                    value=translation,
                    height=100,
                    disabled=True,
                    label_visibility="collapsed"
                )
                st.success("✅ Translation complete!")

# Chat history
if st.session_state.messages:
    st.divider()
    st.subheader("📚 Chat History")
    
    for i, msg in enumerate(st.session_state.messages):
        with st.container():
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f"**{msg['source']}**")
                st.text(msg['original'])
            
            with col2:
                st.markdown(f"**{msg['target']}**")
                st.text(msg['translation'])
            
            st.divider()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.8rem;'>
    <p>Powered by <strong>NLLB-200 (Meta)</strong> | Support 200+ Languages</p>
    <p>Lingo-Voice © 2025 | Licensed under AGPL-3.0 or Commercial</p>
    </div>
""", unsafe_allow_html=True)
