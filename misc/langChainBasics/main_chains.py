from langchain_core.prompts import PromptTemplate
from gen_ai_hub.proxy.langchain.init_models import init_llm
from langchain_core.output_parsers import StrOutputParser
#####  uv pip install  "sap-ai-sdk-gen[all]

def lang_chain_helper(input_question):
    """
    LangChain helper function with proper output key handling
    """
    
    # Initialize the LLM
    llm = init_llm('gpt-4o', max_tokens=300)
    
    # Create the prompt template
    template = """Question: {query}
        Answer: Let's think step by step."""
    prompt = PromptTemplate(template=template, input_variables=['question'])
    
    # Method 1: Simple approach - parse to string then wrap in dict
    chain = prompt | llm | StrOutputParser()
    response_text = chain.invoke({'query': input_question})
    # response = {"description": response_text}
    response =  response_text
    
    # Method 2: Using a custom function (uncomment to use)
    # def format_output(text):
    #     """Custom function to format output with description key"""
    #     return {"description": text}
    # 
    # chain = prompt | llm | StrOutputParser()
    # response_text = chain.invoke({'question': input_question})
    # response = format_output(response_text)
    
    # Method 3: If you want to use RunnableLambda (requires langchain_core.runnables)
    # try:
    #     from langchain_core.runnables import RunnableLambda
    #     format_func = RunnableLambda(lambda text: {"description": text})
    #     chain = prompt | llm | StrOutputParser() | format_func
    #     response = chain.invoke({'question': input_question})
    # except ImportError:
    #     # Fallback to method 1 if RunnableLambda not available
    #     chain = prompt | llm | StrOutputParser()
    #     response_text = chain.invoke({'question': input_question})
    #     response = {"description": response_text}
    
    print(f"Generated response: {response}")
    return response

if __name__ == "__main__":
    lang_chain_helper("What is a supernova?")