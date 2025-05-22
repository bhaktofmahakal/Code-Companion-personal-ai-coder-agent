// Advanced features for AI Code Companion

// Modal controls
document.addEventListener('DOMContentLoaded', function() {
  // Advanced features modal
  if (document.getElementById('advanced-features')) {
    document.getElementById('advanced-features').addEventListener('click', function() {
      document.getElementById('advanced-modal').classList.remove('hidden');
      document.getElementById('advanced-modal').classList.add('flex');
    });
  }
  
  if (document.getElementById('close-advanced-modal')) {
    document.getElementById('close-advanced-modal').addEventListener('click', function() {
      document.getElementById('advanced-modal').classList.add('hidden');
      document.getElementById('advanced-modal').classList.remove('flex');
    });
  }
  
  // Template modal
  if (document.getElementById('close-template-modal')) {
    document.getElementById('close-template-modal').addEventListener('click', function() {
      document.getElementById('template-modal').classList.add('hidden');
      document.getElementById('template-modal').classList.remove('flex');
    });
  }
  
  // Feature buttons
  document.querySelectorAll('.feature-btn').forEach(button => {
    button.addEventListener('click', function() {
      const feature = this.getAttribute('data-feature');
      document.getElementById('mode').value = feature;
      document.getElementById('advanced-modal').classList.add('hidden');
      document.getElementById('advanced-modal').classList.remove('flex');
      
      if (feature === 'template') {
        document.getElementById('template-modal').classList.remove('hidden');
        document.getElementById('template-modal').classList.add('flex');
      } else {
        // Update placeholder based on selected feature
        updatePlaceholder();
      }
    });
  });
  
  // Save template
  if (document.getElementById('save-template')) {
    document.getElementById('save-template').addEventListener('click', async function() {
      const name = document.getElementById('template-name').value.trim();
      const content = document.getElementById('template-content').value.trim();
      
      if (!name || !content) {
        alert('Please provide both a name and content for your template.');
        return;
      }
      
      try {
        const formData = new FormData();
        formData.append('name', name);
        formData.append('content', content);
        
        const response = await fetch('/save_prompt_template', {
          method: 'POST',
          body: formData
        });
        
        if (!response.ok) {
          throw new Error('Failed to save template');
        }
        
        const data = await response.json();
        
        if (data.success) {
          alert('Template saved successfully!');
          document.getElementById('template-modal').classList.add('hidden');
          document.getElementById('template-modal').classList.remove('flex');
          
          // Refresh templates
          loadPromptTemplates();
        } else {
          throw new Error('Failed to save template');
        }
      } catch (error) {
        alert('Error: ' + error.message);
      }
    });
  }
  
  // Mode change handler
  if (document.getElementById('mode')) {
    document.getElementById('mode').addEventListener('change', updatePlaceholder);
    // Initialize placeholder
    updatePlaceholder();
  }
});

function updatePlaceholder() {
  const mode = document.getElementById('mode').value;
  const input = document.getElementById('code-input');
  
  switch (mode) {
    case 'generate':
      input.placeholder = 'Enter a description for code generation...';
      break;
    case 'debug':
      input.placeholder = 'Paste code for debugging...';
      break;
    case 'explain':
      input.placeholder = 'Paste code for explanation...';
      break;
    case 'analyze':
      input.placeholder = 'Paste code for analysis...';
      break;
    case 'test':
      input.placeholder = 'Paste code to generate tests for...';
      break;
    case 'security':
      input.placeholder = 'Paste code for security scanning...';
      break;
    case 'plan':
      input.placeholder = 'Describe a complex coding task to break down...';
      break;
    case 'project':
      input.placeholder = 'Describe the project you want to generate...';
      break;

    default:
      input.placeholder = 'Enter your request...';
  }
}

