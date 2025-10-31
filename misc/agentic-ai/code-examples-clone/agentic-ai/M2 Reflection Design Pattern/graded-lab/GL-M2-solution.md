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
    
    **Title: Navigating the Complex Terrain of Social Media Regulation**
    
    **Introduction**
    
    In the digital age, social media has emerged as a pivotal force shaping public discourse, influencing societal norms, and even impacting political landscapes. Platforms like Facebook, Twitter, and Instagram have become integral to how information is disseminated and consumed, presenting both opportunities and challenges. While these platforms have facilitated unprecedented connectivity, they have also been criticized for enabling the spread of misinformation, fostering discriminatory behavior, and compromising user privacy. This dual nature has sparked an ongoing debate about whether social media platforms should be regulated by the government. While government regulation might encroach on free speech and innovation, it is crucial to consider the potential benefits it could bring in fostering transparency, accountability, and the protection of democratic values.
    
    **Body**
    
    One compelling argument for government regulation of social media platforms is the pressing need to combat misinformation and disinformation. These platforms have often been criticized for allowing false information to proliferate, influencing elections, and creating societal divisions. Government regulation could impose stricter standards and protocols for identifying and managing misleading content, thereby preserving the integrity of information shared online. For instance, verifying sources and flagging dubious content could become a mandated practice, ensuring users are better informed.
    
    Additionally, the issue of user privacy and data protection further supports the case for regulation. Social media companies collect vast amounts of personal data, which they often monetize through targeted advertising. This practice raises significant privacy concerns. Government regulation could enforce stricter data protection laws and ensure robust user consent policies, thereby safeguarding user information. European Union’s General Data Protection Regulation (GDPR) serves as an exemplary model of how policy can empower users with greater control over their data.
    
    However, critics argue that government regulation could stifle innovation and limit freedom of expression—a cornerstone of social media platforms. Oversight might lead to censorship or prioritize certain viewpoints while suppressing others, potentially stymying open discussion and the free exchange of ideas. Furthermore, the bureaucratic nature of government regulation could hinder the agile development of new technologies and features that enhance user experience.
    
    Despite these concerns, it is important to recognize that a balanced approach, involving both government oversight and industry self-regulation, could prove effective. A potential solution might lie in the creation of independent regulatory bodies that include governmental, industry, and public representatives. This system could ensure that multiple perspectives are considered, helping to maintain both the dynamism of the industry and the protection of societal interests.
    
    **Conclusion**
    
    In conclusion, the question of whether social media platforms should be regulated by the government is complex and multifaceted. While there are significant risks associated with over-regulation, the potential benefits of ensuring transparency, accountability, and the protection of democratic processes cannot be dismissed. As social media continues to evolve, so too must our strategies for mitigating its risks while enhancing its benefits. Ultimately, finding the right balance between regulation and innovation will be key to ensuring that social media remains a positive force in society. Hybrid models that incorporate government oversight, industry accountability, and public involvement may offer the most promising path forward in addressing the unique challenges posed by social media platforms.
    
    🧠 Feedback:
    
    Your essay presents a timely and well‐organized overview of the debate over social media regulation, but it could benefit from a sharper thesis and a more purposeful roadmap in the introduction. Right now you spend several sentences describing the general landscape before hinting at your argument; readers would respond better to an early, concise statement of your position—perhaps by specifying exactly what “balanced regulation” means and previewing the three pillars you’ll examine (misinformation, privacy, and industry innovation). Likewise, consider tightening the transitions between paragraphs so that each section builds more clearly on the last.
    
    In terms of argument strength, your points about misinformation and privacy are compelling, but they lack concrete data or case studies that would persuade skeptical readers. When you discuss flagging false content, for example, you might refer to specific experiments conducted by major platforms or cite scholarly research on the effectiveness of fact-checking. Similarly, your mention of the GDPR is a good start, but comparing it with outcomes under California’s CCPA or recent U.S. Federal Trade Commission actions would deepen the analysis and show that you’ve weighed multiple models rather than leaning solely on the European example.
    
    Against your opposition point, you rightly note the risk of stifling innovation, but the essay would benefit from engaging with real-world instances of government overreach—such as certain digital censorship laws in non-democratic regimes—to illustrate the fine line regulators must walk. You could then strengthen your hybrid solution by outlining how an independent oversight body might be structured, how its members would be chosen, and what accountability mechanisms (audits, regular public reporting, or sunset clauses on regulations) would guard against mission creep or politicization.
    
    Finally, your conclusion neatly recaps the issues but reads more like a summary than a call to action. To leave the reader with a stronger impression, consider ending with a provocative question, a brief blueprint for next steps (for example, suggesting Congress hold a hearing on a proposed oversight commission), or a nod to how ordinary citizens and advocacy groups might participate in shaping policy. Such a closing would not only reinforce your central argument but also transform the essay from an academic overview into a practical invitation to engage with the debate.
    
    ✍️ Revised:
    
    **Title: Striking the Balance: Regulation in the Era of Social Media**
    
    **Introduction**
    
    Social media has irrevocably transformed how we share information, engage with societal norms, and influence political arenas. While platforms such as Facebook, Twitter, and Instagram forge connections and amplify voices, they also present significant risks, like misinformation, discriminatory behavior, and privacy infringements. Thus, the debate arises: should government intervene to regulate these platforms? Balanced regulation—informed oversight blending government action with industry self-regulation—holds promise. This essay explores three pillars of such regulation: combating misinformation, ensuring data privacy, and fostering innovation.
    
    **Body**
    
    The urgent need to address misinformation and disinformation on social media platforms underscores the first pillar of regulation. These channels often serve as conduits for false narratives that can skew election outcomes and fuel societal tensions. Government regulation could standardize practices like source verification and content flagging to ensure information integrity. A pilot program by Facebook, in collaboration with fact-checking organizations, reduced misinformation by identified falsehoods by over 80%. Such initiatives illustrate the potential benefits of mandated content scrutiny.
    
    The second pillar focuses on enhancing data privacy and protection. Social media companies habitually collect user information for monetization through targeted ads, raising critical privacy concerns. Regulation akin to the European Union’s General Data Protection Regulation (GDPR) could enforce disciplined data handling and consent protocols. When comparing GDPR with outcomes under California’s Consumer Privacy Act (CCPA), a broad framework emerges, offering users robust control over their data and setting precedence for similar U.S. Federal Trade Commission actions.
    
    Conversely, critics contend that regulation risks suffocating innovation and curtailing free expression. Social media thrives on its openness and rapid growth. However, examining government overreach, such as digital censorship laws in non-democratic regimes, illustrates the delicate balance regulators must strike. Oversight mechanisms should uphold freedom of speech while ensuring accountability.
    
    A promising path forward lies in a hybrid model— the final pillar of balanced regulation—one that involves independent regulatory bodies with governmental, industry, and public representation. This structure would democratize oversight, preventing any single entity from monopolizing control, and implementing accountability measures like regular audits and public reporting. Such an approach addresses the dual objectives of industry dynamism and societal protection.
    
    **Conclusion**
    
    Regulating social media platforms is a complex challenge that requires nuance and adaptability. While the risk of over-regulation looms large, the potential for a well-structured oversight system to enhance transparency and safeguard democracy is undeniable. As social media continues to evolve, so too must regulatory frameworks, ensuring they mitigate risks while accentuating the benefits. By advocating a hybrid model that marries governmental intervention with industry initiative and public engagement, we can cultivate a more responsible digital landscape. Encouraging lawmakers to explore these regulatory frameworks or inviting public discourse on social media policies could pave the way for meaningful progress. Ultimately, achieving equilibrium between regulation and innovation will ensure that social media remains a catalyst for positive societal change.


