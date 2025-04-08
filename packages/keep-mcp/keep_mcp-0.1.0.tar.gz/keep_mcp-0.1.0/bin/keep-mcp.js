#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the directory where the package is installed
const packageRoot = path.resolve(__dirname, '..');

// Find the Python script
const scriptPath = path.join(packageRoot, 'main.py');
if (!fs.existsSync(scriptPath)) {
    console.error('Could not find main.py');
    process.exit(1);
}

// Run the Python script
const pythonProcess = spawn('python', [scriptPath], {
    stdio: 'inherit' // This automatically handles all stdio forwarding
});

// Handle process exit
pythonProcess.on('exit', (code) => {
    if (code !== 0) {
        console.error(`Process exited with code ${code}`);
    }
    process.exit(code);
});

// Forward termination signals to the Python process
process.on('SIGINT', () => pythonProcess.kill('SIGINT'));
process.on('SIGTERM', () => pythonProcess.kill('SIGTERM')); 