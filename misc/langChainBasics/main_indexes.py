from langchain_community.document_loaders import YoutubeLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from gen_ai_hub.proxy.langchain.init_models import init_llm
from langchain_community.vectorstores import FAISS
from gen_ai_hub.proxy.langchain.init_models import init_embedding_model
from langchain_core.output_parsers import StrOutputParser

# Initialize LLM for text generation
llm = init_llm(model_name="gpt-4o")

# Initialize embedding model for vector storage
embedding_model = init_embedding_model(model_name="text-embedding-ada-002")

# print(f"Initialized embedding model: {llm} , type: {type(llm)}")
def create_vector_db_from_youtube_url(video_url: str) -> FAISS:
    try:
        loader = YoutubeLoader.from_youtube_url(video_url)
        transcript = loader.load()
        
        if not transcript:
            raise ValueError("No transcript found for the video")
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(transcript)
        print(f"Number of document chunks created: {len(docs)}")
        
        if not docs:
            raise ValueError("No documents created from transcript")
        
        db = FAISS.from_documents(docs, embedding_model)
        return db
        
    except Exception as e:
        print(f"Error processing YouTube video: {e}")
        print(f"This might be due to:")
        print("1. Video has no transcript/captions")
        print("2. Video is private or restricted")
        print("3. YouTube API rate limiting")
        print("4. Network connectivity issues")
        raise

def get_response_from_query(db, query, k=4):
    """
    text-davinci-003 can handle up to 4097 tokens. Setting the chunksize to 1000 and k to 4 maximizes
    the number of tokens to analyze.
    """

    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    ### llm = OpenAI(model_name="text-davinci-003")
    # llm = init_embedding_model(
    # model_name = "text-embedding-ada-002",)

    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template="""
        You are a helpful assistant that that can answer questions about youtube videos 
        based on the video's transcript.
        
        Answer the following question: {question}
        By searching the following video transcript: {docs}
        
        Only use the factual information from the transcript to answer the question.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed.
        """,
    )

    # Create chain with proper LLM and invoke method
    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"question": query, "docs": docs_page_content})
    response = response.replace("\n", "")
    return response, docs

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=lG7Uxts9SXs"
    vector_db = create_vector_db_from_youtube_url(video_url)
    
    print(f"Created vector DB: {vector_db}, type: {type(vector_db)}")
    # docs = vector_db.similarity_search("What is a supernova?")
    # print(f"Retrieved documents: {docs}")