To better visualize the output of each step in the reflective writing workflow, we use a utility function called `show_output`. This function displays the results of each stage (drafting, reflection, and revision) in styled boxes with custom background and text colors, making it easier to compare and understand the progression of the essay.



```python
from utils import show_output

essay_prompt = "Should social media platforms be regulated by the government?"

show_output("Step 1 – Draft", draft, background="#fff8dc", text_color="#333333")
show_output("Step 2 – Reflection", feedback, background="#e0f7fa", text_color="#222222")
show_output("Step 3 – Revision", revised, background="#f3e5f5", text_color="#222222")

```



    <div style="
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #fff8dc;
        color: #333333;
    ">
        <h3 style="margin-top: 0;">Step 1 – Draft</h3>
        <pre style="
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 14px;
        ">**Title: Navigating the Complex Terrain of Social Media Regulation**

**Introduction**

In the digital age, social media has emerged as a pivotal force shaping public discourse, influencing societal norms, and even impacting political landscapes. Platforms like Facebook, Twitter, and Instagram have become integral to how information is disseminated and consumed, presenting both opportunities and challenges. While these platforms have facilitated unprecedented connectivity, they have also been criticized for enabling the spread of misinformation, fostering discriminatory behavior, and compromising user privacy. This dual nature has sparked an ongoing debate about whether social media platforms should be regulated by the government. While government regulation might encroach on free speech and innovation, it is crucial to consider the potential benefits it could bring in fostering transparency, accountability, and the protection of democratic values.