// Enhanced code processing function
async function processRequest() {
  const inputText = document.getElementById("code-input").value.trim();
  if (!inputText) return;
  
  const mode = document.getElementById("mode").value;
  const promptTemplate = document.getElementById("prompt-template").value;
  const language = document.getElementById("language") ? document.getElementById("language").value : "python";
  const chatContainer = document.getElementById("chat-container");
  
  // Add user message
  addMessage(inputText, 'user');
  
  // Clear input
  document.getElementById("code-input").value = '';
  
  // Add AI message with loading indicator
  const aiMessageId = 'ai-message-' + Date.now();
  addMessage('<div class="spinner mx-auto"></div>', 'ai', aiMessageId);
  
  // Scroll to bottom
  chatContainer.scrollTop = chatContainer.scrollHeight;
  
  try {
    // Prepare form data
    let formData = new FormData();
    
    // Add all possible parameters to ensure the server gets what it needs
    if (mode === 'debug' || mode === 'explain' || mode === 'analyze' || 
        mode === 'test' || mode === 'security' || mode === 'highlight' || 
        mode === 'share') {
      formData.append("code", inputText);
    }
    
    if (mode === 'generate') {
      formData.append("prompt", inputText);
    }
    
    if (mode === 'plan') {
      formData.append("task_description", inputText);
    }
    
    if (mode === 'project') {
      formData.append("project_spec", inputText);
    }
    
    // Always include these parameters
    formData.append("mode", mode);
    formData.append("language", language);
    
    if (promptTemplate) {
      formData.append("prompt_template", promptTemplate);
    }
    
    // For debugging
    console.log("Mode:", mode);
    console.log("Language:", language);
    console.log("Input text length:", inputText.length);
    
    let endpoint = "/generate_code"; // Default endpoint
    
    // Select endpoint based on mode
    switch (mode) {
      case 'generate':
      case 'debug':
      case 'explain':
        endpoint = "/generate_code";
        break;
      case 'analyze':
        endpoint = "/analyze_code";
        break;
      case 'test':
        endpoint = "/generate_tests";
        break;
      case 'security':
        endpoint = "/security_scan";
        break;
      case 'plan':
        endpoint = "/plan_implementation";
        break;
      case 'project':
        endpoint = "/generate_project";
        break;

    }
    
    // Send request
    let response = await fetch(endpoint, {
      method: "POST",
      body: formData
    });
    
    if (!response.ok) {
      updateMessage(aiMessageId, "Error: Failed to process the request. Please try again.");
      return;
    }
    
    let data = await response.json();
    let resultContent = "";
    
    // Process response based on mode
    switch (mode) {
      case 'generate':
      case 'debug':
      case 'explain':
        resultContent = formatCode(data.code);
        break;
      case 'analyze':
        resultContent = formatAnalysisResult(data);
        break;
      case 'test':
        resultContent = formatCode(data.tests);
        break;
      case 'security':
        resultContent = formatSecurityIssues(data.issues);
        break;
      case 'plan':
        resultContent = formatPlanSteps(data.steps);
        break;
      case 'project':
        resultContent = formatProjectResult(data);
        break;

    }
    
    updateMessage(aiMessageId, resultContent);
  } catch (error) {
    updateMessage(aiMessageId, "Error: " + error.message);
  }
  
  // Scroll to bottom again after content is loaded
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Format functions for different response types
function formatAnalysisResult(analysis) {
  let html = '<div class="space-y-4">';
  
  // Complexity
  html += `<div>
    <h3 class="font-bold mb-2">Complexity Score: ${analysis.complexity}</h3>
    <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
      <div class="bg-blue-600 h-2.5 rounded-full" style="width: ${Math.min(analysis.complexity * 10, 100)}%"></div>
    </div>
  </div>`;
  
  // Structure
  if (analysis.structure) {
    html += '<div>';
    html += '<h3 class="font-bold mb-2">Code Structure</h3>';
    html += '<ul class="list-disc pl-5 space-y-1">';
    
    if (analysis.structure.functions && analysis.structure.functions.length > 0) {
      html += `<li>Functions: ${analysis.structure.functions.length} (${analysis.structure.functions.join(', ')})</li>`;
    }
    
    if (analysis.structure.classes && analysis.structure.classes.length > 0) {
      html += `<li>Classes: ${analysis.structure.classes.length} (${analysis.structure.classes.join(', ')})</li>`;
    }
    
    if (analysis.structure.imports && analysis.structure.imports.length > 0) {
      html += `<li>Imports: ${analysis.structure.imports.length} (${analysis.structure.imports.join(', ')})</li>`;
    }
    
    if (analysis.structure.loc) {
      html += `<li>Lines of Code: ${analysis.structure.loc}</li>`;
    }
    
    html += '</ul>';
    html += '</div>';
  }
  
  // Suggestions
  if (analysis.suggestions && analysis.suggestions.length > 0) {
    html += '<div>';
    html += '<h3 class="font-bold mb-2">Suggestions</h3>';
    html += '<ul class="list-disc pl-5 space-y-1">';
    
    for (const suggestion of analysis.suggestions) {
      html += `<li>${suggestion}</li>`;
    }
    
    html += '</ul>';
    html += '</div>';
  }
  
  html += '</div>';
  return html;
}

function formatSecurityIssues(issues) {
  if (!issues || issues.length === 0) {
    return '<div class="p-4 bg-green-100 text-green-800 rounded-md">No security issues found!</div>';
  }
  
  let html = '<div class="space-y-4">';
  html += '<h3 class="font-bold mb-2">Security Issues Found</h3>';
  
  for (const issue of issues) {
    let severityColor = 'yellow';
    if (issue.severity === 'High') {
      severityColor = 'red';
    } else if (issue.severity === 'Low') {
      severityColor = 'green';
    }
    
    html += `<div class="p-4 bg-${severityColor}-100 text-${severityColor}-800 rounded-md">
      <div class="font-bold">${issue.type} (${issue.severity})</div>
      <p>${issue.description}</p>
    </div>`;
  }
  
  html += '</div>';
  return html;
}

function formatPlanSteps(steps) {
  let html = '<div class="space-y-4">';
  html += '<h3 class="font-bold mb-2">Implementation Plan</h3>';
  
  html += '<ol class="list-decimal pl-5 space-y-2">';
  for (const step of steps) {
    html += `<li>
      <div class="font-medium">${step.description}</div>
    </li>`;
  }
  html += '</ol>';
  
  html += '</div>';
  return html;
}

function formatProjectResult(data) {
  let html = '<div class="space-y-4">';
  html += '<h3 class="font-bold mb-2">Generated Project</h3>';
  
  html += '<div class="p-4 bg-green-100 text-green-800 rounded-md">';
  html += 'Project generated successfully with the following files:';
  html += '<ul class="list-disc pl-5 mt-2">';
  
  for (const file of data.files) {
    html += `<li>${file}</li>`;
  }
  
  html += '</ul>';
  html += '</div>';
  
  html += `<div class="mt-4">
    <a href="${data.download_url}" class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700" target="_blank">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
      </svg>
      Download Project
    </a>
  </div>`;
  
  html += '</div>';
  return html;
}



// Simple direct copy to clipboard function
window.copyToClipboard = function(button, text) {
  console.log("Copy button clicked");
  
  // Get the text to copy
  let textToCopy = text;
  
  // If no text was provided directly, try to find it
  if (!textToCopy) {
    // Check if it's a share URL button
    if (button.previousElementSibling && button.previousElementSibling.tagName === 'INPUT') {
      textToCopy = button.previousElementSibling.value;
      console.log("Found text in input field:", textToCopy.substring(0, 20) + "...");
    } 
    // Check if it's a highlighted code button
    else if (button.dataset.copyType === 'highlighted') {
      const container = button.closest('.highlight-container');
      if (container) {
        // Try to get the original code from data attribute
        textToCopy = container.getAttribute('data-original-code');
        if (!textToCopy) {
          // Try to get from pre element
          const preElement = container.querySelector('pre');
          if (preElement) {
            textToCopy = preElement.textContent;
          }
        }
      }
    }
    // Check if it's a regular code block
    else if (button.previousElementSibling && button.previousElementSibling.tagName === 'PRE') {
      textToCopy = button.previousElementSibling.textContent;
    }
  }
  
  // If we still don't have text, show an error
  if (!textToCopy) {
    alert("Could not find text to copy");
    return;
  }
  
  // Create a temporary textarea element
  const textarea = document.createElement('textarea');
  textarea.value = textToCopy;
  textarea.setAttribute('readonly', '');
  textarea.style.position = 'absolute';
  textarea.style.left = '-9999px';
  document.body.appendChild(textarea);
  
  // Select the text and copy it
  textarea.select();
  
  try {
    // Try to use the clipboard API first
    navigator.clipboard.writeText(textToCopy).then(function() {
      showCopiedMessage(button);
    }).catch(function() {
      // Fallback to execCommand
      const successful = document.execCommand('copy');
      if (successful) {
        showCopiedMessage(button);
      } else {
        alert("Copy failed. Please try again.");
      }
    });
  } catch (err) {
    // If clipboard API is not available, try execCommand
    try {
      const successful = document.execCommand('copy');
      if (successful) {
        showCopiedMessage(button);
      } else {
        alert("Copy failed. Please try again.");
      }
    } catch (err) {
      alert("Copy failed. Please try again.");
    }
  }
  
  // Clean up
  document.body.removeChild(textarea);
};

// Show "Copied!" message
function showCopiedMessage(button) {
  // Store original content
  const originalContent = button.innerHTML;
  const originalBackground = button.style.background;
  const originalColor = button.style.color;
  
  // Change button appearance
  button.innerHTML = "Copied!";
  button.style.background = "var(--button-bg)";
  button.style.color = "var(--button-text)";
  
  // Reset after 2 seconds
  setTimeout(function() {
    button.innerHTML = originalContent;
    if (originalBackground) button.style.background = originalBackground;
    if (originalColor) button.style.color = originalColor;
  }, 2000);
}
