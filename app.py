import streamlit as st
import time
import sys
import os

# Add project root to sys.path to allow importing from src
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.rag_pipeline import RAGPipeline

# --- Page Configuration ---
st.set_page_config(
    page_title="CrediTrust Analyst AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS for "Fancy" UI ---
st.markdown("""
<style>
    /* Main Background & Text */
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    
    /* Chat Message Container styling */
    .stChatMessage {
        background-color: #1a1c24;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* User Message Specifics */
    div[data-testid="stChatMessageContent"] {
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }

    /* Header Styling */
    h1 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 20px;
        border-bottom: 1px solid #333;
        margin-bottom: 30px;
    }

    /* Expander Styling for Sources */
    .streamlit-expanderHeader {
        font-family: 'Roboto Mono', monospace;
        color: #FF914D;
        font-weight: bold;
    }
    
    /* Spinner customization */
    .stSpinner > div {
        border-top-color: #FF4B4B !important;
    }

    /* Input Box styling */
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #ffffff;
        border-radius: 10px;
        border: 1px solid #444;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FF4B4B;
        box-shadow: 0 0 5px rgba(255, 75, 75, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize RAG Pipeline (Cached) ---
@st.cache_resource
def load_rag_pipeline():
    return RAGPipeline()

try:
    rag_pipeline = load_rag_pipeline()
except Exception as e:
    st.error(f"Failed to load RAG Pipeline: {e}")
    st.stop()

# --- Application Header ---
st.title("🤖 CrediTrust Complaint Analyst")
st.markdown("""
<div style='text-align: center; color: #888; margin-bottom: 30px;'>
    <i>Your intelligent assistant for analyzing financial consumer complaints. <br>
    Powered by <b>RAG</b> & <b>Hugging Face Transformers</b>.</i>
</div>
""", unsafe_allow_html=True)

# --- Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander(f"📚 View {len(message['sources'])} Source Documents"):
                for idx, source in enumerate(message["sources"]):
                    st.markdown(f"**Source {idx+1} (ID: `{source['complaint_id']}`)**")
                    st.caption(f"Product: {source['product']}")
                    st.info(source.get('original_text', 'No text available')[:300] + "...")

# --- User Input & Processing ---
if prompt := st.chat_input("Ask about consumer complaints..."):
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate Assistant Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Analyzing complaint database..."):
            try:
                # "Streaming" simulation since local pipeline is fast but synchronous
                answer, sources = rag_pipeline.answer(prompt)
                
                # Simulate streaming for UX
                for chunk in answer.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                
                # 3. Append Sources
                if sources:
                    with st.expander(f"📚 View {len(sources)} Source Documents"):
                        for idx, source in enumerate(sources):
                            st.markdown(f"**Source {idx+1} (ID: `{source['complaint_id']}`)**")
                            st.caption(f"Product: {source['product']}")
                            st.info(source.get('original_text', 'No text available')[:300] + "...")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                answer = "I apologize, but I encountered an error extracting that information."
                sources = []
                message_placeholder.markdown(answer)

    # 4. Save Assistant Message to History
    st.session_state.messages.append({
        "role": "assistant", 
        "content": full_response,
        "sources": sources
    })

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("Clear Chat History", type="primary"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**System Status**")
    st.success("RAG Pipeline Active")
    st.markdown(f"**Model:** `{rag_pipeline.model.name_or_path}`")
    st.markdown("**Vector Store:** `FAISS-CPU`")