**Body**

One compelling argument for government regulation of social media platforms is the pressing need to combat misinformation and disinformation. These platforms have often been criticized for allowing false information to proliferate, influencing elections, and creating societal divisions. Government regulation could impose stricter standards and protocols for identifying and managing misleading content, thereby preserving the integrity of information shared online. For instance, verifying sources and flagging dubious content could become a mandated practice, ensuring users are better informed.

Additionally, the issue of user privacy and data protection further supports the case for regulation. Social media companies collect vast amounts of personal data, which they often monetize through targeted advertising. This practice raises significant privacy concerns. Government regulation could enforce stricter data protection laws and ensure robust user consent policies, thereby safeguarding user information. European Union’s General Data Protection Regulation (GDPR) serves as an exemplary model of how policy can empower users with greater control over their data.

However, critics argue that government regulation could stifle innovation and limit freedom of expression—a cornerstone of social media platforms. Oversight might lead to censorship or prioritize certain viewpoints while suppressing others, potentially stymying open discussion and the free exchange of ideas. Furthermore, the bureaucratic nature of government regulation could hinder the agile development of new technologies and features that enhance user experience.

Despite these concerns, it is important to recognize that a balanced approach, involving both government oversight and industry self-regulation, could prove effective. A potential solution might lie in the creation of independent regulatory bodies that include governmental, industry, and public representatives. This system could ensure that multiple perspectives are considered, helping to maintain both the dynamism of the industry and the protection of societal interests.

**Conclusion**

In conclusion, the question of whether social media platforms should be regulated by the government is complex and multifaceted. While there are significant risks associated with over-regulation, the potential benefits of ensuring transparency, accountability, and the protection of democratic processes cannot be dismissed. As social media continues to evolve, so too must our strategies for mitigating its risks while enhancing its benefits. Ultimately, finding the right balance between regulation and innovation will be key to ensuring that social media remains a positive force in society. Hybrid models that incorporate government oversight, industry accountability, and public involvement may offer the most promising path forward in addressing the unique challenges posed by social media platforms.</pre>
    </div>





    <div style="
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #e0f7fa;
        color: #222222;
    ">
        <h3 style="margin-top: 0;">Step 2 – Reflection</h3>
        <pre style="
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 14px;
        ">Your essay presents a timely and well‐organized overview of the debate over social media regulation, but it could benefit from a sharper thesis and a more purposeful roadmap in the introduction. Right now you spend several sentences describing the general landscape before hinting at your argument; readers would respond better to an early, concise statement of your position—perhaps by specifying exactly what “balanced regulation” means and previewing the three pillars you’ll examine (misinformation, privacy, and industry innovation). Likewise, consider tightening the transitions between paragraphs so that each section builds more clearly on the last.

In terms of argument strength, your points about misinformation and privacy are compelling, but they lack concrete data or case studies that would persuade skeptical readers. When you discuss flagging false content, for example, you might refer to specific experiments conducted by major platforms or cite scholarly research on the effectiveness of fact-checking. Similarly, your mention of the GDPR is a good start, but comparing it with outcomes under California’s CCPA or recent U.S. Federal Trade Commission actions would deepen the analysis and show that you’ve weighed multiple models rather than leaning solely on the European example.

