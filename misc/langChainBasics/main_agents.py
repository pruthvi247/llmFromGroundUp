from langchain_core.prompts import PromptTemplate
from gen_ai_hub.proxy.langchain.init_models import init_llm
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import load_tools, initialize_agent, AgentType
#####  uv pip install wikipedia

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
    print(f"Generated response: {response}")
    return response

def lanchain_agent():
    llm = init_llm('gpt-4o', max_tokens=300)
    tools = load_tools(["wikipedia", "llm-math"], llm=llm)
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    result = agent.run("What the age of supernova? Multiply the age by 3")
    print(f"Agent result: {result}")
    return agent

if __name__ == "__main__":
    # lang_chain_helper("What is a supernova?")
    lanchain_agent()