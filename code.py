import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Streamlit App UI
st.set_page_config(page_title="Sentiment Analyzer", page_icon="🧠", layout="wide")

# Header Section
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4A90E2;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #7F8C8D;
        text-align: center;
        margin-bottom: 30px;
    }
    .textarea-box {
        background-color: #F8F9F9;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #D6DBDF;
    }
    .analyze-button {
        background-color: #4A90E2;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 1rem;
        font-weight: bold;
        cursor: pointer;
    }
    .analyze-button:hover {
        background-color: #007BFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-header">Sentiment Analysis with Llama-3.1 Nemotron 🧠</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analyze the sentiment of your text with the power of AI!</div>', unsafe_allow_html=True)

# Input Section
st.markdown("### 📝 Enter your text below:")
input_text = st.text_area("", "", placeholder="Type something here...", height=150, label_visibility="collapsed")

# Analyze Button
if st.button("🚀 Analyze Sentiment", key="analyze"):
    if input_text.strip():
        with st.spinner("Analyzing sentiment... 🚧"):
            try:
                # Modify the prompt to ensure the model responds as required
                completion = client.chat.completions.create(
                    model="nvidia/llama-3.1-nemotron-70b-instruct",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Please analyze the sentiment of the following text and no matter what, respond with only one word: 'Positive', 'Negative', or 'Neutral'. Text: '{input_text}'"
                        }
                    ],
                    temperature=0.5,
                    top_p=1,
                    max_tokens=1024,
                    stream=True
                )

                sentiment = ""  # Variable to accumulate the sentiment result
                for chunk in completion:
                    # Ensure that content exists in the chunk and accumulate
                    if chunk.choices[0].delta.content:
                        sentiment += chunk.choices[0].delta.content.strip()

                # Display the result
                if sentiment.strip():
                    sentiment = sentiment.strip().capitalize()
                    emoji = "😊" if sentiment == "Positive" else "😟" if sentiment == "Negative" else "😐"
                    st.success(f"**Sentiment: {sentiment} {emoji}**")
                else:
                    st.warning("Could not determine sentiment. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text to analyze.")

# Footer Section
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #95A5A6; font-size: 0.9rem;">
        Built with ❤️ using <strong>Streamlit</strong> and <strong>Llama-3.1 Nemotron</strong>.
    </div>
    """,
    unsafe_allow_html=True
)
