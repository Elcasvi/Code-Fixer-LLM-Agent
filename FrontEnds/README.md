# CodeMedic

CodeMedic is an integrated solution that combines:
- A VS Code extension to manage GitHub issues
- A FastAPI server with endpoints for processing issues
- An agent based on LangGraph using LLM to analyze and resolve code problems

## Architecture

The system consists of three main components:

1. **VS Code Extension**: User interface allowing developers to view and select GitHub issues for automatic resolution.
2. **FastAPI Server**: Backend that receives issues and forwards them to the agent for processing.
3. **LangGraph Agent**: LLM-based system that analyzes issues and proposes solutions.

## Prerequisites

- Node.js and npm (for the extension)
- Python 3.8+ (for the server and the agent)
- GitHub token with permissions to access repositories
- VS Code (to run the extension)

## Setup

1. **Configure the GitHub Token**
   ```bash
   # Create a .env file in the project root
   echo "GITHUB_TOKEN=your_github_token" > .env
   ```

2. **Install Server and Agent Dependencies**
   ```bash
   # Optional but recommended: create virtual environment
   python -m venv venv
   source venv/bin/activate  # Unix/macOS
   # venv\Scripts\activate  # Windows
   
   # Install dependencies
   pip install -r server/requirements.txt
   ```

3. **Install Extension Dependencies**
   ```bash
   cd extension
   npm install
   ```

## Execution

### 1. Start the FastAPI Server (Backend API)

```bash
# Navigate to the server directory
cd server

# Activate virtual environment if necessary
# source ../venv/bin/activate  # Uncomment if you're using a virtual environment

# Start the FastAPI server
uvicorn main:app --reload
```

Keep this terminal open to view server logs and agent processing.

### 2. Compile and Run the VS Code Extension

In a new terminal:

```bash
# Navigate to the extension directory
cd extension

# Install dependencies (if not done before)
npm install

# Compile the extension
npm run compile

# Start VS Code with the extension
code --extensionDevelopmentPath=$PWD ..
```

### 3. Use the Extension in VS Code

1. Once VS Code opens, you'll see the CodeMedic icon in the activity bar (insect icon)
2. Click on the icon to open the GitHub Issues view
3. If necessary, authenticate with GitHub by clicking "Authenticate"
4. You will see a list of issues from the current repository
5. To resolve an issue:
   - Option 1: Click on the "Fix Issue with CodeMedic" icon (test tube icon) next to the issue
   - Option 2: Click on the issue to open the details panel and then click the "Fix this issue with CodeMedic" button


### 4. View the Results

- In the terminal where you started the server (step 1), see the agent's logs analyzing and resolving the issue
- In VS Code, a progress notification followed by a success message will appear when the issue is processed

### 5. Test the System with a Script (Optional)

If you prefer to test the system without using VS Code:

```bash
# Ensure you're in the project root directory
cd /path/to/CodeMedic/project

# Run the test script
python test_fix_code.py
```

## Estructura del Proyecto

```
CodeMedic/
├── agent/                     # LangGraph Agent
│   ├── models/                # Data models
│   ├── tools/                 # Agent tools
│   └── ollama_langgraph_agent.py  # Main agent implementation
├── extension/                 # VS Code Extension
│   ├── src/                   # Source code of the extension
│   ├── package.json           # Extension configuration
│   └── README.md              # Extension documentation
├── server/                    # FastAPI Server
│   ├── app/                   # FastAPI application
│   └── main.py                # Server entry point
├── .env                       # Environment variables (GitHub token)
├── test_fix_code.py           # Test script
└── README.md                  # This file
```

## Troubleshooting

### Python Import Error
If you encounter import issues, check the paths in these files:
- server/app/routes.py
- agent/ollama_langgraph_agent.py
- agent/tools/tools.py

### Server Connection Issues
Ensure that:
- The server is running at  http://localhost:8000
- No other process is using port 8000
- The extension is configured with the correct server URL

### GitHub Authentication Error
Verify that:
- Your GitHub token is valid and has necessary permissions
- The token is correctly set in the .env file

## Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE).