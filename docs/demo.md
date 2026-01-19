---
title: Interactive Demo
description: "Try nestedutils Python library in your browser. No installation required. Test dot-notation access to nested dictionaries and lists. Safely get, set, delete, and check existence of values in complex nested data structures."
keywords:
  - interactive demo
  - test nested data access
  - online nested utils
  - try nestedutils
  - browser demo
  - test dot notation
  - validate nested paths
  - test get_at set_at
  - nested dictionary demo
  - nested list demo
---

# Interactive Demo

Try the `nestedutils` library directly in your browser! This page uses [Pyodide](https://pyodide.org/) to run Python in the browser.

<div id="package-info" style="display: none; margin: 20px 0; padding: 15px; background: #e3f2fd; border-left: 4px solid #1976d2; border-radius: 4px;">
  <p style="margin: 0;"><strong>Installed package:</strong> <code>nestedutils</code> <span id="package-version"></span></p>
</div>

<div id="pyodide-loading" style="text-align: center; padding: 20px;">
  <p>Loading Pyodide...</p>
  <div class="spinner"></div>
</div>

<div id="test-interface" style="display: none;">
  <div class="test-section">
    <h3>Current Data Structure</h3>
    <p style="color: #666; font-size: 0.9em; margin-bottom: 10px;">This is your working data structure. All operations will modify this structure.</p>
    <div id="data-display" style="padding: 15px; background: #f5f5f5; border-radius: 4px; font-family: monospace; white-space: pre-wrap; max-height: 300px; overflow-y: auto; border: 1px solid #e0e0e0;"></div>
    <div style="margin-top: 10px; display: flex; gap: 10px;">
      <button 
        id="reset-btn" 
        style="padding: 8px 16px; background: #757575; color: white; border: none; border-radius: 4px; cursor: pointer;"
      >
        Reset to Empty
      </button>
      <button 
        id="load-example-btn" 
        style="padding: 8px 16px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer;"
      >
        Load Example Data
      </button>
    </div>
  </div>

  <div class="test-section" style="margin-top: 30px;">
    <h3>1. Get Value (get_at)</h3>
    <p>Retrieve a value from the nested data structure using dot notation:</p>
    <div style="display: flex; gap: 10px; margin-bottom: 10px; flex-wrap: wrap;">
      <input 
        type="text" 
        id="get-path" 
        placeholder="e.g., user.profile.name or items.0.title"
        style="flex: 1; min-width: 250px; padding: 8px; border: 1px solid #ccc; border-radius: 4px;"
      />
      <input 
        type="text" 
        id="get-default" 
        placeholder="Default value (optional)"
        style="flex: 0 0 150px; padding: 8px; border: 1px solid #ccc; border-radius: 4px;"
      />
      <button 
        id="get-btn" 
        style="padding: 8px 16px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer;"
      >
        Get Value
      </button>
    </div>
    <div id="get-result" style="margin-top: 10px; padding: 10px; background: #f5f5f5; border-radius: 4px; min-height: 30px;"></div>
  </div>

  <div class="test-section" style="margin-top: 30px;">
    <h3>2. Set Value (set_at)</h3>
    <p>Set a value in the nested data structure. Missing containers will be created automatically:</p>
    <div style="display: flex; gap: 10px; margin-bottom: 10px; flex-wrap: wrap;">
      <input 
        type="text" 
        id="set-path" 
        placeholder="e.g., user.profile.email or items.2.name"
        style="flex: 1; min-width: 200px; padding: 8px; border: 1px solid #ccc; border-radius: 4px;"
      />
      <input 
        type="text" 
        id="set-value" 
        placeholder="Value to set"
        style="flex: 1; min-width: 150px; padding: 8px; border: 1px solid #ccc; border-radius: 4px;"
      />
      <select 
        id="set-strategy" 
        style="flex: 0 0 120px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; background: white;"
      >
        <option value="auto">auto</option>
        <option value="none">none</option>
        <option value="dict">dict</option>
        <option value="list">list</option>
      </select>
      <button 
        id="set-btn" 
        style="padding: 8px 16px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer;"
      >
        Set Value
      </button>
    </div>
    <p style="color: #666; font-size: 0.85em; margin-top: 5px;">
      <strong>Fill Strategy:</strong> <code>auto</code> (smart defaults), <code>none</code> (fill gaps with None), 
      <code>dict</code> (always create dicts), <code>list</code> (always create lists)
    </p>
    <div id="set-result" style="margin-top: 10px; padding: 10px; background: #f5f5f5; border-radius: 4px; min-height: 30px;"></div>
  </div>

  <div class="test-section" style="margin-top: 30px;">
    <h3>3. Check Existence (exists_at)</h3>
    <p>Check if a path exists in the nested data structure:</p>
    <div style="display: flex; gap: 10px; margin-bottom: 10px;">
      <input 
        type="text" 
        id="exists-path" 
        placeholder="e.g., user.profile.name or items.0.title"
        style="flex: 1; padding: 8px; border: 1px solid #ccc; border-radius: 4px;"
      />
      <button 
        id="exists-btn" 
        style="padding: 8px 16px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer;"
      >
        Check
      </button>
    </div>
    <div id="exists-result" style="margin-top: 10px; padding: 10px; background: #f5f5f5; border-radius: 4px; min-height: 30px;"></div>
  </div>

  <div class="test-section" style="margin-top: 30px;">
    <h3>4. Delete Value (delete_at)</h3>
    <p>Delete a value from the nested data structure:</p>
    <div style="display: flex; gap: 10px; margin-bottom: 10px; flex-wrap: wrap;">
      <input 
        type="text" 
        id="delete-path" 
        placeholder="e.g., user.profile.email or items.1"
        style="flex: 1; min-width: 200px; padding: 8px; border: 1px solid #ccc; border-radius: 4px;"
      />
      <label style="display: flex; align-items: center; gap: 5px; padding: 8px;">
        <input type="checkbox" id="delete-allow-list" />
        <span style="font-size: 0.9em;">Allow list mutation</span>
      </label>
      <button 
        id="delete-btn" 
        style="padding: 8px 16px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer;"
      >
        Delete
      </button>
    </div>
    <div id="delete-result" style="margin-top: 10px; padding: 10px; background: #f5f5f5; border-radius: 4px; min-height: 30px;"></div>
  </div>

</div>

<style>
  .test-section {
    border: 1px solid #e0e0e0;
    padding: 20px;
    border-radius: 8px;
    background: white;
  }
  
  .spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #1976d2;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .result-success {
    color: #2e7d32;
    font-weight: bold;
  }
  
  .result-error {
    color: #c62828;
    font-weight: bold;
  }
  
  .result-info {
    color: #1976d2;
  }
  
  button:hover {
    background: #1565c0 !important;
  }
  
  button:active {
    background: #0d47a1 !important;
  }
  
  #reset-btn:hover {
    background: #616161 !important;
  }
  
  #reset-btn:active {
    background: #424242 !important;
  }
  
  select {
    cursor: pointer;
  }
  
  select:focus, input:focus {
    outline: 2px solid #1976d2;
    outline-offset: 2px;
  }
