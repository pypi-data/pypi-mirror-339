// Export any JavaScript utilities or functions that might be useful
// for other applications that want to import this package

module.exports = {
  // If you want to expose any JavaScript functionality
  version: require('./package.json').version,
  
  // You could also add a programmatic way to execute your Python script
  execute: function(args = []) {
    const { spawn } = require('child_process');
    const path = require('path');
    
    const pythonScriptPath = path.join(__dirname, 'gpt-researcher-mcp.py');
    return spawn('python', [pythonScriptPath, ...args], { stdio: 'inherit' });
  }
};