import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Streamlit UI
st.set_page_config(layout="wide")  # Set wide layout for more space

# Header Section
st.markdown(
    """
    <h1 style="color:#0066cc;">Sentiment Analysis Using Llama-3.1 Nemotron 70b</h1>
    <p style="font-size:16px;">Analyze text sentiment with NVIDIA's Llama-3.1 Nemotron 70b model.</p>
    """,
    unsafe_allow_html=True
)

# Text input box for the user to enter text
with st.container():
    input_text = st.text_area(
        "Enter text for sentiment analysis:",
        height=150,
        placeholder="Type or paste your text here..."
    )

# Analysis Button
col1, col2 = st.columns([4, 1])
with col2:
    analyze_button = st.button("Analyze Sentiment")

# Analysis Result
if analyze_button:
    if input_text:
        # Modify the prompt to ensure the model responds with just 'positive', 'negative', or 'neutral'
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",  # Ensure this model supports sentiment analysis
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
        
        sentiment = ""  # Variable to accumulate the sentiment result
        for chunk in completion:
            # Ensure that content exists in the chunk and accumulate
            if chunk.choices[0].delta.content:
                sentiment += chunk.choices[0].delta.content.strip()
        
        # Check the accumulated sentiment and display
        if sentiment.strip():
            st.markdown(
                f"""
                <h2 style="color:#0066cc;">Sentiment Result:</h2>
                <h1 style="color:{'green' if sentiment.strip() == 'Positive' else 'red' if sentiment.strip() == 'Negative' else 'orange'};">{sentiment.strip()}</h1>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <h2 style="color:#0066cc;">Sentiment Result:</h2>
                <h1 style="color:gray;">Could not determine sentiment. Please try again.</h1>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            """
            <h2 style="color:#0066cc;">Sentiment Result:</h2>
            <h1 style="color:gray;">Please enter some text to analyze.</h1>
            """,
            unsafe_allow_html=True
        )
