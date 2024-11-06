import streamlit as st

class ControlGapUI:
    def controlgap_generation(self):
        if st.session_state.generating:
            st.write("This is where control gap analysis would happen")
            st.session_state.controlgap = "Example control gap analysis content"

        if st.session_state.controlgap and st.session_state.controlgap != "":
            with st.container():
                st.write("Control Gap Analysis generated successfully!")
                st.download_button(
                    label="Download HTML file",
                    data=st.session_state.controlgap,
                    file_name="controlgap.html",
                    mime="text/html",
                )
            st.session_state.generating = False

    def sidebar(self):
        with st.sidebar:
            st.title("Control Gap Analysis")

            st.write(
                """
                To generate a control gap analysis, enter a topic and a personal message.
                """
            )

            st.text_input("Topic", key="topic", placeholder="Swap dealer")

            st.text_area(
                "Your personal message (to include at the top of the analysis)",
                key="personal_message",
                placeholder="Give me the updated CFTC rules and current controls on swap trading limit",
            )

            if st.button("Generate Analysis"):
                st.session_state.generating = True

    def render(self):
        st.set_page_config(page_title="Control Gap Analysis", page_icon="🔍")

        if "topic" not in st.session_state:
            st.session_state.topic = ""

        if "personal_message" not in st.session_state:
            st.session_state.personal_message = ""

        if "controlgap" not in st.session_state:
            st.session_state.controlgap = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        self.sidebar()
        self.controlgap_generation()

if __name__ == "__main__":
    ControlGapUI().render()