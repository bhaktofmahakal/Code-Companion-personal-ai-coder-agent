import os
import json
import uuid
import zipfile
from io import BytesIO
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

# Code Analysis Functions
def analyze_code_structure(code, language="python"):
    """
    Analyze code structure and return insights
    """
    analysis = {
        "complexity": 0,
        "suggestions": [],
        "structure": {}
    }
    
    # Simple complexity analysis
    if language == "python":
        # Count indentation levels as a simple complexity metric
        lines = code.split('\n')
        max_indent = 0
        for line in lines:
            if line.strip() and not line.strip().startswith('#'):
                indent = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent // 4)
        
        analysis["complexity"] = max_indent
        
        # Basic structure analysis for Python
        functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code)
        classes = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:\(]', code)
        imports = re.findall(r'import\s+([a-zA-Z_][a-zA-Z0-9_]*)', code)
        imports.extend(re.findall(r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import', code))
        
        analysis["structure"] = {
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "loc": len(lines)
        }
        
        # Simple suggestions
        if max_indent > 4:
            analysis["suggestions"].append("Consider refactoring deeply nested code for better readability")
        if len(functions) > 10:
            analysis["suggestions"].append("Consider splitting into multiple modules for better organization")
    
    return analysis

def generate_unit_tests(code, language="python"):
    """
    Generate basic unit tests for the given code
    """
    if language == "python":
        # Extract function definitions
        functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):', code, re.DOTALL)
        
        tests = []
        for func_name, params in functions:
            # Skip if it looks like a private method or special method
            if func_name.startswith('_'):
                continue
                
            # Create a basic test for this function
            param_list = params.split(',')
            clean_params = []
            for p in param_list:
                p = p.strip()
                if p and not p.startswith('self'):
                    clean_params.append(p.split(':')[0].split('=')[0].strip())
            
            test_code = f"""
def test_{func_name}():
    # Arrange
    {"# TODO: Set up test parameters" if clean_params else "pass"}
    {f"# Parameters: {', '.join(clean_params)}" if clean_params else ""}
    
    # Act
    result = {func_name}({", ".join(["None" for _ in clean_params])})
    
    # Assert
    assert result is not None  # Replace with actual assertion
"""
            tests.append(test_code)
        
        if tests:
            full_test_code = "import pytest\n\n" + "\n".join(tests)
            return full_test_code
        else:
            return "# No testable functions found in the provided code"
    
    return "# Test generation not supported for this language yet"

def check_security_issues(code, language="python"):
    """
    Basic security check for common issues in code
    """
    issues = []
    
    if language == "python":
        # Check for potential SQL injection
        if re.search(r'execute\s*\(\s*[\'"][^\']*\%s[^\']*[\'"]\s*%\s*', code):
            issues.append({
                "type": "SQL Injection",
                "severity": "High",
                "description": "Possible SQL injection vulnerability detected. Use parameterized queries instead."
            })
        
        # Check for hardcoded credentials
        if re.search(r'password\s*=\s*[\'"][^\'"]+[\'"]\s*', code, re.IGNORECASE):
            issues.append({
                "type": "Hardcoded Credentials",
                "severity": "High",
                "description": "Hardcoded password detected. Use environment variables or a secure vault instead."
            })
        
        # Check for use of eval
        if re.search(r'eval\s*\(', code):
            issues.append({
                "type": "Code Injection",
                "severity": "High",
                "description": "Use of eval() detected, which can lead to code injection vulnerabilities."
            })
        
        # Check for pickle usage (potential deserialization issues)
        if re.search(r'import\s+pickle|from\s+pickle\s+import', code):
            issues.append({
                "type": "Unsafe Deserialization",
                "severity": "Medium",
                "description": "Use of pickle module detected. Be cautious with untrusted data."
            })
    
    return issues

def format_code_with_highlighting(code, language="python"):
    """
    Format code with syntax highlighting using Pygments
    """
    try:
        # Get the appropriate lexer for the language
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except Exception as lexer_error:
            print(f"Lexer error for language '{language}': {str(lexer_error)}")
            # Fallback to python if language not found
            lexer = get_lexer_by_name("python", stripall=True)
        
        # Use monokai style for better visibility
        formatter = HtmlFormatter(style="monokai", linenos=True, cssclass="source")
        result = highlight(code, lexer, formatter)
        
        # Get CSS for the highlighting
        css = HtmlFormatter(style="monokai").get_style_defs('.source')
        
        # Add some additional CSS to improve display
        css += """
        .source {
            background-color: #272822;
            padding: 0.5em;
            border-radius: 5px;
            margin: 1em 0;
            overflow-x: auto;
        }
        .source .linenos {
            color: #8f908a;
            padding-right: 0.8em;
            border-right: 1px solid #464741;
            text-align: right;
        }
        """
        
        return {"html": result, "css": css}
    except Exception as e:
        print(f"Error highlighting code: {str(e)}")
        # Fallback to simple pre tag if highlighting fails
        return {"html": f"<pre>{code}</pre>", "css": ""}

def break_down_task(task_description):
    """
    Break down a complex coding task into steps
    """
    # This is a simplified version - in a real implementation, 
    # this would use more sophisticated NLP or call the LLM
    steps = []
    
    # Basic task breakdown based on keywords
    if "api" in task_description.lower() or "endpoint" in task_description.lower():
        steps.append({"step": 1, "description": "Define API requirements and endpoints"})
        steps.append({"step": 2, "description": "Set up basic server structure"})
        steps.append({"step": 3, "description": "Implement data models"})
        steps.append({"step": 4, "description": "Implement API endpoints"})
        steps.append({"step": 5, "description": "Add error handling and validation"})
        steps.append({"step": 6, "description": "Test API endpoints"})
    
    elif "database" in task_description.lower() or "db" in task_description.lower():
        steps.append({"step": 1, "description": "Define database schema"})
        steps.append({"step": 2, "description": "Set up database connection"})
        steps.append({"step": 3, "description": "Implement data models"})
        steps.append({"step": 4, "description": "Create CRUD operations"})
        steps.append({"step": 5, "description": "Add data validation"})
        steps.append({"step": 6, "description": "Test database operations"})
    
    elif "ui" in task_description.lower() or "interface" in task_description.lower():
        steps.append({"step": 1, "description": "Define UI requirements and wireframes"})
        steps.append({"step": 2, "description": "Set up basic UI structure"})
        steps.append({"step": 3, "description": "Implement UI components"})
        steps.append({"step": 4, "description": "Add styling and layout"})
        steps.append({"step": 5, "description": "Implement user interactions"})
        steps.append({"step": 6, "description": "Test UI functionality"})
    
    else:
        # Generic software development steps
        steps.append({"step": 1, "description": "Analyze requirements"})
        steps.append({"step": 2, "description": "Design solution architecture"})
        steps.append({"step": 3, "description": "Implement core functionality"})
        steps.append({"step": 4, "description": "Add error handling and edge cases"})
        steps.append({"step": 5, "description": "Write tests"})
        steps.append({"step": 6, "description": "Refactor and optimize"})
    
    return steps

def generate_unique_id():
    """
    Generate a unique ID for sharing code
    """
    return str(uuid.uuid4())[:8]

def store_shared_code(share_id, code, language="python"):
    """
    Store shared code with the given ID
    """
    shared_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shared_code")
    os.makedirs(shared_dir, exist_ok=True)
    
    # Store code and metadata
    data = {
        "code": code,
        "language": language,
        "created_at": str(uuid.uuid1())  # Use timestamp-based UUID for creation time
    }
    
    with open(os.path.join(shared_dir, f"{share_id}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f)
    
    return True

def get_shared_code(share_id):
    """
    Retrieve shared code by ID
    """
    shared_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shared_code")
    file_path = os.path.join(shared_dir, f"{share_id}.json")
    
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data

def save_user_template(template_name, template_content):
    """
    Save a user-created prompt template
    """
    prompts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")
    os.makedirs(prompts_dir, exist_ok=True)
    
    # Sanitize filename
    safe_name = re.sub(r'[^\w\-\.]', '_', template_name)
    if not safe_name.endswith('.txt'):
        safe_name += '.txt'
    
    file_path = os.path.join(prompts_dir, safe_name)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template_content)
    
    return file_path

def analyze_project_structure(project_path):
    """
    Analyze the structure of a project directory
    """
    if not os.path.exists(project_path) or not os.path.isdir(project_path):
        return {"error": "Invalid project path"}
    
    structure = {"directories": [], "files": [], "summary": {}}
    file_types = {}
    
    for root, dirs, files in os.walk(project_path):
        # Skip hidden directories and files
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        rel_path = os.path.relpath(root, project_path)
        if rel_path == '.':
            rel_path = ''
        
        for dir_name in dirs:
            structure["directories"].append(os.path.join(rel_path, dir_name))
        
        for file_name in files:
            if not file_name.startswith('.'):
                file_path = os.path.join(rel_path, file_name)
                structure["files"].append(file_path)
                
                # Count file types
                ext = os.path.splitext(file_name)[1].lower()
                if ext:
                    file_types[ext] = file_types.get(ext, 0) + 1
    
    # Generate summary
    structure["summary"] = {
        "total_directories": len(structure["directories"]),
        "total_files": len(structure["files"]),
        "file_types": file_types
    }
    
    return structure

def analyze_dependencies(project_path):
    """
    Analyze project dependencies
    """
    dependencies = {"python": None, "javascript": None}
    
    # Check for Python dependencies
    requirements_path = os.path.join(project_path, "requirements.txt")
    pipfile_path = os.path.join(project_path, "Pipfile")
    setup_py_path = os.path.join(project_path, "setup.py")
    
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            content = f.read()
            dependencies["python"] = {"type": "requirements.txt", "dependencies": []}
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    dependencies["python"]["dependencies"].append(line)
    
    elif os.path.exists(pipfile_path):
        dependencies["python"] = {"type": "Pipfile", "dependencies": "Pipfile detected, but detailed parsing not implemented"}
    
    elif os.path.exists(setup_py_path):
        dependencies["python"] = {"type": "setup.py", "dependencies": "setup.py detected, but detailed parsing not implemented"}
    
    # Check for JavaScript dependencies
    package_json_path = os.path.join(project_path, "package.json")
    if os.path.exists(package_json_path):
        try:
            with open(package_json_path, "r", encoding="utf-8") as f:
                package_data = json.load(f)
                dependencies["javascript"] = {
                    "type": "package.json",
                    "dependencies": package_data.get("dependencies", {}),
                    "devDependencies": package_data.get("devDependencies", {})
                }
        except json.JSONDecodeError:
            dependencies["javascript"] = {"type": "package.json", "error": "Invalid JSON format"}
    
    return dependencies

def create_zip_archive(files):
    """
    Create a ZIP archive from a dictionary of files
    files should be a dict with {filename: content}
    """
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path, content in files.items():
            zip_file.writestr(file_path, content)
    
    zip_buffer.seek(0)
    
    # Save the zip file to disk
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated")
    os.makedirs(output_dir, exist_ok=True)
    
    zip_path = os.path.join(output_dir, f"project_{generate_unique_id()}.zip")
    with open(zip_path, "wb") as f:
        f.write(zip_buffer.getvalue())
    
    return zip_path

def generate_multiple_files(project_spec):
    """
    Generate multiple files based on a project specification
    This is a simplified version - in a real implementation,
    this would use more sophisticated NLP or call the LLM
    """
    files = {}
    
    # Simple example for a basic Flask API
    if "flask" in project_spec.lower() and "api" in project_spec.lower():
        files["app.py"] = """from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"})

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
"""
        files["requirements.txt"] = "flask==2.0.1\n"
        files["README.md"] = """# Flask API

A simple Flask API with basic endpoints.

## Setup

```
pip install -r requirements.txt
python app.py
```

## Endpoints

- GET /api/hello - Returns a hello message
- POST /api/echo - Echoes back the JSON payload
"""
    
    # Simple example for a basic React app
    elif "react" in project_spec.lower():
        files["index.html"] = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>React App</title>
</head>
<body>
    <div id="root"></div>
    <script src="https://unpkg.com/react@17/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@17/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script type="text/babel" src="app.js"></script>
</body>
</html>"""
        files["app.js"] = """const App = () => {
    const [count, setCount] = React.useState(0);
    
    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>React Counter App</h1>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>Increment</button>
            <button onClick={() => setCount(count - 1)}>Decrement</button>
        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('root'));"""
        files["README.md"] = """# React Counter App

A simple React app with a counter.

## Usage

Open index.html in a web browser.
"""
    
    # Default - simple HTML/CSS/JS project
    else:
        files["index.html"] = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Web Project</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>Hello, World!</h1>
        <p>This is a simple web project.</p>
        <button id="clickMe">Click Me</button>
        <p id="result"></p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""
        files["styles.css"] = """body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}

.container {
    width: 80%;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
}

button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}"""
        files["script.js"] = """document.getElementById('clickMe').addEventListener('click', function() {
    document.getElementById('result').textContent = 'Button clicked at ' + new Date().toLocaleTimeString();
});"""
        files["README.md"] = """# Simple Web Project

A basic HTML, CSS, and JavaScript project.

## Usage

Open index.html in a web browser.
"""
    
    return files