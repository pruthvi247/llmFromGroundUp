from langchain_core.prompts import PromptTemplate
from gen_ai_hub.proxy.langchain.init_models import init_llm
#####  uv pip install  "sap-ai-sdk-gen[all]
llm = init_llm(
    model_name = "gpt-4o",
    # model_name = "gpt-4o",
)
prompt = PromptTemplate(
    template="give me the age of below celebraty \n {celeb}",
    input_variables=["celeb"]
)

final_prompt = prompt.invoke({"celeb": "srk"})
response = llm.invoke(final_prompt)
print(response)