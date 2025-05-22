from fastapi import FastAPI, HTTPException, Form, File, UploadFile, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import json
import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import shutil
from datetime import datetime

# Import utility functions
from utils import (
    analyze_code_structure, 
    generate_unit_tests, 
    check_security_issues,
    format_code_with_highlighting,
    break_down_task,
    generate_unique_id,
    store_shared_code,
    get_shared_code,
    save_user_template,
    analyze_project_structure,
    analyze_dependencies,
    create_zip_archive,
    generate_multiple_files
)

app = FastAPI(
    title="AI Code Companion API",
    description="API for the AI Code Companion application",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/shared_code", StaticFiles(directory="shared_code"), name="shared_code")
app.mount("/generated", StaticFiles(directory="generated"), name="generated")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "codellama:7b-instruct"
  # Using CodeLlama for code generation & debugging

# Directory containing prompt templates
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/prompts")
def get_prompts():
    """Get a list of available prompts from the Prompts directory"""
    try:
        prompt_files = []
        for file in os.listdir(PROMPTS_DIR):
            if file.endswith(".txt"):
                # Remove the .txt extension for display
                prompt_name = os.path.splitext(file)[0]
                prompt_files.append({"name": prompt_name, "file": file})
        return JSONResponse(content={"prompts": prompt_files})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving prompts: {str(e)}")

@app.get("/prompts/{prompt_file}")
def get_prompt_content(prompt_file: str):
    """Get the content of a specific prompt file"""
    try:
        # Ensure the file exists and is within the Prompts directory
        file_path = os.path.join(PROMPTS_DIR, prompt_file)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail=f"Prompt file not found: {prompt_file}")
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return JSONResponse(content={"content": content})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading prompt file: {str(e)}")

@app.post("/generate_code")
def generate_code(
    code: Optional[str] = Form(None),
    prompt: Optional[str] = Form(None), 
    mode: str = Form(...),
    language: str = Form(...),
    task_description: Optional[str] = Form(None),
    project_spec: Optional[str] = Form(None),
    prompt_template: Optional[str] = Form(None)
):
    """
    Generate, debug, or explain code based on the selected mode
    """
    headers = {"Content-Type": "application/json"}
    
    # Determine which input to use based on mode
    input_text = prompt or code or task_description or project_spec or ""
    
    # Print debug information
    print(f"Mode: {mode}, Language: {language}")
    print(f"Input text length: {len(input_text)}")
    
    # Define prompts based on mode (generate, debug, or explain)
    if mode == "generate":
        full_prompt = f"Write a clean, well-documented {language} code for: {input_text}"
    elif mode == "debug":
        full_prompt = f"Debug and fix the following {language} code:\n{input_text}"
    elif mode == "explain":
        full_prompt = f"""Explain the following {language} code in detail:
```
{input_text}
```

Please include:
1. What the code does overall
2. How it works step by step
3. Explanation of any complex or non-obvious parts
4. Any potential issues or improvements

Format your explanation in clear, concise language that would help a beginner understand the code."""
    else:
        # Return error response instead of raising exception
        return JSONResponse(
            content={"code": f"Invalid mode selected: {mode}"},
            status_code=400
        )

    try:
        # Send the request to Ollama without streaming (to avoid potential streaming issues)
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": full_prompt, "stream": False},
            headers=headers
        )
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Ollama API error: {response.status_code} - {response.text}")
            return JSONResponse(
                content={"code": f"Ollama API returned error: {response.text}"},
                status_code=200  # Return 200 to client but with error message
            )
        
        # Process the non-streaming response
        json_response = response.json()
        if "response" in json_response:
            return {"code": json_response["response"]}
        else:
            print("Unexpected response format:", json_response)
            return {"code": "No valid response received from Ollama."}

    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"Request to Ollama failed: {str(e)}")
        return JSONResponse(
            content={"code": f"Request to Ollama failed: {str(e)}"},
            status_code=200  # Return 200 to client but with error message
        )
    except Exception as e:
        # Handle any other exceptions
        print(f"Error processing request: {str(e)}")
        return JSONResponse(
            content={"code": f"Error processing request: {str(e)}"},
            status_code=200  # Return 200 to client but with error message
        )

