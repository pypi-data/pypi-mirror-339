#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the path to the Python script
const pythonScriptPath = path.join(__dirname, 'gpt-researcher-mcp.py');

// Check if Python script exists
if (!fs.existsSync(pythonScriptPath)) {
  console.error(`Error: Python script not found at ${pythonScriptPath}`);
  process.exit(1);
}

// Forward command line arguments to the Python script
const args = process.argv.slice(2);

// Spawn Python process with stdio inherited to properly handle piped input
const pythonProcess = spawn('python', [pythonScriptPath, ...args], {
  stdio: 'inherit' // This ensures stdin/stdout/stderr are inherited from parent process
});

pythonProcess.on('error', (err) => {
  if (err.code === 'ENOENT') {
    console.error('Error: Python is not installed or not in PATH. Please install Python to use this tool.');
  } else {
    console.error(`Error executing Python script: ${err.message}`);
  }
  process.exit(1);
});

pythonProcess.on('close', (code) => {
  process.exit(code);
});