# CV checker 
(or scanning, checking resume of candidate) using AI ;-)

This is my own exercise when studying the course  [LLM Engineering: Master AI, Large Language Models & Agents](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models)

How to use (MS Windows):
1. Install python for windows
2. Install Ollama for windows (and pull some models)

From command line:
```
ollama pull llama3.1:8b
ollama pull sailor2:8b
ollama pull deepseek-r1:8b
```
3.  From the command line:
```
git clone https://github.com/biennt/cvchecker.git
python -m venv cvchecker
pip install -r requirements.txt
python cvchecker
```
4. Using your browser to access http://127.0.0.1:7860/
(sample CVs are provided in cvdocs directory, just copy and paste the content)

Have fun!

BTW: also take a look at the cvscanner.py file, give it a shot
```
python cvscanner.py cvdocs
```

Run few times, do you see the different results between runs?

