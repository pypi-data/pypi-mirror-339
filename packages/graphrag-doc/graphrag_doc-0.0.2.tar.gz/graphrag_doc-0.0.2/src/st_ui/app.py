import asyncio
from functools import lru_cache
import streamlit as st
from langgraph_sdk import get_client

# Backend URL (LangGraph Dev)
BACKEND_URL = "http://127.0.0.1:2024"
GRAPH_ID = "legal_doc"

# Initialize Streamlit Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "assistant_id" not in st.session_state:
    st.session_state.assistant_id = None

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

@lru_cache
def lg_client():
    """Returns a cached LangGraph client instance."""
    return get_client(url=BACKEND_URL)

async def initialize_session():
    """Ensures session state is populated with necessary assistant and thread IDs."""
    client = lg_client()

    # Fetch or create Assistant ID
    if not st.session_state.assistant_id:
        try:
            assistants = await client.assistants.search(graph_id=GRAPH_ID)
            if not assistants:
                st.error("No assistants found.")
                st.stop()
            st.session_state.assistant_id = assistants[0]["assistant_id"]
        except Exception as e:
            st.error(f"Error fetching assistant ID: {e}")
            st.stop()

    # Fetch or create Thread ID
    if not st.session_state.thread_id:
        try:
            st.session_state.thread_id = (await client.threads.create())["thread_id"]
        except Exception as e:
            st.error(f"Error creating thread: {e}")
            st.stop()

async def main():
    """Main function for the Streamlit chatbot."""
    st.set_page_config(page_title="Legal Chatbot", page_icon="💼")
    st.title("💼 Legal Chatbot with LightRAG")

    # Ensure required session state variables are initialized
    await initialize_session()

    # Display chat history
    for role, content in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(content)

    client = lg_client()
    user_input = st.chat_input("Ask a legal question related to FRANCIS...")

    if user_input:
        # Append user input to chat history
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # Prepare request payload
        run_input = {"messages": user_input}

        # Send request to LangGraph backend
        with st.chat_message("assistant"):
            response_container = st.empty()
            with st.spinner("Thinking..."):
                try:
                    response = await client.runs.wait(
                        assistant_id=st.session_state.assistant_id,
                        thread_id=st.session_state.thread_id,
                        input=run_input
                    )
                    if "messages" in response and response["messages"]: # type: ignore
                        agent_message = response["messages"][-1] # type: ignore
                        agent_message["type"] = "ai"

                        # Append response to session state
                        st.session_state.messages.append(agent_message)
                        st.session_state.chat_history.append(("assistant", agent_message.get("content", "No response.")))

                    else:
                        st.error("Received empty response from assistant.")

                    st.rerun()

                except Exception as e:
                    st.error(f"Error during assistant response: {e}")

if __name__ == "__main__":
    asyncio.run(main())