from dotenv import load_dotenv
load_dotenv() ## loading all the environment variable

import streamlit as st
import os
from google import genai
from google.genai import types

client =genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
tools = [types.Tool(google_search=types.GoogleSearch())]
## function to load gemini pro model and get responses

def get_gemini_response(question):
   response = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=question,
        config=types.GenerateContentConfig(
            tools=tools
        )
    )
   return response

# Streamlit page
st.set_page_config(page_title="AI News Chatbot", page_icon="🤖")

st.title("🤖 AI News Chatbot")
st.caption("Powered by Gemini + Google Search")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
if prompt := st.chat_input("Ask about latest news..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot response
    with st.chat_message("assistant"):

        response_box = st.empty()
        full_response = ""

        response = get_gemini_response(prompt)

        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                response_box.markdown(full_response)

    # Save bot message
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )