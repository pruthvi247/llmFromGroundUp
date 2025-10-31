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
def generate_draft(prompt: str, model: str = "openai:gpt-4o") -> str:
    instruction = f"""
    Write a well-structured draft essay in response to the following prompt.
    The draft should include an introduction, body, and conclusion.

    Prompt:
    {prompt}
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": instruction}],
        temperature=1.0,
    )
    return response.choices[0].message.content

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
def reflect_on_draft(draft: str, model: str = "openai:o4-mini") -> str:
    instruction = f"""
    Reflect critically on the following draft essay.
    Identify areas for improvement in structure, clarity, argument strength, or style.
    Provide constructive feedback in paragraph form.

    Draft:
    {draft}
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": instruction}],
        temperature=1.0,
    )
    return response.choices[0].message.content

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
def revise_draft(original_draft: str, reflection: str, model: str = "openai:gpt-4o") -> str:
    instruction = f"""
    Revise the following essay draft using the feedback provided.
    Make improvements in clarity, coherence, argumentation, and flow.
    Return only the improved essay.

    Original Draft:
    {original_draft}

    Feedback:
    {reflection}
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": instruction}],
        temperature=1.0,
    )
    return response.choices[0].message.content

```

### 🧪 Test the Reflective Writing Workflow

Use the functions you implemented to simulate the complete writing workflow:

1. **Generate a draft** in response to the essay prompt.
2. **Reflect** on the draft to identify improvements.
3. **Revise** the draft using the feedback.

Observe the outputs of each step. You do **not** need to modify the outputs — just verify that the workflow runs as expected and each component returns a valid string.



```python
essay_prompt = "Should social media platforms be regulated by the government?"

# Agente 1 – Draft
draft = generate_draft(essay_prompt)
print("📝 Draft:\n")
print(draft)

# Agente 2 – Reflection
feedback = reflect_on_draft(draft)
print("\n🧠 Feedback:\n")
print(feedback)

# Agente 3 – Revision
revised = revise_draft(draft, feedback)
print("\n✍️ Revised:\n")
print(revised)


```

    📝 Draft:
    
    **Title: The Case for Government Regulation of Social Media Platforms**
    
    **Introduction**
    
    In the digital age, social media platforms have become integral to daily communication, information dissemination, and social interaction. With billions of users worldwide, platforms like Facebook, Twitter, Instagram, and TikTok wield enormous influence over public discourse. This unprecedented power raises critical questions about their role in society and the need for regulation. Proponents of government oversight argue that regulation is necessary to protect users from harmful content, safeguard privacy, and ensure the integrity of democratic processes. Opponents, on the other hand, warn that government intervention could stifle innovation, infringe on free speech, and create bureaucratic inefficiencies. This essay will examine these contrasting viewpoints and argue that, despite legitimate concerns, government regulation is necessary to address the challenges posed by the unchecked power of social media platforms.
    
    **Body**
    
    One of the primary arguments for regulating social media platforms is the need to protect users from harmful content. The proliferation of fake news, hate speech, and misinformation on these platforms underscores the risks posed by unregulated digital spaces. For instance, during significant political events, false information can spread rapidly, influencing public opinion and potentially altering election outcomes. Government intervention could enforce standards for content moderation, ensuring that harmful and misleading information is swiftly identified and removed.
    
    Another critical issue is the protection of user privacy. Social media platforms collect vast amounts of personal data, often with minimal transparency and oversight. This data is sometimes sold to third parties, leading to privacy breaches that can have severe consequences for users. Government regulation could enforce stringent data protection standards, ensuring that users retain control over their personal information and that companies face penalties for data misuse. Regulations like the General Data Protection Regulation (GDPR) in the European Union provide a blueprint for how governmental oversight can effectively safeguard user privacy.
    
    Furthermore, social media platforms' significant influence over public discourse necessitates regulation to uphold democratic integrity. Algorithms that prioritize sensationalist content can polarize societies by reinforcing echo chambers and amplifying extreme viewpoints. By implementing regulations that promote transparency in how algorithms function, governments could help mitigate these effects, fostering a more balanced and informed public dialogue.
    
    Nevertheless, critics argue that government regulation may stifle innovation. Social media companies thrive on creativity and rapid adaptation, qualities that could be hindered by bureaucratic oversight. However, this critique overlooks the potential for a regulatory framework that encourages innovation while setting boundaries for ethical conduct, much like regulations in other industries such as finance and healthcare.
    
    Concerns about free speech rights also surface in discussions about regulation. There is apprehension that government involvement could lead to censorship or favoritism. However, regulation need not dictate speech content but rather establish guidelines for transparency, accountability, and fairness, ensuring that platforms do not arbitrarily restrict user expression.
    
    **Conclusion**
    
    In conclusion, the regulation of social media platforms by the government is a necessary step to address the myriad of challenges they present in today's digital landscape. While opponents of regulation raise valid concerns about innovation and free speech, these issues can be addressed through well-considered policies that balance oversight with creative freedom. Ultimately, the goal of regulation should not be to limit the power of social media but to harness it responsibly, protecting users, ensuring privacy, and maintaining the integrity of democratic systems. As social media continues to evolve, so too must the frameworks governing it, safeguarding the interests of users and society alike.
    
    🧠 Feedback:
    
    The draft offers a clear and timely thesis, and its organization—moving from the need for content moderation to privacy protection, democratic integrity, and counterarguments—creates a logical progression. To strengthen the structure further, consider sharpening your introduction with a more specific thesis statement that previews the precise mechanisms of regulation you will endorse (for example, independent oversight boards or data‐usage audits), rather than broadly arguing “government regulation is necessary.” This will help readers anticipate the essay’s direction and make each subsequent section feel more focused.
    
    In terms of clarity and argument strength, each body paragraph benefits from relevant examples, but you might deepen your analysis by incorporating empirical data or case studies. For instance, you mention the spread of misinformation during elections—citing a specific study or incident (such as the 2016 U.S. election or Brazil’s 2018 election) would lend concrete weight to your claims. When discussing privacy, referencing actual GDPR enforcement actions or statistics on data breaches could illustrate how regulation has succeeded (or fallen short) in practice. These details will reinforce your credibility and help readers grasp the real‐world stakes.
    
    Your treatment of counterarguments is commendable, yet it can be made more robust by engaging with the most nuanced concerns—such as the risk of regulatory capture or the possibility that well‐intentioned rules produce unintended consequences, like favoring large incumbents over startups. Addressing these subtleties, and then explaining how your recommended framework would guard against them, will demonstrate that you have thought through potential pitfalls and are proposing a balanced, workable solution.
    
    Finally, on style and flow, watch for repetition—phrases like “government regulation” and “social media platforms” appear frequently and can be varied. Shortening some of the longer, more complex sentences will also increase readability: for example, break apart clauses to strengthen your topic sentences and ensure each paragraph begins with a clear idea. You might also improve transitions by signaling contrasts (“Despite these benefits…,” “Conversely…,”) or cause and effect (“Consequently…,” “As a result…”) to guide the reader smoothly from one point to the next. A concluding suggestion might be to outline next steps or potential legislative models, so your closing moves beyond summary into actionable insight. Incorporating these refinements will elevate the essay’s persuasiveness and give it a more polished, authoritative voice.
    
    ✍️ Revised:
    
    **Title: Strategic Regulatory Measures for Social Media Platforms**
    
    **Introduction**
    
    In today's digital era, social media platforms are central to global communication and information exchange. With billions of users, platforms like Facebook, Twitter, Instagram, and TikTok shape public discourse and influence societal norms. Their immense power emphasizes the need for regulation to address risks such as exposure to harmful content, privacy breaches, and threats to democratic integrity. Key regulatory mechanisms—such as independent oversight boards and comprehensive data-usage audits—could mitigate these challenges effectively. While concerns about innovation and free speech remain, this essay argues that a balanced regulatory approach is crucial for responsibly harnessing the power of social media.
    
    **Body**
    
    A compelling argument for regulating social media platforms is the urgent need to shield users from harmful content. Platforms have become breeding grounds for fake news, hate speech, and misinformation, significantly impacting public perception. For instance, the spread of false information during critical elections, such as the 2016 U.S. presidential election and the 2018 Brazilian election, shows how unregulated digital spaces can distort democratic processes. Implementing independent oversight boards could ensure adherence to content moderation standards, swiftly addressing misleading content.
    
    Moreover, the issue of user privacy demands rigorous governmental oversight. Social media companies accumulate extensive personal data, often exploited without user consent. This was evident in incidents like the Cambridge Analytica scandal, where data misuse had dire consequences. Adopting stringent data-usage audits, akin to the General Data Protection Regulation (GDPR) in the European Union, could enforce transparency and empower users to maintain control over their personal information. Notably, GDPR enforcement actions have demonstrated the potential for robust privacy protection.
    
    The influence of social media platforms on public discourse further underscores the need for regulation to safeguard democratic integrity. Algorithms that prioritize sensationalist content risk entrenching echo chambers and amplifying extreme views. Regulatory measures promoting algorithmic transparency could counteract these effects, fostering more balanced public dialogue. By understanding algorithmic decisions, users can engage with content more critically and diversify their information sources.
    
    Conversely, critics express concern that regulation may stifle innovation, as social media thrives on creativity and adaptability. However, a nuanced regulatory framework can simultaneously encourage innovation and impose ethical boundaries, much like successful regulations in industries like healthcare. Furthermore, apprehensions about infringing on free speech rights reflect fears of censorship. Nonetheless, by establishing guidelines for accountability, regulation can ensure fair expression without dictating speech content.
    
    **Conclusion**
    
    In conclusion, strategic government regulation of social media platforms addresses pressing challenges while balancing the preservation of innovation and free speech. Addressing nuanced concerns such as regulatory capture and unintended market consequences ensures a thoughtful, balanced approach. Suggested mechanisms include independent oversight boards for content moderation, comprehensive data-usage audits for user privacy, and transparent algorithm regulations for democratic protection. To forge a path forward, legislative models need development, harnessing platforms' power for users' and society's benefit. As social media evolves, solidifying regulatory frameworks is critical to safeguarding user rights and democratic values.


## Grading


```python
from utils_grading import run_all_tests

run_all_tests(generate_draft, reflect_on_draft, revise_draft)

```

    ✅ test_generate_draft passed
    ✅ test_reflect_on_draft passed
    ✅ test_revise_draft passed
    
    ✅ 3/3 tests passed.

