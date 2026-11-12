# OMID AI 🤖
**An Autonomous Multi-Agent Software Engineering System running on Android (Termux).**

OMID AI is a fully functional, lightweight AI agent system built entirely on a smartphone. It uses Groq (or OpenRouter) to orchestrate a team of specialized AI agents (Manager, Developer, Reviewer, QC) to automatically write, test, and package Python projects.

## 🚀 Features
- **Multi-Agent Architecture:** 10 specialized agents working together.
- **Autonomous Runner:** Runs in the background without needing a web browser.
- **Live Code Editor:** Watch the AI write code in real-time with syntax highlighting.
- **Auto-Debug:** Tests the code and fixes errors automatically.
- **Reviewer Agent:** Reviews the code for logical bugs before finishing.
- **Multi-File Projects:** Creates complex projects with `main.py` and `utils.py`.
- **ZIP Download:** Download the entire generated project with one click.

## 📱 How to Run (Termux)
1. Install Termux and Ubuntu (proot-distro).
2. Clone this repository.
3. Install requirements: `pip install -r requirements.txt`
4. Set your API key: `export GROQ_API_KEY="your_key"`
5. Start the Web Dashboard: `uvicorn web_ui:app --host 0.0.0.0 --port 8000`
6. Start Autonomous Mode: `python3 autonomous_runner.py goal.txt`

## 🛠️ Built With
- Python, FastAPI, Tailwind CSS, SSE, Groq (LLaMA 3), Ubuntu proot.

*Built with ❤️ by OMID.*
