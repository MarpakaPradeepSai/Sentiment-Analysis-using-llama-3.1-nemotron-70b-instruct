from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key= "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"
)

# Sample input text for sentiment analysis
input_text = "Not a good product"

# Modify the prompt to ensure the model responds with just 'positive', 'negative', or 'neutral'
completion = client.chat.completions.create(
    model="nvidia/llama-3.1-nemotron-70b-instruct",  # Ensure this model supports sentiment analysis
    messages=[
        {
            "role": "user",
            "content": f"Please analyze the sentiment of the following text and respond with only one word: 'positive', 'negative', or 'neutral'. Text: '{input_text}'"
        }
    ],
    temperature=0.5,
    top_p=1,
    max_tokens=1024,
    stream=True
)

# Process and print the response
for chunk in completion:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content.strip(), end="")