# New endpoints for advanced features

@app.post("/analyze_code")
def analyze_code_endpoint(
    code: str = Form(...),
    language: str = Form("python")
):
    """
    Analyze code structure and provide insights
    """
    try:
        # Print debug information
        print(f"Analyzing code in language: {language}")
        print(f"Code length: {len(code)}")
        
        analysis = analyze_code_structure(code, language)
        return JSONResponse(content=analysis)
    except Exception as e:
        print(f"Error analyzing code: {str(e)}")
        return JSONResponse(
            content={"error": f"Error analyzing code: {str(e)}"},
            status_code=200  # Return 200 to client but with error message
        )

@app.post("/generate_tests")
def generate_tests_endpoint(
    code: str = Form(...),
    language: str = Form("python")
):
    """
    Generate unit tests for the provided code
    """
    try:
        # Print debug information
        print(f"Generating tests for language: {language}")
        print(f"Code length: {len(code)}")
        
        tests = generate_unit_tests(code, language)
        return JSONResponse(content={"tests": tests})
    except Exception as e:
        print(f"Error generating tests: {str(e)}")
        return JSONResponse(
            content={"tests": f"Error generating tests: {str(e)}"},
            status_code=200  # Return 200 to client but with error message
        )

@app.post("/security_scan")
def security_scan_endpoint(
    code: str = Form(...),
    language: str = Form("python")
):
    """
    Scan code for potential security issues
    """
    try:
        # Print debug information
        print(f"Security scanning for language: {language}")
        print(f"Code length: {len(code)}")
        
        issues = check_security_issues(code, language)
        return JSONResponse(content={"issues": issues})
    except Exception as e:
        print(f"Error scanning for security issues: {str(e)}")
        return JSONResponse(
            content={"issues": [{"type": "Error", "severity": "High", "description": f"Error scanning code: {str(e)}"}]},
            status_code=200  # Return 200 to client but with error message
        )

@app.post("/highlight_code")
def highlight_code_endpoint(
    code: str = Form(...),
    language: str = Form("python")
):
    """
    Format code with syntax highlighting
    """
    try:
        # Validate input
        if not code or len(code.strip()) == 0:
            raise ValueError("Code cannot be empty")
            
        # Clean up language string to ensure compatibility with Pygments
        language = language.lower().strip()
        
        # Map common language names to Pygments lexer names
        language_map = {
            "js": "javascript",
            "py": "python",
            "cs": "csharp",
            "ts": "typescript",
            "c++": "cpp",
            "html+css": "html",
            "html+js": "html"
        }
        
        if language in language_map:
            language = language_map[language]
            
        # Format the code with syntax highlighting
        highlighted = format_code_with_highlighting(code, language)
        
        # For debugging
        print(f"Highlighting result: {highlighted}")
        
        return JSONResponse(content=highlighted)
    except Exception as e:
        print(f"Highlighting error: {str(e)}")
        # Return a simple fallback instead of raising an error
        return JSONResponse(content={
            "html": f"<pre>{code}</pre>",
            "css": ""
        })

@app.post("/plan_implementation")
def plan_implementation_endpoint(
    task_description: str = Form(...)
):
    """
    Break down a complex coding task into steps
    """
    try:
        # Print debug information
        print(f"Planning implementation for task: {task_description[:100]}...")
        
        steps = break_down_task(task_description)
        return JSONResponse(content={"steps": steps})
    except Exception as e:
        print(f"Error planning implementation: {str(e)}")
        return JSONResponse(
            content={"steps": [{"step": 1, "description": f"Error planning implementation: {str(e)}"}]},
            status_code=200  # Return 200 to client but with error message
        )

