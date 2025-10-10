import streamlit as st
import main_indexes as lch
import textwrap

st.title("YouTube Assistant")

st.write("This is a simple app to demonstrate the basics of LangChain.")

with st.sidebar:
    with st.form(key='my_form'):
        youtube_url = st.sidebar.text_area(
            label="What is the YouTube video URL?",
            max_chars=50
            )
        query = st.sidebar.text_area(
            label="Ask me about the video?",
            max_chars=50,
            key="query"
            )
        # openai_api_key = st.sidebar.text_input(
        #     label="OpenAI API Key",
        #     key="langchain_search_api_key_openai",
        #     max_chars=50,
        #     type="password"
        #     )
        # "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        # "[View the source code](https://github.com/rishabkumar7/pets-name-langchain/tree/main)"
        submit_button = st.form_submit_button(label='Submit')

if submit_button and youtube_url and query:
    try:
        with st.spinner('Processing YouTube video...'):
            db = lch.create_vector_db_from_youtube_url(youtube_url)
        
        with st.spinner('Generating response...'):
            response, docs = lch.get_response_from_query(db, query)
        
        st.subheader("Answer:")
        st.text(textwrap.fill(response, width=85))
        
        # Show source documents
        st.subheader("Source Documents:")
        for i, doc in enumerate(docs):
            st.write(f"**Document {i+1}:**")
            st.write(textwrap.fill(doc.page_content[:200] + "...", width=85))
            
    except Exception as e:
        st.error(f"Error processing request: {str(e)}")
        st.info("Please make sure:")
        st.info("1. The YouTube URL is valid and public")
        st.info("2. The video has captions/transcript available")
        st.info("3. You have a stable internet connection")

elif submit_button:
    if not youtube_url:
        st.warning("Please provide a YouTube URL")
    if not query:
        st.warning("Please provide a question about the video")