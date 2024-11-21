import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Streamlit UI enhancements
st.set_page_config(page_title="Llama-3 Sentiment Analyzer 🧠", page_icon="🤔")

st.markdown("<h1 style='text-align: center; color: #2E8B57;'>Sentiment Analysis with Llama-3 🚀</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Discover the sentiment of your text using the power of AI!</p>", unsafe_allow_html=True)

input_text = st.text_area("✍️ Enter your text here:", height=200)

if st.button("Analyze Sentiment 🔍"):
    if input_text:
        with st.spinner("Analyzing... ⏳"):
            completion = client.chat.completions.create(
                model="nvidia/llama-3.1-nemotron-70b-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": f"Please analyze the sentiment of the following text and no matter what just respond with only one word: 'Positive', 'Negative', or 'Neutral'. Text: '{input_text}'"
                    }
                ],
                temperature=0.5,
                top_p=1,
                max_tokens=1024,
                stream=True
            )
            sentiment = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    sentiment += chunk.choices[0].delta.content.strip()

            if sentiment.strip():
                sentiment_display = sentiment.strip().lower()
                if sentiment_display == "positive":
                    st.success("😄 Sentiment: **Positive**")
                elif sentiment_display == "negative":
                    st.error("😞 Sentiment: **Negative**")
                else:
                    st.info("😐 Sentiment: **Neutral**")
            else:
                st.warning("⚠️ Could not determine sentiment. Please try again.")
    else:
        st.warning("⚠️ Please enter some text to analyze.")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>Powered by NVIDIA Llama-3 🦙</p>", unsafe_allow_html=True)
