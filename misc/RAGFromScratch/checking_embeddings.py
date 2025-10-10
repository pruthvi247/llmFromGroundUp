from langchain_core.prompts import PromptTemplate
# from gen_ai_hub.proxy.langchain.init_models import init_llm, init_embeddings
from gen_ai_hub.proxy.langchain.init_models import  init_embedding_model

# llm = init_llm(
#     model_name = "text-embedding-ada-00",)
#     # model_name = "gpt-4o",)
#####  uv pip install  "sap-ai-sdk-gen[all]

llm = init_embedding_model(
    model_name = "text-embedding-ada-002",)
    # model_name = "gpt-4o",)

#  "model": "text-embedding-ada-002"

# prompt = PromptTemplate(
#     template="give me the age of below celebraty \n {celeb}",
#     input_variables=["celeb"]

# )

# final_prompt = prompt.invoke({"celeb": "srk"})

# llm.invoke(final_prompt)
print(llm.embed_query("hello world"))
 