from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import requests
import os
import json

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "codellama:7b-instruct"
  # Using CodeLlama for code generation & debugging

# Directory containing prompt templates
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "Prompts")

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
    prompt: str = Form(...), 
    mode: str = Form(...),
    prompt_template: str = Form(None)
):
    headers = {"Content-Type": "application/json"}
    
    # If a prompt template is specified, load it from the file
    template_content = ""
    if prompt_template:
        try:
            template_path = os.path.join(PROMPTS_DIR, prompt_template)
            if os.path.exists(template_path) and os.path.isfile(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
        except Exception as e:
            print(f"Error loading prompt template: {str(e)}")
    
    # Define prompts based on mode (generate, debug, or explain)
    if mode == "generate":
        if template_content:
            full_prompt = f"{template_content}\n\nWrite a clean, well-documented {prompt} code snippet."
        else:
            full_prompt = f"Write a clean, well-documented {prompt} code snippet."
    elif mode == "debug":
        if template_content:
            full_prompt = f"{template_content}\n\nDebug and fix the following code:\n{prompt}"
        else:
            full_prompt = f"Debug and fix the following code:\n{prompt}"
    elif mode == "explain":
        if template_content:
            full_prompt = f"{template_content}\n\nExplain the following code in detail:\n```\n{prompt}\n```\n\nPlease include:\n1. What the code does overall\n2. How it works step by step\n3. Explanation of any complex or non-obvious parts\n4. Any potential issues or improvements\n\nFormat your explanation in clear, concise language that would help a beginner understand the code."
        else:
            full_prompt = f"""Explain the following code in detail:
```
{prompt}
```

Please include:
1. What the code does overall
2. How it works step by step
3. Explanation of any complex or non-obvious parts
4. Any potential issues or improvements

Format your explanation in clear, concise language that would help a beginner understand the code."""
    else:
        raise HTTPException(status_code=400, detail="Invalid mode selected.")

    try:
        # Send the request to Ollama without streaming (to avoid potential streaming issues)
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": full_prompt, "stream": False},
            headers=headers
        )
        
        # Check if the request was successful
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, 
                               detail=f"Ollama API returned error: {response.text}")
        
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
        raise HTTPException(status_code=500, 
                          detail=f"Request to Ollama failed: {str(e)}")
    except Exception as e:
        # Handle any other exceptions
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, 
                          detail=f"Error processing request: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
