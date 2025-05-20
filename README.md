# 🧠 Code Companion

**Personal AI Coder Agent**

A powerful autonomous AI agent framework built with Ollama and CodeLlama:7B-Instruct, designed to plan, code, and improve software applications—starting with a responsive Blog Platform using FastAPI, HTML, and TailwindCSS.

---

## 🚀 Give your coding superpowers an AI upgrade – fully local, private, and open-source!

---

## 🎯 Key Features

* 🤖 **Autonomous Task Planning & Execution** — Just describe your goal, and let the agent do the work.
* 💡 **AI Code Generation & Review** — Generate backend, frontend, and logic in seconds.
* 🧠 **Self-Improving Critic & Reflection Loop** — Smart feedback cycles to optimize and revise.
* 🌐 **Modern Web UI** — Built with React + TailwindCSS to show real-time status and task flow.
* 📦 **Downloadable Code Files** — Easily view, edit, or run generated projects.
* 🔍 **Live Code Validation** — Backend checks and feedback via API endpoints.

---

## 📽️ Demo Video & Screenshots

<p align="center"> <a href="https://youtu.be/pDlP85JFjF4"> <img src="images\project.jpg" alt="Watch Demo" width="100%"/> </a> </p>


*click on the image.*

---

### ⚠️ **Performance Note (Important)**

      👉 **If the Code Companion AI is giving slow responses on your device, please note that the issue is not with the code.**  
      This usually happens when your device's RAM is under heavy load or your system lacks proper resources (RAM or GPU).
      
      - **Slow responses typically occur due to limited free RAM or background processes.**
      - **If the AI doesn't run at all, your system likely has less than 8GB of RAM or no suitable GPU.**
      - **✅ Recommended: Use a machine with at least 16GB RAM and a dedicated GPU (NVIDIA 6GB+ VRAM preferred) for optimal performance.**

---

🚀 **If you're using a high-end system with 16GB+ RAM, SSD storage, and a powerful GPU, you can switch to advanced local models such as:**

- `CodeLlama-13B-Instruct`
- `CodeLlama-34B-Instruct`
- `Deepseek-Coder-33B-Instruct`
- `WizardCoder-33B`
- *and other top-tier open-source coding models*

---

    ✅ **When using these advanced models on a capable system, this Code Companion project can perform at a level comparable to GPT-4.5 AI coding agents like Replit Ghostwriter, Devin AI, or Cursor AI.**



## 🛠️ Prerequisites

* Python 3.10.12
* Node.js 20.18.0
* Ollama installed with `codellama:7b-instruct` model
* Git

---

## ⚙️ Setup Instructions

1. Clone the Repository

   ```bash
   git clone https://github.com/bhaktofmahakal/Code-Companion-personal-ai-coder-agent.git
   cd Code-Companion-personal-ai-coder-agent
Backend Setup (FastAPI)

      python -m venv venv
      source venv/bin/activate  # Windows: venv\Scripts\activate

Frontend Setup (html + TailwindCSS)

      Start Ollama
      ollama run codellama:7b-instruct

Start Backend API

    uvicorn backend.main:app --host 0.0.0.0 --port 8000

🧪 How It Works
      
      Sample Input : “Build a blog platform”
      
      The agent will:
      
      Plan tasks using prompts
      
      Generate and execute code
      
      Review and improve the solution
      
      Provide downloadable output

🧠 AI Code Companion – Main Capabilities
      
      Code Generation
      
      Generates clean, well-documented code in any programming language based on your descriptions.
      
      Creates applications, functions, and algorithms tailored to your needs.
      
      Code Debugging
      
      Identifies errors and bugs in your code.
      
      Provides fixes and improved versions.
      
      Analyzes root causes to help you resolve issues effectively.
      
      Code Explanation
      
      Offers detailed, step-by-step explanations of code snippets.
      
      Clarifies purpose and functionality.
      
      Simplifies complex code and suggests improvements.
      
      Prompt Templates
      
      Uses specialized templates like:
      
      Manus AI Assistant: Content creation and problem solving.
      
      Agent Loop: Data processing and website creation.
      
      Modules: Advanced knowledge integration.
      
      User Interface Features
      
      Supports dark/light mode.
      
      Three modes: Generate, Debug, Explain.
      
      View prompt templates before use.
      
      Copy generated code easily.
      
      Chat interface with saved history.
      
      Technical Features
      
      Local LLM execution with Ollama.
      
      Powered by CodeLlama 7B for quality code understanding.
      
      FastAPI backend for scalability.
      
      Non-streaming response for stability.
      
      Static file serving and responsive design.
      
      Programming Language Support
      Includes JavaScript, Python, HTML/CSS, Bash, SQL, PHP, Ruby, Java, C/C++, Go, and more.
      
      Framework & Library Support
      Compatible with React, Vue, Angular, Node.js, Express, Django, Flask, pandas, numpy, testing tools, and ORMs.

🌍 Contributing

    We welcome contributions!

Fork this repository

      Create your feature branch: git checkout -b my-feature
      
      Commit changes: git commit -m 'Add feature'
      
      Push to branch: git push origin my-feature
      
      Create a Pull Request

📜 License

    Licensed under the MIT License. See LICENSE for details.

🙏 Acknowledgments

      💡 Ollama – Local LLM orchestration
      
      ⚡ FastAPI – Async Python API
      
      🎨 HTML + TailwindCSS – Frontend stack