</style>

<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>

<script type="text/javascript">
  let pyodide;

  async function main() {
    // Load Pyodide
    pyodide = await loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/"
    });
    
    // Update loading message
    document.getElementById("pyodide-loading").innerHTML = "<p>Installing nestedutils package...</p>";
    
    // Install nestedutils package
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install("nestedutils");
    
    // Import functions and initialize data
    pyodide.runPython(`
      from nestedutils import get_at, set_at, delete_at, exists_at
      import json
      
      # Initialize data structure
      data = {}
      
      # Try to get package version
      try:
          import importlib.metadata
          package_version = importlib.metadata.version('nestedutils')
      except:
          try:
              import importlib_metadata
              package_version = importlib_metadata.version('nestedutils')
          except:
              package_version = "unknown"
    `);
    
    const packageVersion = pyodide.globals.get("package_version");
    
    // Display package version
    if (packageVersion && packageVersion !== "unknown") {
      document.getElementById("package-version").textContent = `v${packageVersion}`;
      document.getElementById("package-info").style.display = "block";
    }
    
    // Initialize data structure display
    updateDataDisplay();
    
    // Hide loading, show interface
    document.getElementById("pyodide-loading").style.display = "none";
    document.getElementById("test-interface").style.display = "block";
    
    // Setup event listeners
    setupEventListeners();
  }

  function updateDataDisplay() {
    try {
      const json = pyodide.runPython(`json.dumps(data, indent=2)`);
      document.getElementById("data-display").textContent = json || "{}";
    } catch (error) {
      document.getElementById("data-display").textContent = "Error displaying data";
    }
  }

  function setupEventListeners() {
    // Reset data
    document.getElementById("reset-btn").addEventListener("click", () => {
      pyodide.runPython(`data = {}`);
      updateDataDisplay();
      clearResults();
    });
    
    // Load example data
    document.getElementById("load-example-btn").addEventListener("click", () => {
      pyodide.runPython(`
        data = {
          "user": {
            "name": "John Doe",
            "age": 30,
            "profile": {
              "email": "john@example.com",
              "bio": "Software developer"
            }
          },
          "items": [
            {"id": 1, "title": "First Item", "tags": ["python", "demo"]},
            {"id": 2, "title": "Second Item", "tags": ["javascript"]}
          ],
          "settings": {
            "theme": "dark",
            "notifications": True
          }
        }
      `);
      updateDataDisplay();
      clearResults();
    });
    
    // Get value
    document.getElementById("get-btn").addEventListener("click", async () => {
      const path = document.getElementById("get-path").value.trim();
      const defaultValue = document.getElementById("get-default").value.trim();
      const resultDiv = document.getElementById("get-result");
      
      if (!path) {
        resultDiv.innerHTML = '<span class="result-error">Please enter a path</span>';
        return;
      }
      
      try {
        resultDiv.innerHTML = '<span class="result-info">Processing...</span>';
        
        let code = `get_at(data, ${JSON.stringify(path)}`;
        if (defaultValue) {
          // Try to parse as appropriate type
          let defaultVal = defaultValue;
          if (defaultValue === "null" || defaultValue === "None") {
            defaultVal = null;
          } else if (!isNaN(defaultValue) && defaultValue !== "") {
            defaultVal = Number(defaultValue);
          } else if (defaultValue === "true" || defaultValue === "True") {
            defaultVal = true;
          } else if (defaultValue === "false" || defaultValue === "False") {
            defaultVal = false;
          }
          code += `, default=${JSON.stringify(defaultVal)}`;
        }
        code += `)`;
        
        const result = pyodide.runPython(code);
        
        // Format the result for display
        let resultStr;
        try {
          resultStr = pyodide.runPython(`json.dumps(${JSON.stringify(result)})`);
        } catch (e) {
          resultStr = String(result);
        }
        
        if (result === null || result === undefined) {
          resultDiv.innerHTML = `<span class="result-info">Result: <code>null</code></span>`;
        } else {
          resultDiv.innerHTML = `<span class="result-success">Value found:</span><br><code style="background: white; padding: 5px; border-radius: 3px; display: inline-block; margin-top: 5px; font-family: monospace;">${escapeHtml(resultStr)}</code>`;
        }
      } catch (error) {
        resultDiv.innerHTML = `<span class="result-error">Error: ${escapeHtml(error.message)}</span>`;
      }
    });
    
    // Set value
    document.getElementById("set-btn").addEventListener("click", async () => {
      const path = document.getElementById("set-path").value.trim();
      const value = document.getElementById("set-value").value.trim();
      const strategy = document.getElementById("set-strategy").value;
      const resultDiv = document.getElementById("set-result");
      
      if (!path || value === "") {
        resultDiv.innerHTML = '<span class="result-error">Please enter a path and value</span>';
        return;
      }
      
      try {
        resultDiv.innerHTML = '<span class="result-info">Processing...</span>';
        
        // Try to parse value as appropriate type
        let parsedValue = value;
        if (value === "null" || value === "None") {
          parsedValue = null;
        } else if (!isNaN(value) && value !== "") {
          parsedValue = Number(value);
        } else if (value === "true" || value === "True") {
          parsedValue = true;
        } else if (value === "false" || value === "False") {
          parsedValue = false;
        } else {
          // Try to parse as JSON array or object
          try {
            parsedValue = JSON.parse(value);
          } catch (e) {
            // Keep as string
            parsedValue = value;
          }
        }
        
        pyodide.runPython(`set_at(data, ${JSON.stringify(path)}, ${JSON.stringify(parsedValue)}, fill_strategy=${JSON.stringify(strategy)})`);
        updateDataDisplay();
        resultDiv.innerHTML = `<span class="result-success">✓ Value set successfully</span>`;
      } catch (error) {
        resultDiv.innerHTML = `<span class="result-error">Error: ${escapeHtml(error.message)}</span>`;
      }
    });
    
    // Check existence
    document.getElementById("exists-btn").addEventListener("click", async () => {
      const path = document.getElementById("exists-path").value.trim();
      const resultDiv = document.getElementById("exists-result");
      
      if (!path) {
        resultDiv.innerHTML = '<span class="result-error">Please enter a path</span>';
        return;
      }
      
      try {
        resultDiv.innerHTML = '<span class="result-info">Processing...</span>';
        const exists = pyodide.runPython(`exists_at(data, ${JSON.stringify(path)})`);
        
        if (exists) {
          resultDiv.innerHTML = `<span class="result-success">✓ Path exists</span>`;
        } else {
          resultDiv.innerHTML = `<span class="result-info">Path does not exist</span>`;
        }
      } catch (error) {
        resultDiv.innerHTML = `<span class="result-error">Error: ${escapeHtml(error.message)}</span>`;
      }
    });
    
    // Delete value
    document.getElementById("delete-btn").addEventListener("click", async () => {
      const path = document.getElementById("delete-path").value.trim();
      const allowListMutation = document.getElementById("delete-allow-list").checked;
      const resultDiv = document.getElementById("delete-result");
      
      if (!path) {
        resultDiv.innerHTML = '<span class="result-error">Please enter a path</span>';
        return;
      }
      
      try {
        resultDiv.innerHTML = '<span class="result-info">Processing...</span>';
        const deleted = pyodide.runPython(`delete_at(data, ${JSON.stringify(path)}, allow_list_mutation=${allowListMutation})`);
        updateDataDisplay();
        
        // Format the deleted value for display
        let deletedStr;
        try {
          deletedStr = pyodide.runPython(`json.dumps(${JSON.stringify(deleted)})`);
        } catch (e) {
          // If JSON serialization fails, convert to string
          deletedStr = String(deleted);
        }
        
        resultDiv.innerHTML = `<span class="result-success">✓ Value deleted:</span><br><code style="background: white; padding: 5px; border-radius: 3px; display: inline-block; margin-top: 5px; font-family: monospace;">${escapeHtml(deletedStr)}</code>`;
      } catch (error) {
        resultDiv.innerHTML = `<span class="result-error">Error: ${escapeHtml(error.message)}</span>`;
      }
    });
    
    // Allow Enter key to trigger actions
    document.getElementById("get-path").addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        document.getElementById("get-btn").click();
      }
    });
    
    document.getElementById("set-path").addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        document.getElementById("set-btn").click();
      }
    });
    
    document.getElementById("exists-path").addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        document.getElementById("exists-btn").click();
      }
    });
    
    document.getElementById("delete-path").addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        document.getElementById("delete-btn").click();
      }
    });
  }

  function clearResults() {
    document.getElementById("get-result").innerHTML = "";
    document.getElementById("set-result").innerHTML = "";
    document.getElementById("exists-result").innerHTML = "";
    document.getElementById("delete-result").innerHTML = "";
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  // Start loading Pyodide when page is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      main().catch(err => {
        document.getElementById("pyodide-loading").innerHTML = 
          `<p style="color: #c62828;">Error loading Pyodide: ${err.message}</p>`;
        console.error(err);
      });
    });
  } else {
    main().catch(err => {
      document.getElementById("pyodide-loading").innerHTML = 
        `<p style="color: #c62828;">Error loading Pyodide: ${err.message}</p>`;
      console.error(err);
    });
  }
</script>
