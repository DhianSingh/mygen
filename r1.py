import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PyPDF2 import PdfReader
import requests
import time

# DeepSeek API configuration
DEEPSEEK_API_KEY = "your-deepseek-api-key"  # Replace with your DeepSeek API key
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Replace with the actual DeepSeek API endpoint

# Function to call DeepSeek R1 model
def call_deepseek_model(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-r1",  # Replace with the correct model name
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Streamlit App
st.title("Generative Ai Web App")

# Sidebar for user inputs
st.sidebar.header("User Input Features")
uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type="pdf")
live_data = st.sidebar.checkbox("Enable Live Data Streaming")

# Main area
st.header("Data Visualization")

if uploaded_file is not None:
    # Read the PDF file
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    st.subheader("Extracted Text from PDF")
    st.write(text)

    # Use DeepSeek R1 model to process the text
    if st.button("Process Text with DeepSeek"):
        response = call_deepseek_model(text)
        st.subheader("DeepSeek R1 Response")
        st.write(response)

if live_data:
    st.subheader("Live Data Streaming")
    placeholder = st.empty()
    
    # Simulate live data streaming
    for i in range(10):
        data = pd.DataFrame({
            'x': range(i, i+10),
            'y': [j ** 2 for j in range(i, i+10)]
        })
        
        placeholder.line_chart(data)
        time.sleep(1)

# Graph Visualization
st.subheader("Multiple Graphs")

# Example data
data = pd.DataFrame({
    'x': range(10),
    'y': [i ** 2 for i in range(10)],
    'z': [i ** 3 for i in range(10)]
})

# Plotting with Matplotlib
fig, ax = plt.subplots()
ax.plot(data['x'], data['y'], label='y = x^2')
ax.plot(data['x'], data['z'], label='z = x^3')
ax.set_xlabel('x')
ax.set_ylabel('y/z')
ax.legend()
st.pyplot(fig)

# Plotting with Seaborn
st.subheader("look the graph")
sns.lineplot(data=data, x='x', y='y', label='y = x^2')
sns.lineplot(data=data, x='x', y='z', label='z = x^3')
st.pyplot(plt.gcf())