@app.post("/share_code")
def share_code(
    code: str = Form(...),
    language: str = Form("python")
):
    """
    Generate a shareable link for code
    """
    try:
        # Validate input
        if not code or len(code.strip()) == 0:
            raise ValueError("Code cannot be empty")
            
        # Generate a unique ID for the shared code
        code_id = generate_unique_id()
        
        # Store the code with the ID
        store_shared_code(code_id, code, language)
        
        # For debugging
        print(f"Code shared with ID: {code_id}")
        
        # Return the shareable link
        return JSONResponse(content={
            "share_id": code_id,
            "share_url": f"/shared/{code_id}"
        })
    except Exception as e:
        print(f"Error sharing code: {str(e)}")
        # Return a simple error message instead of raising an exception
        return JSONResponse(content={
            "error": f"Error sharing code: {str(e)}"
        })

@app.get("/shared/{code_id}")
def get_shared_code_endpoint(code_id: str):
    """
    Retrieve shared code by ID
    """
    try:
        code_data = get_shared_code(code_id)
        if not code_data:
            return JSONResponse(content={"error": "Shared code not found"}, status_code=404)
        return JSONResponse(content=code_data)
    except Exception as e:
        print(f"Error retrieving shared code: {str(e)}")
        return JSONResponse(content={"error": f"Error retrieving shared code: {str(e)}"}, status_code=500)

@app.post("/save_template")
def save_prompt_template(
    template_name: str = Form(...),
    template_content: str = Form(...)
):
    """
    Save a custom prompt template
    """
    try:
        # Print debug information
        print(f"Saving template: {template_name}")
        print(f"Template content length: {len(template_content)}")
        
        # Validate input
        if not template_name or not template_content:
            raise ValueError("Template name and content are required")
            
        # Save the template
        template_path = save_user_template(template_name, template_content)
        
        return JSONResponse(content={
            "status": "success",
            "message": f"Template '{template_name}' saved successfully",
            "template_file": os.path.basename(template_path)
        })
    except Exception as e:
        print(f"Error saving template: {str(e)}")
        return JSONResponse(
            content={
                "status": "error",
                "message": f"Error saving template: {str(e)}"
            },
            status_code=200  # Return 200 to client but with error message
        )

@app.post("/analyze_project")
def analyze_project_endpoint(
    project_path: str = Form(...)
):
    """
    Analyze the structure of a project directory
    """
    try:
        # Print debug information
        print(f"Analyzing project at path: {project_path}")
        
        structure = analyze_project_structure(project_path)
        dependencies = analyze_dependencies(project_path)
        return JSONResponse(content={
            "structure": structure,
            "dependencies": dependencies
        })
    except Exception as e:
        print(f"Error analyzing project: {str(e)}")
        return JSONResponse(
            content={
                "structure": {"error": f"Error analyzing project: {str(e)}"},
                "dependencies": []
            },
            status_code=200  # Return 200 to client but with error message
        )

@app.post("/generate_project")
def generate_project_endpoint(
    project_spec: str = Form(...)
):
    """
    Generate a multi-file project based on a specification
    """
    try:
        # Print debug information
        print(f"Generating project from spec: {project_spec[:100]}...")
        
        files = generate_multiple_files(project_spec)
        zip_path = create_zip_archive(files)
        
        # Get the filename from the path
        filename = os.path.basename(zip_path)
        
        # Return a download link
        return JSONResponse(content={
            "download_url": f"/generated/{filename}",
            "files": list(files.keys())
        })
    except Exception as e:
        print(f"Error generating project: {str(e)}")
        return JSONResponse(
            content={
                "download_url": "",
                "files": [f"Error: {str(e)}"]
            },
            status_code=200  # Return 200 to client but with error message
        )

@app.get("/download/{filename}")
def download_file(filename: str):
    """
    Download a generated file
    """
    try:
        file_path = os.path.join("generated", filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {filename}")
        return FileResponse(file_path, filename=filename)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
