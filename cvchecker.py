import gradio as gr
import requests
from openai import OpenAI
system_message = {
    "role": "system",
    "content": """You are a hiring assistant. 
                    It is your goal to evaluate the following resume, and provide me with a "Pass" or "Fail" response (only Pass or Fail, no other words or content), 
                     if the resume matches the type of candidate I'm looking for. The candidate I'm looking for must be fluent in Go, NodeJS, must know PSQL,
                     have at least 5 years of experience with software development, and have quite some cyber security knowledge, especially in the web field. 
                     The candidate who is in Asia is a plus. The resume to review is in user's prompt"""
}


def interface(MODEL, cvcontent):
    messages = [system_message]
    messages.append({"role":"user", "content":cvcontent})
    response = ollama_via_openai.chat.completions.create(model=MODEL, messages=messages)
    return_content = response.choices[0].message.content
    return return_content

def list_of_models():
    listofmodel = []
    try:
        response = requests.get(base_url + "/api/tags")
        api_data = response.json()
        models = api_data["models"]
        for model in models:
            listofmodel.append(model["name"])
    except requests.exceptions.Timeout:
        print("Error when connecting to local Ollama service")

    return listofmodel

## Main
api_key = "ollama"
base_url = "http://127.0.0.1:11434"
ollama_via_openai  = OpenAI(base_url = base_url + "/v1", api_key = api_key)
demo = gr.Interface(interface, [ gr.Dropdown(list_of_models(), label="Model", info="Select the LLM model to ask"), gr.Textbox("cvcontent")], outputs="text", title="Resume Checker")
demo.launch(share=False)
