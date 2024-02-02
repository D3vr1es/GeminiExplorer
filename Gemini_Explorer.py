import vertexai 
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

# Initialize session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get user input for their name
user_name = st.text_input("Enter your name")

# Check if the user's name is provided
if user_name:
    personalized_greeting = f"Hello, {user_name}! How can I assist you today?"
else:
    personalized_greeting = "Hello! How can I assist you today?"

# Display personalized greeting
st.title("Gemini Explorer")
st.write(personalized_greeting)

project = "gemini-explorer-412321"
vertexai.init(project=project)

config = generative_models.GenerationConfig(
    temperature=0.4
)

model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)

chat = model.start_chat()

def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })
    st.session_state.messages.append({
        "role": "model",
        "content": output
    })

# Display chat input field if user name is provided
if user_name:
    query = st.text_input("Gemini Explorer")
    if query:
        with st.chat_message("user"):
            st.markdown(query)

        llm_function(chat, query)
