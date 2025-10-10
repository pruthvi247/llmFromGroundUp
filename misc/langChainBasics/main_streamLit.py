import main_chains as main_chains
import streamlit as st

st.title("LangChain Basics")
st.write("This is a simple app to demonstrate the basics of LangChain.")

question_topic = st.selectbox("select a topic",["Supernova","Black Hole","Neutron Star","Pulsar","Quasar"])

if question_topic:
    # st.sidebar.text_area(f"You selected: {question_topic}")
    st.sidebar.write(f"You selected: {question_topic}")

if st.button("Generate"):
    response = main_chains.lang_chain_helper(question_topic)
    st.write(response)
    # st.text_area("Response", value=response["description"], height=200)
    st.write("Done")