# Tika setup
from tika import parser
from transformers import pipeline
# Streamlit UI
import streamlit as st

# Allow user to upload file
uploaded_file = st.file_uploader("Choose a file") 

# Extract text using Tika
if uploaded_file is not None:
    file_details = {"Filename":uploaded_file.name, "FileSize":uploaded_file.size}
    st.write(file_details)
    raw_text = parser.from_file(uploaded_file)['content'] 

# Summarization code
# Use T5
summarizer = pipeline("summarization", model="t5-base")  

# Allow user to set summary length
summary_length = st.slider("Select summary length", min_value=10, max_value=500, value=20)

# Summarize 
summary = summarizer(raw_text, max_length=summary_length)

# Display summary
st.write(summary)