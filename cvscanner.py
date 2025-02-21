import sys
import os
import re
import requests
from prettytable import PrettyTable
from openai import OpenAI

system_message = {
    "role": "system",
    "content": """You are a hiring assistant. 
                    It is your goal to evaluate the following resume, 
                    and provide me with a score with range from 0 to 5 in a new separated line,
                    example of the response is 'SCORE: 3' with nothing before or after in the line.
                    The highest score means the most matched candidate. Respond to me in English.
                    The candidate I'm looking for must be fluent in Go, NodeJS, must know PSQL,
                    have at least 4 years of experience with software development, 
                    and have quite some cyber security knowledge, especially in the web field. 
                    The candidate also has to be located in Asia. The resume to review is in user's prompt"""
}

def search_multiline(text, pattern):
    regex = re.compile(pattern)
    lines = text.splitlines()
    returnstr = ""
    for line in lines:
        if regex.search(line):
            returnstr = line
    return returnstr

def cvcheck(cvfile, model):
    returnstr = ""
    if cvfile.endswith('.txt'):
        with open(cvfile, 'r', encoding="utf-8") as file:
            cvcontent = file.read()
            messages = [system_message]
            messages.append({"role":"user", "content":cvcontent})
            stream = ollama_via_openai.chat.completions.create(model=model, messages=messages, stream=True)
            response = ""
            print(f"------------: AI {model} response for {cvfile}:------------")
            for chunk in stream:
                word = chunk.choices[0].delta.content or ''
                response += word
                print(word,end='')
            print("")
            pattern = "SCORE: "
            returnstr = search_multiline(response, pattern)
            print(f"Final answer is: {returnstr}")
            print("------------: End of AI response :------------")
    return returnstr

    
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
final_result = []
api_key = "ollama"
base_url = "http://127.0.0.1:11434"
table = PrettyTable()
table.field_names = ["File", "model", "result"]

if len(sys.argv) < 2:
    print("You need to provide the directory contains CV(s)")
else:
    cvdir=sys.argv[1]
    print(f"Scanning the directory {cvdir}")
    ollama_via_openai  = OpenAI(base_url=base_url + "/v1", api_key=api_key)
    files = os.listdir(cvdir)
    for cvfile in files:
        for MODEL in list_of_models():
            chkresult = cvcheck(cvdir + "/" + cvfile, MODEL)
            table.add_row([cvfile, MODEL, chkresult])

print("FINAL REPORT:")
print(table)
print("END")
