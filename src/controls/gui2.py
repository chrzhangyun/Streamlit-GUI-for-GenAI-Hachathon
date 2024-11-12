import pandas as pd
import streamlit as st
from openai import OpenAI

class ControlGapUI:

    def bulk_render(self):
        st.title("Bulk Gap Analysis")

        st.write(
            """
            To generate a control gap analysis, upload a file with control information.
            """
        )

        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:

            df = pd.read_csv(uploaded_file)
            container = st.dataframe(df, height=300)           

        if st.button("Generate Analysis"):
            st.session_state.generating = True

    def chat_render(self):
        st.title("Chat about Barclays Controls")

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask me a question about Barclays controls"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

    def render(self):
        st.set_page_config(page_title="Control Gap Analysis", page_icon="🔍", layout="wide")

        if "topic" not in st.session_state:
            st.session_state.topic = ""

        if "personal_message" not in st.session_state:
            st.session_state.personal_message = ""

        if "controlgap" not in st.session_state:
            st.session_state.controlgap = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        self.bulk, self.chat = st.columns(2, gap="large")
        with self.bulk:
            self.bulk_render()
        with self.chat:
            self.chat_render()


if __name__ == "__main__":
    ControlGapUI().render()