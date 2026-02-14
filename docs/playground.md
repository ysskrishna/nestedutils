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

# Interactive Playground

Try the `nestedutils` library directly in your browser! This page uses [Pyodide](https://pyodide.org/) to run Python in the browser.

<div id="pyodide-loading" style="text-align: center; padding: 40px 20px;">
  <div class="spinner"></div>
  <p style="margin-top: 15px; color: #666;">Loading Pyodide...</p>
</div>

<div id="playground-container" style="display: none;">
  <!-- Package Info Banner -->
  <div id="package-info" style="display: none; margin-bottom: 20px; padding: 12px 16px; background: #e3f2fd; border-left: 4px solid #1976d2; border-radius: 4px;">
    <span style="font-weight: 500;">Installed:</span> <code>nestedutils</code> <span id="package-version" style="font-weight: 600; color: #1976d2;"></span>
  </div>

  <!-- Main Layout -->
  <div class="playground-layout">
    <!-- Left Panel - Data Viewer -->
    <div class="data-panel">
      <div class="panel-header">
        <span class="panel-title">Data</span>
        <div class="example-buttons">
          <button class="example-btn active" data-example="example1">Config File</button>
          <button class="example-btn" data-example="example2">API Response</button>
          <button class="example-btn" data-example="example3">Event Log</button>
          <button class="example-btn" data-example="custom">Custom</button>
        </div>
      </div>

      <div class="json-editor-container">
        <div id="json-status" class="json-status"></div>
        <textarea
          id="custom-json-input"
          class="json-editor"
          placeholder='Enter valid JSON here, e.g., {"key": "value"}'
          spellcheck="false"
        ></textarea>
        <div id="json-error" class="json-error"></div>
      </div>

      <!-- Stats Bar -->
      <div class="stats-bar">
        <div class="stat-item">
          <span class="stat-label">Depth</span>
          <span class="stat-value" id="stat-depth">-</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Leaves</span>
          <span class="stat-value" id="stat-leaves">-</span>
        </div>
      </div>
    </div>

    <!-- Right Panel - Operations -->
    <div class="ops-panel">
      <div class="ops-tabs">
        <button class="ops-tab active" data-op="get_at">get_at</button>
        <button class="ops-tab" data-op="set_at">set_at</button>
        <button class="ops-tab" data-op="exists_at">exists_at</button>
        <button class="ops-tab" data-op="delete_at">delete_at</button>
        <button class="ops-tab" data-op="get_depth">get_depth</button>
        <button class="ops-tab" data-op="count_leaves">count_leaves</button>
        <button class="ops-tab" data-op="get_all_paths">get_all_paths</button>
      </div>

      <div class="ops-content">
        <!-- get_at Section -->
        <div class="op-section active" data-op="get_at">
          <h3 class="op-title">Get Value</h3>
          <p class="op-description">Retrieve a value from the nested data structure using dot notation.</p>

          <div class="form-group">
            <label class="form-label">Path</label>
            <input type="text" id="get-path" class="form-input" placeholder="e.g., user.profile.email" />
            <p class="form-hint">Use dot notation. For arrays: items.0.title</p>
          </div>

          <div class="form-group">
            <label class="form-label">Default Value (optional)</label>
            <input type="text" id="get-default" class="form-input" placeholder="Value if path not found" />
            <p class="form-hint">If omitted and path doesn't exist, raises PathError</p>
          </div>

          <button id="get-btn" class="execute-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            Execute
          </button>

          <div class="code-preview">
            <div class="code-preview-header">
              <span>Python Code</span>
              <button class="copy-btn" onclick="copyCode('get_at')">Copy</button>
            </div>
            <div class="code-preview-body" id="get-code-preview">
              <span class="code-fn">get_at</span>(data, <span class="code-str">"path"</span>)
            </div>
          </div>

          <div id="get-result" class="result-panel"></div>
        </div>

        <!-- set_at Section -->
        <div class="op-section" data-op="set_at">
          <h3 class="op-title">Set Value</h3>
          <p class="op-description">Set a value in the nested data structure at the specified path.</p>

          <div class="form-group">
            <label class="form-label">Path</label>
            <input type="text" id="set-path" class="form-input" placeholder="e.g., user.profile.bio" />
          </div>

          <div class="form-group">
            <label class="form-label">Value</label>
            <input type="text" id="set-value" class="form-input" placeholder="Value to set" />
          </div>

          <div class="form-group">
            <label class="checkbox-group">
              <input type="checkbox" id="set-create" checked />
              <span>Create missing containers (create=True)</span>
            </label>
          </div>

          <button id="set-btn" class="execute-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            Execute
          </button>

          <div class="code-preview">
            <div class="code-preview-header">
              <span>Python Code</span>
              <button class="copy-btn" onclick="copyCode('set_at')">Copy</button>
            </div>
            <div class="code-preview-body" id="set-code-preview">
              <span class="code-fn">set_at</span>(data, <span class="code-str">"path"</span>, value, <span class="code-param">create</span>=<span class="code-bool">True</span>)
            </div>
          </div>

          <div id="set-result" class="result-panel"></div>
        </div>

        <!-- exists_at Section -->
        <div class="op-section" data-op="exists_at">
          <h3 class="op-title">Check Existence</h3>
          <p class="op-description">Check if a path exists in the nested data structure.</p>

          <div class="form-group">
            <label class="form-label">Path</label>
            <input type="text" id="exists-path" class="form-input" placeholder="e.g., user.profile.email" />
          </div>

          <button id="exists-btn" class="execute-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            Execute
          </button>

          <div class="code-preview">
            <div class="code-preview-header">
              <span>Python Code</span>
              <button class="copy-btn" onclick="copyCode('exists_at')">Copy</button>
            </div>
            <div class="code-preview-body" id="exists-code-preview">
              <span class="code-fn">exists_at</span>(data, <span class="code-str">"path"</span>)
            </div>
          </div>

          <div id="exists-result" class="result-panel"></div>
        </div>

        <!-- delete_at Section -->
        <div class="op-section" data-op="delete_at">
          <h3 class="op-title">Delete Value</h3>
          <p class="op-description">Delete a value from the nested data structure.</p>

          <div class="form-group">
            <label class="form-label">Path</label>
            <input type="text" id="delete-path" class="form-input" placeholder="e.g., user.profile.email" />
          </div>

          <div class="form-group">
            <label class="checkbox-group">
              <input type="checkbox" id="delete-allow-list" />
              <span>Allow list mutation (allow_list_mutation=True)</span>
            </label>
          </div>

          <button id="delete-btn" class="execute-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            Execute
          </button>

          <div class="code-preview">
            <div class="code-preview-header">
              <span>Python Code</span>
              <button class="copy-btn" onclick="copyCode('delete_at')">Copy</button>
            </div>
            <div class="code-preview-body" id="delete-code-preview">
              <span class="code-fn">delete_at</span>(data, <span class="code-str">"path"</span>)
            </div>
          </div>

          <div id="delete-result" class="result-panel"></div>
        </div>

        <!-- get_depth Section -->
        <div class="op-section" data-op="get_depth">
          <h3 class="op-title">Get Depth</h3>
          <p class="op-description">Get the maximum nesting depth of your data structure.</p>

          <button id="depth-btn" class="execute-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            Execute
          </button>

          <div class="code-preview">
            <div class="code-preview-header">
              <span>Python Code</span>
              <button class="copy-btn" onclick="copyCode('get_depth')">Copy</button>
            </div>
            <div class="code-preview-body" id="depth-code-preview">
              <span class="code-fn">get_depth</span>(data)
            </div>
          </div>

          <div id="depth-result" class="result-panel"></div>
        </div>

        <!-- count_leaves Section -->
        <div class="op-section" data-op="count_leaves">
          <h3 class="op-title">Count Leaves</h3>
          <p class="op-description">Count the total number of leaf values (non-container values) in your data.</p>

          <button id="leaves-btn" class="execute-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            Execute
          </button>

          <div class="code-preview">
            <div class="code-preview-header">
              <span>Python Code</span>
              <button class="copy-btn" onclick="copyCode('count_leaves')">Copy</button>
            </div>
            <div class="code-preview-body" id="leaves-code-preview">
              <span class="code-fn">count_leaves</span>(data)
            </div>
          </div>

          <div id="leaves-result" class="result-panel"></div>
        </div>

        <!-- get_all_paths Section -->
        <div class="op-section" data-op="get_all_paths">
          <h3 class="op-title">Get All Paths</h3>
          <p class="op-description">Get all paths to leaf values in your data structure.</p>

          <button id="paths-btn" class="execute-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            Execute
          </button>

          <div class="code-preview">
            <div class="code-preview-header">
              <span>Python Code</span>
              <button class="copy-btn" onclick="copyCode('get_all_paths')">Copy</button>
            </div>
            <div class="code-preview-body" id="paths-code-preview">
              <span class="code-fn">get_all_paths</span>(data)
            </div>
          </div>

          <div id="paths-result" class="result-panel"></div>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  /* Spinner */
  .spinner {
    border: 4px solid #e0e0e0;
    border-top: 4px solid #1976d2;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Main Layout - Top/Bottom */
  .playground-layout {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  /* Data Panel */
  .data-panel {
    background: #263238;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .panel-header {
    padding: 12px 16px;
    background: #1e272c;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
  }

  .panel-title {
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #90a4ae;
  }

  .example-buttons {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }

  .example-btn {
    padding: 5px 10px;
    background: transparent;
    border: 1px solid #455a64;
    color: #b0bec5;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.75rem;
    transition: all 0.2s;
  }

  .example-btn:hover {
    background: #37474f;
    border-color: #607d8b;
  }

  .example-btn.active {
    background: #1976d2;
    color: white;
    border-color: #1976d2;
  }

  /* JSON Editor */
  .json-editor-container {
    display: flex;
    flex-direction: column;
    position: relative;
    height: 280px;
  }

  .json-status {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 0.75rem;
    font-weight: 500;
    z-index: 1;
    padding: 3px 8px;
    border-radius: 4px;
  }

  .json-status.valid {
    background: rgba(76, 175, 80, 0.2);
    color: #81c784;
  }

  .json-status.invalid {
    background: rgba(244, 67, 54, 0.2);
    color: #e57373;
  }

  .json-editor {
    flex: 1;
    width: 100%;
    padding: 16px;
    padding-top: 40px;
    background: #263238;
    border: none;
    color: #eceff1;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.85rem;
    line-height: 1.6;
    resize: none;
    outline: none;
    overflow: auto;
  }

  .json-editor::placeholder {
    color: #546e7a;
  }

  .json-error {
    padding: 8px 16px;
    font-size: 0.75rem;
    color: #e57373;
    background: #1e272c;
    font-family: monospace;
    min-height: 32px;
  }

  /* Stats Bar */
  .stats-bar {
    padding: 10px 16px;
    background: #1e272c;
    display: flex;
    gap: 20px;
    border-top: 1px solid #37474f;
  }

  .stat-item {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .stat-label {
    font-size: 0.7rem;
    color: #78909c;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .stat-value {
    background: #37474f;
    padding: 2px 10px;
    border-radius: 4px;
    color: #80cbc4;
    font-weight: 600;
    font-size: 0.8rem;
    font-family: monospace;
  }

  /* Operations Panel */
  .ops-panel {
    background: white;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .ops-tabs {
    display: flex;
    background: #fafafa;
    border-bottom: 1px solid #e0e0e0;
    overflow-x: auto;
    flex-shrink: 0;
  }

  .ops-tab {
    padding: 12px 16px;
    background: transparent;
    border: none;
    color: #757575;
    cursor: pointer;
    font-size: 0.8rem;
    font-weight: 500;
    font-family: 'Monaco', 'Menlo', monospace;
    border-bottom: 2px solid transparent;
    white-space: nowrap;
    transition: all 0.2s;
  }

  .ops-tab:hover {
    color: #424242;
    background: #f5f5f5;
  }

  .ops-tab.active {
    color: #1976d2;
    border-bottom-color: #1976d2;
    background: white;
  }

  .ops-content {
    flex: 1;
    overflow: auto;
    padding: 20px;
  }

  .op-section {
    display: none;
  }

  .op-section.active {
    display: block;
  }

  .op-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0 0 6px 0;
    color: #212121;
  }

  .op-description {
    color: #757575;
    font-size: 0.9rem;
    margin: 0 0 20px 0;
  }

  /* Form Elements */
  .form-group {
    margin-bottom: 16px;
  }

  .form-label {
    display: block;
    font-size: 0.75rem;
    font-weight: 600;
    color: #616161;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .form-input {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    font-size: 0.9rem;
    font-family: 'Monaco', 'Menlo', monospace;
    transition: border-color 0.2s, box-shadow 0.2s;
    background: white;
  }

  .form-input:focus {
    outline: none;
    border-color: #1976d2;
    box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
  }

  .form-input::placeholder {
    color: #bdbdbd;
  }

  .form-hint {
    font-size: 0.75rem;
    color: #9e9e9e;
    margin: 6px 0 0 0;
  }

  .checkbox-group {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    background: #fafafa;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.85rem;
    color: #616161;
  }

  .checkbox-group input {
    width: 16px;
    height: 16px;
    cursor: pointer;
  }

  /* Execute Button */
  .execute-btn {
    width: 100%;
    padding: 12px 16px;
    background: #1976d2;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }

  .execute-btn:hover {
    background: #1565c0;
  }

  .execute-btn:active {
    transform: scale(0.98);
  }

  /* Code Preview */
  .code-preview {
    margin-top: 16px;
    background: #263238;
    border-radius: 6px;
    overflow: hidden;
  }

  .code-preview-header {
    padding: 8px 12px;
    background: #1e272c;
    color: #90a4ae;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .copy-btn {
    padding: 3px 8px;
    background: #37474f;
    border: none;
    color: #b0bec5;
    border-radius: 3px;
    cursor: pointer;
    font-size: 0.65rem;
    text-transform: uppercase;
  }

  .copy-btn:hover {
    background: #455a64;
  }

  .code-preview-body {
    padding: 12px;
    font-family: 'Monaco', 'Menlo', monospace;
    font-size: 0.85rem;
    color: #eceff1;
    overflow-x: auto;
  }

  .code-fn {
    color: #82aaff;
  }

  .code-str {
    color: #c3e88d;
  }

  .code-param {
    color: #ffcb6b;
  }

  .code-bool {
    color: #c792ea;
  }

  .code-num {
    color: #f78c6c;
  }

  /* Result Panel */
  .result-panel {
    margin-top: 16px;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid #e0e0e0;
    min-height: 50px;
  }

  .result-panel:empty {
    display: none;
  }

  .result-panel .result-header {
    padding: 8px 12px;
    background: #fafafa;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #757575;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .result-panel .result-body {
    padding: 12px;
    font-family: 'Monaco', 'Menlo', monospace;
    font-size: 0.85rem;
    background: white;
  }

  .result-success {
    color: #2e7d32;
  }

  .result-error {
    color: #c62828;
  }

  .result-info {
    color: #1976d2;
  }

  .result-value {
    background: #f5f5f5;
    padding: 8px 12px;
    border-radius: 4px;
    margin-top: 8px;
    display: block;
    word-break: break-all;
  }

  .result-status {
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 0.65rem;
    font-weight: 600;
  }

  .result-status.success {
    background: #e8f5e9;
    color: #2e7d32;
  }

  .result-status.error {
    background: #ffebee;
    color: #c62828;
  }

  .paths-list {
    margin: 8px 0 0 0;
    padding: 0 0 0 20px;
    max-height: 200px;
    overflow-y: auto;
  }

  .paths-list li {
    padding: 4px 0;
    font-family: monospace;
    font-size: 0.8rem;
    color: #424242;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .json-editor-container {
      height: 220px;
    }

    .ops-tab {
      padding: 10px 12px;
      font-size: 0.75rem;
    }

    .panel-header {
      flex-direction: column;
      align-items: flex-start;
    }

    .example-buttons {
      width: 100%;
    }
  }
</style>

<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>

<script type="text/javascript">
  let pyodide;
  let appliedJsonString = "";
  let autoApplyTimer = null;
  let currentCodeStrings = {};

  async function main() {
    // Load Pyodide
    pyodide = await loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/"
    });

    // Update loading message
    document.getElementById("pyodide-loading").innerHTML = '<div class="spinner"></div><p style="margin-top: 15px; color: #666;">Installing nestedutils package...</p>';

    // Install nestedutils package
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install("nestedutils");

    // Import functions and initialize data
    pyodide.runPython(`
      from nestedutils import get_at, set_at, delete_at, exists_at, get_depth, count_leaves, get_all_paths
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

    // Hide loading, show interface
    document.getElementById("pyodide-loading").style.display = "none";
    document.getElementById("playground-container").style.display = "block";

    // Load default example
    loadExampleData("example1");

    // Setup event listeners
    setupEventListeners();
  }

  function updateDataDisplay(syncTextarea = false) {
    if (syncTextarea) {
      try {
        const json = pyodide.runPython(`json.dumps(data, indent=2)`);
        const jsonStr = json || "{}";
        document.getElementById("custom-json-input").value = jsonStr;
        appliedJsonString = JSON.stringify(JSON.parse(jsonStr));
        document.getElementById("json-error").textContent = "";
        updateJsonStatus(true);
        updateStats();
      } catch (error) {
        console.error("Error updating display:", error);
      }
    }
  }

  function updateStats() {
    try {
      const depth = pyodide.runPython(`get_depth(data)`);
      const leaves = pyodide.runPython(`count_leaves(data)`);

      document.getElementById("stat-depth").textContent = depth;
      document.getElementById("stat-leaves").textContent = leaves;
    } catch (e) {
      document.getElementById("stat-depth").textContent = "-";
      document.getElementById("stat-leaves").textContent = "-";
    }
  }

  function hasUnsavedChanges() {
    const jsonInput = document.getElementById("custom-json-input").value.trim();

    if (!jsonInput) {
      return appliedJsonString !== "" && appliedJsonString !== "{}";
    }

    if (jsonInput === "{}" || jsonInput === "[]") {
      return jsonInput !== appliedJsonString;
    }

    try {
      const normalized = JSON.stringify(JSON.parse(jsonInput));
      return normalized !== appliedJsonString;
    } catch {
      return true;
    }
  }

  function applyJsonData() {
    const jsonInput = document.getElementById("custom-json-input").value.trim();
    const errorDiv = document.getElementById("json-error");

    if (!jsonInput) {
      updateJsonStatus(false, "Empty");
      errorDiv.textContent = "Please enter JSON data";
      return;
    }

    let parsedData;
    try {
      parsedData = JSON.parse(jsonInput);
    } catch (error) {
      updateJsonStatus(false, "Invalid");
      errorDiv.textContent = `Invalid JSON: ${error.message}`;
      return;
    }

    if (typeof parsedData !== "object" || parsedData === null) {
      updateJsonStatus(false, "Invalid");
      errorDiv.textContent = "JSON must be an object {} or array []";
      return;
    }

    try {
      const jsonStr = JSON.stringify(parsedData);
      pyodide.runPython(`data = json.loads(${JSON.stringify(jsonStr)})`);
      appliedJsonString = jsonStr;
      clearResults();
      updateJsonStatus(true, "Applied");
      errorDiv.textContent = "";
      updateStats();

      // Update example buttons
      document.querySelectorAll('.example-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelector('.example-btn[data-example="custom"]').classList.add('active');
    } catch (error) {
      updateJsonStatus(false, "Error");
      errorDiv.textContent = `Error: ${error.message}`;
    }
  }

  function updateJsonStatus(isValid, message = null) {
    const statusDiv = document.getElementById("json-status");

    if (message) {
      statusDiv.textContent = message;
      statusDiv.className = `json-status ${isValid ? 'valid' : 'invalid'}`;
    } else if (isValid === true) {
      statusDiv.textContent = "Valid";
      statusDiv.className = "json-status valid";
    } else if (isValid === false) {
      statusDiv.textContent = "Invalid";
      statusDiv.className = "json-status invalid";
    } else {
      statusDiv.textContent = "";
      statusDiv.className = "json-status";
    }
  }

  function loadExampleData(exampleType) {
    let exampleCode = "";

    switch(exampleType) {
      case "example1":
        // Config File - Deep nesting with various types
        exampleCode = `
data = {
  "app": {
    "name": "MyApp",
    "version": "2.0.1",
    "debug": False
  },
  "database": {
    "primary": {
      "host": "localhost",
      "port": 5432,
      "credentials": {
        "username": "admin",
        "password": None
      }
    },
    "replica": {
      "host": "replica.db.local",
      "port": 5432,
      "readonly": True
    }
  },
  "features": {
    "authentication": {
      "enabled": True,
      "providers": ["google", "github", "email"],
      "session_timeout": 3600
    },
    "analytics": {
      "enabled": False,
      "tracking_id": None
    }
  },
  "logging": {
    "level": "info",
    "outputs": ["console", "file"]
  }
}`;
        break;
      case "example2":
        // API Response - Paginated data with metadata
        exampleCode = `
data = {
  "status": "success",
  "data": {
    "users": [
      {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com",
        "profile": {
          "avatar": "https://example.com/alice.jpg",
          "bio": "Software Engineer"
        },
        "roles": ["admin", "user"],
        "active": True
      },
      {
        "id": 2,
        "username": "bob",
        "email": "bob@example.com",
        "profile": {
          "avatar": None,
          "bio": "Product Manager"
        },
        "roles": ["user"],
        "active": False
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total_pages": 5,
      "total_items": 42
    }
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2025-02-14T10:30:00Z"
  }
}`;
        break;
      case "example3":
        // Event Log - Timestamped events with varying structures
        exampleCode = `
data = {
  "events": [
    {
      "id": "evt_001",
      "type": "user.login",
      "timestamp": "2025-02-14T09:00:00Z",
      "data": {
        "user_id": 42,
        "ip_address": "192.168.1.100",
        "device": {"type": "mobile", "os": "iOS"}
      },
      "success": True
    },
    {
      "id": "evt_002",
      "type": "payment.processed",
      "timestamp": "2025-02-14T09:15:00Z",
      "data": {
        "order_id": "ORD-789",
        "amount": 99.99,
        "currency": "USD",
        "method": {"type": "card", "last4": "4242"}
      },
      "success": True
    },
    {
      "id": "evt_003",
      "type": "email.sent",
      "timestamp": "2025-02-14T09:20:00Z",
      "data": {
        "to": "user@example.com",
        "subject": "Order Confirmation",
        "template": "order_confirmation_v2"
      },
      "success": False,
      "error": {"code": "SMTP_TIMEOUT", "message": "Connection timed out"}
    }
  ],
  "summary": {
    "total": 3,
    "successful": 2,
    "failed": 1
  }
}`;
        break;
      case "custom":
        // Clear data for fresh start
        pyodide.runPython(`data = {}`);
        document.getElementById("custom-json-input").value = "{}";
        appliedJsonString = "{}";
        clearResults();
        updateStats();
        updateJsonStatus(true);
        document.getElementById("json-error").textContent = "";
        document.querySelectorAll('.example-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelector('.example-btn[data-example="custom"]').classList.add('active');
        return;
    }

    if (exampleCode) {
      pyodide.runPython(exampleCode);
      updateDataDisplay(true);
      clearResults();

      // Update example buttons
      document.querySelectorAll('.example-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelector(`.example-btn[data-example="${exampleType}"]`).classList.add('active');
    }
  }

  function setupEventListeners() {
    // Example buttons
    document.querySelectorAll('.example-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        loadExampleData(btn.dataset.example);
      });
    });

    // Operation tabs
    document.querySelectorAll('.ops-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.ops-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.op-section').forEach(s => s.classList.remove('active'));

        tab.classList.add('active');
        document.querySelector(`.op-section[data-op="${tab.dataset.op}"]`).classList.add('active');
      });
    });

    // JSON editor
    document.getElementById("custom-json-input").addEventListener("input", () => {
      const jsonInput = document.getElementById("custom-json-input").value.trim();
      const errorDiv = document.getElementById("json-error");

      if (autoApplyTimer) {
        clearTimeout(autoApplyTimer);
        autoApplyTimer = null;
      }

      if (!jsonInput) {
        updateJsonStatus(null);
        errorDiv.textContent = "";
        return;
      }

      let isValid = false;
      try {
        const parsed = JSON.parse(jsonInput);
        if (typeof parsed !== "object" || parsed === null) {
          updateJsonStatus(false);
          errorDiv.textContent = "JSON must be an object {} or array []";
        } else {
          updateJsonStatus(true);
          errorDiv.textContent = "";
          isValid = true;
        }
      } catch (error) {
        updateJsonStatus(false);
        errorDiv.textContent = `Invalid JSON: ${error.message}`;
      }

      if (isValid) {
        autoApplyTimer = setTimeout(() => {
          if (hasUnsavedChanges()) {
            applyJsonData();
          }
        }, 1000);
      }
    });

    // Update code previews on input
    document.getElementById("get-path").addEventListener("input", updateGetCodePreview);
    document.getElementById("get-default").addEventListener("input", updateGetCodePreview);
    document.getElementById("set-path").addEventListener("input", updateSetCodePreview);
    document.getElementById("set-value").addEventListener("input", updateSetCodePreview);
    document.getElementById("set-create").addEventListener("change", updateSetCodePreview);
    document.getElementById("exists-path").addEventListener("input", updateExistsCodePreview);
    document.getElementById("delete-path").addEventListener("input", updateDeleteCodePreview);
    document.getElementById("delete-allow-list").addEventListener("change", updateDeleteCodePreview);

    // Get value
    document.getElementById("get-btn").addEventListener("click", async () => {
      const path = document.getElementById("get-path").value.trim();
      const defaultValue = document.getElementById("get-default").value.trim();
      const resultDiv = document.getElementById("get-result");

      if (!path) {
        showResult(resultDiv, "error", "Please enter a path");
        return;
      }

      try {
        showResult(resultDiv, "info", "Processing...");

        let code = `get_at(data, ${JSON.stringify(path)}`;
        if (defaultValue) {
          let defaultVal = parseValue(defaultValue);
          code += `, default=${JSON.stringify(defaultVal)}`;
        }
        code += `)`;

        currentCodeStrings['get_at'] = code;
        const result = pyodide.runPython(code);

        let resultStr;
        try {
          resultStr = pyodide.runPython(`json.dumps(${JSON.stringify(result)})`);
        } catch (e) {
          resultStr = String(result);
        }

        showResult(resultDiv, "success", "Value found", resultStr);
      } catch (error) {
        showResult(resultDiv, "error", error.message);
      }
    });

    // Set value
    document.getElementById("set-btn").addEventListener("click", async () => {
      const path = document.getElementById("set-path").value.trim();
      const value = document.getElementById("set-value").value.trim();
      const create = document.getElementById("set-create").checked;
      const resultDiv = document.getElementById("set-result");

      if (!path || value === "") {
        showResult(resultDiv, "error", "Please enter a path and value");
        return;
      }

      try {
        showResult(resultDiv, "info", "Processing...");

        let parsedValue = parseValue(value);
        const code = `set_at(data, ${JSON.stringify(path)}, ${JSON.stringify(parsedValue)}, create=${create ? 'True' : 'False'})`;
        currentCodeStrings['set_at'] = code;

        pyodide.runPython(code);
        updateDataDisplay(true);
        showResult(resultDiv, "success", "Value set successfully");
      } catch (error) {
        showResult(resultDiv, "error", error.message);
      }
    });

    // Check existence
    document.getElementById("exists-btn").addEventListener("click", async () => {
      const path = document.getElementById("exists-path").value.trim();
      const resultDiv = document.getElementById("exists-result");

      if (!path) {
        showResult(resultDiv, "error", "Please enter a path");
        return;
      }

      try {
        showResult(resultDiv, "info", "Processing...");
        const code = `exists_at(data, ${JSON.stringify(path)})`;
        currentCodeStrings['exists_at'] = code;
        const exists = pyodide.runPython(code);

        if (exists) {
          showResult(resultDiv, "success", "Path exists", "True");
        } else {
          showResult(resultDiv, "info", "Path does not exist", "False");
        }
      } catch (error) {
        showResult(resultDiv, "error", error.message);
      }
    });

    // Delete value
    document.getElementById("delete-btn").addEventListener("click", async () => {
      const path = document.getElementById("delete-path").value.trim();
      const allowListMutation = document.getElementById("delete-allow-list").checked;
      const resultDiv = document.getElementById("delete-result");

      if (!path) {
        showResult(resultDiv, "error", "Please enter a path");
        return;
      }

      try {
        showResult(resultDiv, "info", "Processing...");
        const code = `delete_at(data, ${JSON.stringify(path)}, allow_list_mutation=${allowListMutation ? 'True' : 'False'})`;
        currentCodeStrings['delete_at'] = code;
        const deleted = pyodide.runPython(code);
        updateDataDisplay(true);

        let deletedStr;
        try {
          deletedStr = pyodide.runPython(`json.dumps(${JSON.stringify(deleted)})`);
        } catch (e) {
          deletedStr = String(deleted);
        }

        showResult(resultDiv, "success", "Value deleted", deletedStr);
      } catch (error) {
        showResult(resultDiv, "error", error.message);
      }
    });

    // Get depth
    document.getElementById("depth-btn").addEventListener("click", async () => {
      const resultDiv = document.getElementById("depth-result");

      try {
        showResult(resultDiv, "info", "Processing...");
        const code = `get_depth(data)`;
        currentCodeStrings['get_depth'] = code;
        const depth = pyodide.runPython(code);
        showResult(resultDiv, "success", "Maximum nesting depth", String(depth));
      } catch (error) {
        showResult(resultDiv, "error", error.message);
      }
    });

    // Count leaves
    document.getElementById("leaves-btn").addEventListener("click", async () => {
      const resultDiv = document.getElementById("leaves-result");

      try {
        showResult(resultDiv, "info", "Processing...");
        const code = `count_leaves(data)`;
        currentCodeStrings['count_leaves'] = code;
        const count = pyodide.runPython(code);
        showResult(resultDiv, "success", "Total leaf values", String(count));
      } catch (error) {
        showResult(resultDiv, "error", error.message);
      }
    });

    // Get all paths
    document.getElementById("paths-btn").addEventListener("click", async () => {
      const resultDiv = document.getElementById("paths-result");

      try {
        showResult(resultDiv, "info", "Processing...");
        const code = `get_all_paths(data)`;
        currentCodeStrings['get_all_paths'] = code;

        const pathsJson = pyodide.runPython(`
import json
paths = get_all_paths(data)
dot_paths = []
for path in paths:
    if not path:
        dot_paths.append("(root)")
    else:
        dot_paths.append(".".join(str(p) for p in path))
json.dumps(dot_paths)
        `);

        const paths = JSON.parse(pathsJson);

        if (paths.length === 0) {
          showResult(resultDiv, "info", "No leaf values found (empty data structure)");
        } else {
          showResultPaths(resultDiv, paths);
        }
      } catch (error) {
        showResult(resultDiv, "error", error.message);
      }
    });

    // Enter key handlers
    ["get-path", "set-path", "exists-path", "delete-path"].forEach(id => {
      document.getElementById(id).addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
          document.getElementById(id.replace("-path", "-btn")).click();
        }
      });
    });
  }

  function parseValue(value) {
    if (value === "null" || value === "None") return null;
    if (!isNaN(value) && value !== "") return Number(value);
    if (value === "true" || value === "True") return true;
    if (value === "false" || value === "False") return false;
    try {
      return JSON.parse(value);
    } catch (e) {
      return value;
    }
  }

  function showResult(div, type, message, value = null) {
    const statusClass = type === "success" ? "success" : type === "error" ? "error" : "";
    const statusText = type === "success" ? "Success" : type === "error" ? "Error" : "Info";

    let html = `
      <div class="result-header">
        <span>Result</span>
        ${statusClass ? `<span class="result-status ${statusClass}">${statusText}</span>` : ''}
      </div>
      <div class="result-body">
        <span class="result-${type}">${escapeHtml(message)}</span>
        ${value ? `<code class="result-value">${escapeHtml(value)}</code>` : ''}
      </div>
    `;
    div.innerHTML = html;
  }

  function showResultPaths(div, paths) {
    const pathList = paths.map(p => `<li>${escapeHtml(p)}</li>`).join('');
    div.innerHTML = `
      <div class="result-header">
        <span>Result</span>
        <span class="result-status success">Success</span>
      </div>
      <div class="result-body">
        <span class="result-success">Found ${paths.length} path${paths.length !== 1 ? 's' : ''}:</span>
        <ul class="paths-list">${pathList}</ul>
      </div>
    `;
  }

  function updateGetCodePreview() {
    const path = document.getElementById("get-path").value.trim() || "path";
    const defaultValue = document.getElementById("get-default").value.trim();

    let code = `<span class="code-fn">get_at</span>(data, <span class="code-str">"${escapeHtml(path)}"</span>`;
    if (defaultValue) {
      code += `, <span class="code-param">default</span>=<span class="code-str">${escapeHtml(JSON.stringify(parseValue(defaultValue)))}</span>`;
    }
    code += `)`;

    document.getElementById("get-code-preview").innerHTML = code;
  }

  function updateSetCodePreview() {
    const path = document.getElementById("set-path").value.trim() || "path";
    const value = document.getElementById("set-value").value.trim() || "value";
    const create = document.getElementById("set-create").checked;

    let parsedValue = parseValue(value);
    let valueDisplay = typeof parsedValue === "string" ? `"${escapeHtml(parsedValue)}"` : escapeHtml(String(parsedValue));
    document.getElementById("set-code-preview").innerHTML = `<span class="code-fn">set_at</span>(data, <span class="code-str">"${escapeHtml(path)}"</span>, <span class="code-str">${valueDisplay}</span>, <span class="code-param">create</span>=<span class="code-bool">${create ? 'True' : 'False'}</span>)`;
  }

  function updateExistsCodePreview() {
    const path = document.getElementById("exists-path").value.trim() || "path";
    document.getElementById("exists-code-preview").innerHTML = `<span class="code-fn">exists_at</span>(data, <span class="code-str">"${escapeHtml(path)}"</span>)`;
  }

  function updateDeleteCodePreview() {
    const path = document.getElementById("delete-path").value.trim() || "path";
    const allowList = document.getElementById("delete-allow-list").checked;

    let code = `<span class="code-fn">delete_at</span>(data, <span class="code-str">"${escapeHtml(path)}"</span>`;
    if (allowList) {
      code += `, <span class="code-param">allow_list_mutation</span>=<span class="code-bool">True</span>`;
    }
    code += `)`;

    document.getElementById("delete-code-preview").innerHTML = code;
  }

  function copyCode(op) {
    let code = '';
    switch(op) {
      case 'get_at':
        const getPath = document.getElementById("get-path").value.trim() || "path";
        const getDefault = document.getElementById("get-default").value.trim();
        code = `get_at(data, "${getPath}"${getDefault ? `, default=${JSON.stringify(parseValue(getDefault))}` : ''})`;
        break;
      case 'set_at':
        const setPath = document.getElementById("set-path").value.trim() || "path";
        const setValue = document.getElementById("set-value").value.trim() || "value";
        const setCreate = document.getElementById("set-create").checked;
        code = `set_at(data, "${setPath}", ${JSON.stringify(parseValue(setValue))}, create=${setCreate ? 'True' : 'False'})`;
        break;
      case 'exists_at':
        const existsPath = document.getElementById("exists-path").value.trim() || "path";
        code = `exists_at(data, "${existsPath}")`;
        break;
      case 'delete_at':
        const deletePath = document.getElementById("delete-path").value.trim() || "path";
        const allowList = document.getElementById("delete-allow-list").checked;
        code = `delete_at(data, "${deletePath}"${allowList ? ', allow_list_mutation=True' : ''})`;
        break;
      case 'get_depth':
        code = 'get_depth(data)';
        break;
      case 'count_leaves':
        code = 'count_leaves(data)';
        break;
      case 'get_all_paths':
        code = 'get_all_paths(data)';
        break;
    }

    navigator.clipboard.writeText(code).then(() => {
      const btn = event.target;
      const original = btn.textContent;
      btn.textContent = 'Copied!';
      setTimeout(() => btn.textContent = original, 1500);
    });
  }

  function clearResults() {
    document.querySelectorAll('.result-panel').forEach(el => el.innerHTML = '');
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  // Start loading Pyodide
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
