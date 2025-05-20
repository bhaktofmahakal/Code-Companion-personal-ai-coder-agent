# Manus AI Agent Framework

A powerful AI agent framework that uses Ollama and codellama:7b-instruct to build applications autonomously. This implementation focuses on building a responsive blog platform with FastAPI, React, and TailwindCSS.

## Features

- 🤖 Autonomous task planning and execution
- 📝 Code generation and review
- 🔄 Continuous improvement through reflection
- 🌐 Modern web interface with real-time status updates
- 📦 File generation and management
- 🔍 Code validation and feedback

## Prerequisites

- Python 3.10.12
- Node.js 20.18.0
- Ollama with codellama:7b-instruct model
- Git

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd manus-agent
   ```

2. Set up the Python backend:
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. Set up the React frontend:
   ```bash
   cd frontend
   npm install
   ```

4. Start Ollama with codellama:7b-instruct:
   ```bash
   ollama run codellama:7b-instruct
   ```

## Running the Application

1. Start the backend server:
   ```bash
   # From the project root
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

2. Start the frontend development server:
   ```bash
   # From the frontend directory
   npm start
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## Usage

1. Open the frontend in your browser
2. Enter your goal in the input field (e.g., "Build a blog platform")
3. The agent will:
   - Generate a task plan
   - Execute tasks autonomously
   - Generate and review code
   - Provide downloadable files
   - Suggest improvements

## Project Structure

```
manus-agent/
├── backend/
│   ├── core/
│   │   └── ollama_client.py
│   ├── routes/
│   │   ├── planner.py
│   │   ├── executor.py
│   │   ├── memory.py
│   │   └── critic.py
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── tailwind.config.js
├── prompts/
│   ├── system.txt
│   ├── planner.txt
│   ├── executor.txt
│   ├── memory.txt
│   └── critic.txt
├── requirements.txt
└── README.md
```

## API Endpoints

- `POST /run-agent`: Run the agent with a goal
- `GET /status`: Check agent status
- `GET /files/{file_path}`: Download generated files
- `POST /planner/plan`: Generate task plan
- `POST /executor/execute`: Execute a task
- `POST /memory/reflect`: Reflect on past actions
- `POST /critic/review`: Review code output

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Ollama team for the amazing AI model
- FastAPI for the high-performance backend framework
- React and TailwindCSS for the beautiful frontend 