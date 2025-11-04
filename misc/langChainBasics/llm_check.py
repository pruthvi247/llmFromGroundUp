from gen_ai_hub.proxy.langchain.init_models import init_llm
 
# This will show available models when you try to initialize
# You can check what models are available by looking at the error or documentation
 
# First, let's check if we can list available models
try:
    # Try to get a proxy client
    from gen_ai_hub.proxy.gen_ai_hub_proxy.client import GenAIHubProxyClient
    
    client = GenAIHubProxyClient()
    deployments = client.get_deployments()
    
    print("Available deployments:")
    for deployment in deployments:
        print(f"- Model: {deployment.model_name}")
        print(f"- Model: {deployment}")
        break
        # print(f"  ID: {deployment.id}")
        # print(f"  Status: {deployment.status}")
        # print(f"  Scenario: {deployment.scenario_id}")
        print("---")
        
except Exception as e:
    print(f"Error: {e}")