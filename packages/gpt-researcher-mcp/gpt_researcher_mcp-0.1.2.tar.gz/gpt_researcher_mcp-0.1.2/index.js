#!/usr/bin/env node
const { spawn } = require('cross-spawn');
const path = require('path');

const scriptPath = path.join(__dirname, 'gpt-researcher-mcp.py'); // Path to the Python script
const child = spawn('python', [scriptPath, ...process.argv.slice(2)]);

child.stdout.pipe(process.stdout);
child.stderr.pipe(process.stderr);

child.on('close', (code) => {
  process.exit(code);
});
