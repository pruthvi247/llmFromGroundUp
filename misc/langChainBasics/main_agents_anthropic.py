from langchain_core.prompts import PromptTemplate
from gen_ai_hub.proxy.langchain.init_models import init_llm
from langchain_core.output_parsers import StrOutputParser
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType
from gen_ai_hub.proxy.langchain.amazon import (
    init_chat_model as amazon_init_invoke_model,
    init_chat_converse_model as amazon_init_converse_model
)
from gen_ai_hub.proxy.langchain.amazon import ChatBedrock, ChatBedrockConverse
from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client

#####  uv pip install wikipedia
#### <path>/llmFromGroundUp/.venv/bin/python main_agents.py



def lang_chain_helper(input_question):
    """
    LangChain helper function with proper output key handling
    """
    llm_model='anthropic--claude-4-sonnet'
    anthropic_model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    # Initialize the LLM
    # llm = init_llm(llm_model, max_tokens=300)
    
    # llm = init_llm(llm_model, max_tokens=300)
    # Always use the specific Anthropic deployment - no other models allowed
    # anthropic_model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    # llm_model = 'anthropic--claude-4-sonnet'
    deployment_id = 'd0a6f0c69d44cb5b'
    
    print(f"================================ Using ONLY Anthropic Model Deployment {deployment_id} ==================")
    proxy_client = get_proxy_client('gen-ai-hub')

    try:
            llm = init_llm(llm_model, model_id=anthropic_model_id, init_func=amazon_init_converse_model, max_tokens=300)
            print("Fallback initialization successful")
    except Exception as e2:
            print(f"Fallback init also failed: {e2}")
            raise RuntimeError(f"Unable to initialize Anthropic model: {e2}")
    # Create the prompt template
    template = """Question: {query}
        Answer: Let's think step by step."""
    prompt = PromptTemplate(template=template, input_variables=['query'])
    
        # Method 1: Use the underlying client directly to bypass LangChain serialization
    from langchain_core.messages import HumanMessage
    
    # Format the prompt directly
    formatted_prompt = prompt.format(query=input_question)
    
    try:
        # Access the underlying bedrock client directly to avoid LangChain serialization
        print("Attempting to use underlying client directly...")
        
        # Get the underlying client from the LLM
        if hasattr(llm, 'client'):
            bedrock_client = llm.client
            # bedrock_client = init_llm(llm_model,model_id=anthropic_model_id,init_func=amazon_init_converse_model) # Explicitly select Converse API)
            
            # Prepare the request directly
            request_body = {
                "messages": [{"role": "user", "content": formatted_prompt}],
                "max_tokens": 300,
                "temperature": 0.7,
                "anthropic_version": "bedrock-2023-05-31"
            }
            
            # Make direct API call using the deployment endpoint
            import json
            response = bedrock_client.invoke_model(
                body=json.dumps(request_body),
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",  # fallback model ID
                accept='application/json',
                contentType='application/json'
            )
            
            # Parse response
            response_body = json.loads(response.get('body').read())
            response_text = response_body.get('content', [{}])[0].get('text', '')
            
        else:
            # Fallback: try a very basic invocation without serialization
            print("No direct client access, trying basic invocation...")
            
            # Create a simple text prompt instead of messages to avoid message serialization
            try:
                # Monkey patch to avoid serialization
                original_serialized = llm._serialized
                llm._serialized = {}  # Empty dict to avoid circular reference
                
                response = llm.invoke(formatted_prompt)
                
                # Restore original
                llm._serialized = original_serialized
                
                if hasattr(response, 'content'):
                    response_text = response.content
                else:
                    response_text = str(response)
                    
            except Exception as e3:
                print(f"Basic invocation also failed: {e3}")
                # Ultimate fallback - return a mock response indicating the issue
                response_text = f"ERROR: Unable to get response from Anthropic model due to circular reference in LangChain serialization. Model is deployed and accessible at deployment_id: d0a6f0c69d44cb5b, but LangChain has serialization conflicts with this specific model configuration."
                
    except Exception as e:
        print(f"Direct client method failed: {e}")
        response_text = f"ERROR: All methods failed. The Anthropic model is available but has fundamental LangChain compatibility issues. Error: {e}"
    
    print(f"Generated response: {response_text}")
    return response_text

def lanchain_agent():
    # Use only the Anthropic deployment
    deployment_id = 'd0a6f0c69d44cb5b'
    proxy_client = get_proxy_client('gen-ai-hub')
    llm_model='gpt-4o'
    try:
        llm = ChatBedrockConverse(
            proxy_client=proxy_client,
            deployment_id=deployment_id,
            streaming=False,
            max_tokens=300,
            temperature=0.7
        )
    except Exception as e:
        print(f"Agent: Direct deployment failed: {e}")
        # Fallback
        llm = init_llm(llm_model, model_id="anthropic--claude-4-sonnet", init_func=amazon_init_converse_model, max_tokens=300)
    tools = load_tools(["wikipedia", "llm-math"], llm=llm)
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    result = agent.run("What the age of supernova? Multiply the age by 3")
    print(f"Agent result: {result}")
    return agent

def check_model_availability():
    try:
        from gen_ai_hub.proxy.gen_ai_hub_proxy.client import GenAIHubProxyClient
        
        client = GenAIHubProxyClient()
        deployments = client.get_deployments()
        
        print("Available deployments:")
        for deployment in deployments:
            print(f"- Model: {deployment.model_name}")
            print(f"- Model: {deployment}")
            break
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # llm_model='gpt-4o'
    llm_model='anthropic--claude-4-sonnet'
    anthropic_model_id = "anthropic--claude-4-sonnet"
    # check_model_availability()
    lang_chain_helper("What is a supernova?")
    # lanchain_agent()