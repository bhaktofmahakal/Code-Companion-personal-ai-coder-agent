🧠 Code Companion – Personal AI Coder Agent
A powerful autonomous AI agent framework built with Ollama and CodeLlama:7B-Instruct, designed to plan, code, and improve software applications—starting with a responsive Blog Platform using FastAPI, React, and TailwindCSS.


🚀 Give your coding superpowers an AI upgrade – fully local, private, and open-source!

🎯 Key Features

      🤖 Autonomous Task Planning & Execution – Just describe your goal, and let the agent do the work.
      
      💡 AI Code Generation & Review – Generate backend, frontend, and logic in seconds.
      
      🧠 Self-Improving Critic & Reflection Loop – Smart feedback cycles to optimize and revise.
      
      🌐 Modern Web UI – Built with React + TailwindCSS to show real-time status and task flow.
      
      📦 Downloadable Code Files – Easily view, edit, or run generated projects.
      
      🔍 Live Code Validation – Backend checks and feedback via API endpoints.

📽️ Demo Video & Screenshots
<p align="center"> <a href="/images/samle.mp4"> <img src="images/sample.mp4" alt="Watch Demo" width="100%"/> </a> </p>
📷 Screenshots will be added soon inside the images/ folder.

🛠️ Prerequisites
      
      Python 3.10.12
      
      Node.js 20.18.0
      
      Ollama installed with codellama:7b-instruct model
      
      Git

⚙️ Setup Instructions

      1. Clone the Repository
      
      git clone https://github.com/bhaktofmahakal/Code-Companion-personal-ai-coder-agent.git
      cd Code-Companion-personal-ai-coder-agent
      2. Backend Setup (FastAPI)
      
      python -m venv venv
      source venv/bin/activate      # Windows: venv\Scripts\activate
      pip install -r requirements.txt
      3. Frontend Setup (React + TailwindCSS)
      
      cd frontend
      npm install
      4. Start Ollama
      
      ollama run codellama:7b-instruct
      ▶️ Running the Application
      Start Backend API
      
      uvicorn backend.main:app --host 0.0.0.0 --port 8000


🧪 How It Works

      Input a goal: “Build a blog platform”
      
      The agent will:
      
      Plan tasks using prompts
      
      Generate and execute code
      
      Review and improve the solution
      
      Provide downloadable output

🌍 Contributing
      
      We welcome contributions! Here's how:
      
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
      
      🎨 Html + TailwindCSS – frontend stack

