import streamlit as st
from openai import OpenAI
import time
import base64  # For embedding images

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Set page configuration
st.set_page_config(
    page_title="Sentiment Analyzer Pro with Llama-3 ✨",
    page_icon="🤩",
    layout="wide"  # Use wide layout for more space
)

# --- Background and Styling ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Replace 'background.png' with your background image file
# Ensure you have a background image in the same directory as your script
set_background('background.png')  # You'll need to provide a background image

# --- Custom CSS ---
st.markdown("""
<style>
    [data-testid="stTextArea"] div div textarea {
        border: 4px solid #8A2BE2;  /* Violet border */
        border-radius: 20px;
        padding: 25px;
        font-size: 18px;
        box-shadow: 7px 7px 15px rgba(0, 0, 0, 0.2);
        transition: border 0.3s ease;
    }
    [data-testid="stTextArea"] div div textarea:focus {
        border: 4px solid #9370DB;  /* Medium purple on focus */
    }
    [data-testid="stButton"] button {
        background: linear-gradient(135deg, #663399, #A020F0);  /* Gradient background */
        color: white;
        padding: 18px 30px;
        border: none;
        border-radius: 15px;
        font-size: 20px;
        box-shadow: 5px 5px 12px rgba(0, 0, 0, 0.3);
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stButton"] button:hover {
        transform: translateY(-5px);
        box-shadow: 7px 7px 15px rgba(0, 0, 0, 0.4);
    }
    .result {
        padding: 30px;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.8);  /* Semi-transparent white */
        box-shadow: 7px 7px 15px rgba(0, 0, 0, 0.1);
        margin-top: 30px;
        font-size: 24px;
        text-align: center;
        animation: fadeIn 1s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# --- Main Content ---
st.title("🤩 Sentiment Analyzer Pro with Llama-3 🚀")
st.markdown("Discover the emotion behind your words with advanced AI! 👇")

input_text = st.text_area("✍️ Enter your text here to unveil its sentiment:")

if st.button("✨ Analyze Sentiment ✨"):
    if input_text:
        with st.spinner('Unveiling sentiment... 🌀'):
            completion = client.chat.completions.create(
                model="nvidia/llama-3.1-nemotron-70b-instruct",
                messages=[{"role": "user", "content": f"Please analyze the sentiment... (same prompt)"}],
                temperature=0.5, top_p=1, max_tokens=1024, stream=True
            )
            sentiment = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    sentiment += chunk.choices[0].delta.content.strip()
                    time.sleep(0.05)

        if sentiment.strip():
            sentiment = sentiment.strip().lower()
            if sentiment == "positive":
                result_display = f"🎉 Sentiment: **{sentiment.capitalize()}** 😄"
            elif sentiment == "negative":
                result_display = f"😞 Sentiment: **{sentiment.capitalize()}** 😢"
            else:
                result_display = f"😐 Sentiment: **{sentiment.capitalize()}** 🤔"

            st.markdown(f'<div class="result">{result_display}</div>', unsafe_allow_html=True)
        else:
            st.write("😞 Could not determine sentiment. Please try again.")
    else:
        st.write("📝 Please enter some text to analyze.")

st.markdown("---")
st.markdown("✨ Powered by OpenAI's Llama-3 and Streamlit's magic ✨")
