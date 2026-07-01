import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# =====================================================
# Load API Key
# =====================================================
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    st.error("⚠️ GROQ_API_KEY not found in .env file. Please add it.")
    st.stop()

# Initialize Groq Client (OpenAI SDK compatible)
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# =====================================================
# Vedaz System Prompt (Safety Rules)
# =====================================================
SYSTEM_PROMPT = """
आप Vedaz के AI ज्योतिषी हैं। आप वैदिक ज्योतिष (लाहिड़ी अयनांश) के आधार पर करुणामय, संतुलित और गैर-भाग्यवादी मार्गदर्शन देते हैं।
आप कभी मृत्यु, बीमारी या किसी अनहोनी की भविष्यवाणी नहीं करते।
स्वास्थ्य, कानूनी या वित्तीय गंभीर मामलों में योग्य पेशेवर से सलाह लेने को कहते हैं।
उपाय हमेशा सहायक आध्यात्मिक अभ्यास के रूप में बताते हैं, गारंटी के रूप में नहीं।
"""

st.set_page_config(page_title="Vedaz AI Astrologer", page_icon="🔮", layout="wide")

# Sidebar for evaluation results
with st.sidebar:
    st.header("📊 Evaluation Results")
    try:
        import pandas as pd
        df = pd.read_csv("outputs/evaluation.csv")
        st.dataframe(df, use_container_width=True)
    except FileNotFoundError:
        st.info("⚠️ `outputs/evaluation.csv` not found. Run `evaluator.py` first.")

# -----------------------------
# Main Chat Interface
# -----------------------------
st.title("🔮 Vedaz AI Astrologer Chat")
st.caption("Ask your astrological questions safely and honestly.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Apna sawaal poochhiye (e.g., Meri job kab lagegi?)"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call Groq API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Groq's fast and free model
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",   # Groq model
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages
                ],
                temperature=0.7,
                stream=True
            )
            
            # Stream the response
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            if "429" in str(e):
                st.error("🚫 API Rate Limit exceeded! Please wait a few minutes and retry.")
            elif "402" in str(e):
                st.error("💳 Insufficient balance. Please add credits to your Groq account.")
            else:
                st.error(f"An error occurred: {e}")
            full_response = "मुझे माफ़ करें, अभी API कॉल नहीं हो पा रही है। कृपया बाद में पूछें।"
            message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})