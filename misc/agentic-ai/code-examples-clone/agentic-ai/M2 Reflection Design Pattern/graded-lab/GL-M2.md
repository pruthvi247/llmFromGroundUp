<img src="https://learn.deeplearning.ai/assets/dlai-logo.png"></img>

## 🧠 Graded Lab: Reflection in a Research Agent

In this graded lab, you’ll implement a simple **agentic workflow** designed to simulate reflective thinking in a writing task. This is one building block of a more complex research agent that will be constructed throughout the course.

### 📘 Objective

Build a three-step workflow where an LLM writes an essay draft, critiques it, and rewrites it. The focus of the lab is not on the content quality of the essay, but rather on how you orchestrate the **calls to the LLM** and pass intermediate results between steps.

### 🛠️ What You’ll Build

* **Step 1 – Drafting:** Call the LLM to generate an initial draft of an essay based on a simple prompt.
* **Step 2 – Reflection:** Reflect on the draft using a reasoning step. (Optionally, this can be done with a different model.)
* **Step 3 – Revision:** Apply the feedback from the reflection to generate a revised version of the essay.

### 🧪 Assessment Criteria

You’ll be graded based on how well you implement the agent functions. The grading is focused on **code correctness**, not the essay content. Specifically:

* Each function should:

  1. Successfully make a call to the LLM.
  2. Return the correct **type** of output (e.g., a string).
* The full workflow should:

  * Successfully execute end-to-end.
  * Maintain consistent structure and data flow across steps.

## ⚙️ Loading Essentials

Before interacting with the language models, we initialize the `aisuite` client. This setup loads environment variables (e.g., API keys) from a `.env` file to securely authenticate with backend services. The `ai.Client()` instance will be used to make all model calls throughout this workflow.


```python
from dotenv import load_dotenv

load_dotenv()

import aisuite as ai

client = ai.Client()
```

### 📝 Exercise: `generate_draft` Function

**Objective**:
Write a function called `generate_draft` that takes in a string prompt and uses a language model to generate a complete draft essay.

**Inputs**:

* `prompt` (str): The essay question or writing prompt.
* `model` (str, optional): The model identifier to use. Defaults to `"openai:gpt-4o"`.

**Output**:

* A string representing the full draft of the essay.

**Requirements**:

* The generated essay should be well-structured, including an introduction, a body, and a conclusion.
* The function should send the prompt to the model and return only the model’s response.

You do **not** need to modify or analyze the content—just call the model appropriately and return the generated draft.



```python
# Write your `generate_draft` function here
```

### 🔍 Exercise: `reflect_on_draft` Function

**Objective**:
Write a function called `reflect_on_draft` that takes a previously generated essay draft and uses a language model to provide constructive feedback.

**Inputs**:

* `draft` (str): The essay text to reflect on.
* `model` (str, optional): The model identifier to use. Defaults to `"openai:o4-mini"`.

**Output**:

* A string with feedback in paragraph form.

**Requirements**:

* The feedback should be critical but constructive.
* It should address issues such as structure, clarity, strength of argument, and writing style.
* The function should send the draft to the model and return its response.

You do **not** need to rewrite the essay at this step—just analyze and reflect on it.



```python
# Write your `reflect_on_draft` function here
```

### 🔁 Exercise: `revise_draft` Function

**Objective**:
Implement a function called `revise_draft` that improves a given essay draft based on feedback from a reflection step.

**Inputs**:

* `original_draft` (str): The initial version of the essay.
* `reflection` (str): Constructive feedback or critique on the draft.
* `model` (str, optional): The model identifier to use. Defaults to `"openai:gpt-4o"`.

**Output**:

* A string containing the revised and improved essay.

**Requirements**:

* The revised draft should address the issues mentioned in the feedback.
* It should improve clarity, coherence, argument strength, and overall flow.
* The function should use the feedback to guide the revision, and return only the final revised essay.



```python
# Write your `revise_draft` function here
```

### 🧪 Test the Reflective Writing Workflow

Use the functions you implemented to simulate the complete writing workflow:

1. **Generate a draft** in response to the essay prompt.
2. **Reflect** on the draft to identify improvements.
3. **Revise** the draft using the feedback.

Observe the outputs of each step. You do **not** need to modify the outputs — just verify that the workflow runs as expected and each component returns a valid string.

>**👉 Uncomment the code below once your functions are ready to test them in action.**




```python
essay_prompt = "Should social media platforms be regulated by the government?"

# Agente 1 – Draft
#draft = generate_draft(essay_prompt)
#print("📝 Draft:\n")
#print(draft)

# Agente 2 – Reflection
#feedback = reflect_on_draft(draft)
#print("\n🧠 Feedback:\n")
#print(feedback)

# Agente 3 – Revision
#revised = revise_draft(draft, feedback)
#print("\n✍️ Revised:\n")
#print(revised)


```

To better visualize the output of each step in the reflective writing workflow, we use a utility function called `show_output`. This function displays the results of each stage (drafting, reflection, and revision) in styled boxes with custom background and text colors, making it easier to compare and understand the progression of the essay.

>**👉 Uncomment the code below once your functions are ready to test them in action.**




```python
from utils import show_output

essay_prompt = "Should social media platforms be regulated by the government?"

#show_output("Step 1 – Draft", draft, background="#fff8dc", text_color="#333333")
#show_output("Step 2 – Reflection", feedback, background="#e0f7fa", text_color="#222222")
#show_output("Step 3 – Revision", revised, background="#f3e5f5", text_color="#222222")

```