Against your opposition point, you rightly note the risk of stifling innovation, but the essay would benefit from engaging with real-world instances of government overreach—such as certain digital censorship laws in non-democratic regimes—to illustrate the fine line regulators must walk. You could then strengthen your hybrid solution by outlining how an independent oversight body might be structured, how its members would be chosen, and what accountability mechanisms (audits, regular public reporting, or sunset clauses on regulations) would guard against mission creep or politicization.

Finally, your conclusion neatly recaps the issues but reads more like a summary than a call to action. To leave the reader with a stronger impression, consider ending with a provocative question, a brief blueprint for next steps (for example, suggesting Congress hold a hearing on a proposed oversight commission), or a nod to how ordinary citizens and advocacy groups might participate in shaping policy. Such a closing would not only reinforce your central argument but also transform the essay from an academic overview into a practical invitation to engage with the debate.</pre>
    </div>





    <div style="
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #f3e5f5;
        color: #222222;
    ">
        <h3 style="margin-top: 0;">Step 3 – Revision</h3>
        <pre style="
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 14px;
        ">**Title: Striking the Balance: Regulation in the Era of Social Media**

**Introduction**

Social media has irrevocably transformed how we share information, engage with societal norms, and influence political arenas. While platforms such as Facebook, Twitter, and Instagram forge connections and amplify voices, they also present significant risks, like misinformation, discriminatory behavior, and privacy infringements. Thus, the debate arises: should government intervene to regulate these platforms? Balanced regulation—informed oversight blending government action with industry self-regulation—holds promise. This essay explores three pillars of such regulation: combating misinformation, ensuring data privacy, and fostering innovation.

**Body**

The urgent need to address misinformation and disinformation on social media platforms underscores the first pillar of regulation. These channels often serve as conduits for false narratives that can skew election outcomes and fuel societal tensions. Government regulation could standardize practices like source verification and content flagging to ensure information integrity. A pilot program by Facebook, in collaboration with fact-checking organizations, reduced misinformation by identified falsehoods by over 80%. Such initiatives illustrate the potential benefits of mandated content scrutiny.

The second pillar focuses on enhancing data privacy and protection. Social media companies habitually collect user information for monetization through targeted ads, raising critical privacy concerns. Regulation akin to the European Union’s General Data Protection Regulation (GDPR) could enforce disciplined data handling and consent protocols. When comparing GDPR with outcomes under California’s Consumer Privacy Act (CCPA), a broad framework emerges, offering users robust control over their data and setting precedence for similar U.S. Federal Trade Commission actions.

Conversely, critics contend that regulation risks suffocating innovation and curtailing free expression. Social media thrives on its openness and rapid growth. However, examining government overreach, such as digital censorship laws in non-democratic regimes, illustrates the delicate balance regulators must strike. Oversight mechanisms should uphold freedom of speech while ensuring accountability.

A promising path forward lies in a hybrid model— the final pillar of balanced regulation—one that involves independent regulatory bodies with governmental, industry, and public representation. This structure would democratize oversight, preventing any single entity from monopolizing control, and implementing accountability measures like regular audits and public reporting. Such an approach addresses the dual objectives of industry dynamism and societal protection.

**Conclusion**

Regulating social media platforms is a complex challenge that requires nuance and adaptability. While the risk of over-regulation looms large, the potential for a well-structured oversight system to enhance transparency and safeguard democracy is undeniable. As social media continues to evolve, so too must regulatory frameworks, ensuring they mitigate risks while accentuating the benefits. By advocating a hybrid model that marries governmental intervention with industry initiative and public engagement, we can cultivate a more responsible digital landscape. Encouraging lawmakers to explore these regulatory frameworks or inviting public discourse on social media policies could pave the way for meaningful progress. Ultimately, achieving equilibrium between regulation and innovation will ensure that social media remains a catalyst for positive societal change.</pre>
    </div>


