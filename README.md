# Resume AI Agents

A comprehensive suite of AI-powered agents for resume building and review, built with LangGraph, FastAPI, and Google Generative AI.

## 📋 Overview

This project implements two complementary agents:

- **Resume Builder Agent**: Creates professional, ATS-friendly resumes from raw user details using streaming capabilities
- **Resume Reviewer Agent**: Analyzes resumes and provides detailed feedback on ATS optimization, content quality, and improvement recommendations

Both agents are built on the a2a-sdk framework and use LangGraph for workflow orchestration.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Application                      │
└────────────┬──────────────────────────────┬─────────────────┘
             │                              │
      ┌──────▼──────┐              ┌────────▼──────┐
      │   Resume    │              │    Resume     │
      │   Builder   │              │   Reviewer    │
      │   Agent     │              │    Agent      │
      │  (Port 8001)│              │  (Port 8002)  │
      └─────┬───────┘              └────────┬──────┘
            │                                │
      ┌─────▼────────┐            ┌─────────▼────┐
      │  Agent Card  │            │  Agent Card  │
      │  Definition  │            │ Definition   │
      └──────────────┘            └──────────────┘
            │                             │
      ┌─────▼────────────────────────────▼──────┐
      │   LLM Services (OpenAI/Groq/LiteLLM)    │
      └───────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (venv, conda, etc.)
- API Keys:
  - Google Generative AI (for Resume Builder)
  - OpenAI or Groq (for LLMs)

### Installation

1. **Clone the repository** (if not already done)
   ```bash
   cd c:\Users\mails\Documents\GitHub\a2a_async_finance
   ```

2. **Create and activate virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file in the root directory with:
   GOOGLE_API_KEY=your_google_api_key
   OPENAI_API_KEY=your_openai_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

## 🎯 Running the Agents

### Resume Builder Agent

Start the Resume Builder Agent on port 8001:

```bash
cd adk_resumebuilder_agent
python main.py
```

**Agent Details:**
- **URL**: `http://localhost:8001`
- **Skill ID**: `resume_Builder`
- **Input Modes**: `text/plain`, `application/json`
- **Output Modes**: `text/plain`, `application/json`
- **Features**: Streaming support enabled

### Resume Reviewer Agent

Start the Resume Reviewer Agent on port 8002:

```bash
cd langgraph_resumereview_agent
python main.py
```

**Agent Details:**
- **URL**: `http://localhost:8002`
- **Skill ID**: `resume_reviewer`
- **Input Modes**: `text/plain`
- **Output Modes**: `text/plain`
- **Features**: Structured feedback and ATS optimization suggestions

### Running Both Agents

In separate terminals after activation:

```bash
# Terminal 1 - Resume Builder
cd adk_resumebuilder_agent && python main.py

# Terminal 2 - Resume Reviewer
cd langgraph_resumereview_agent && python main.py
```

## 📁 Project Structure

```
a2a_async_finance/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env                               # Environment variables (not in git)
│
├── adk_resumebuilder_agent/           # Resume Builder Agent
│   ├── main.py                        # Startup & server configuration
│   ├── agent_executor.py              # Execution handler
│   ├── agent.py                       # Agent logic & workflow
│   ├── server.py                      # Server setup
│   └── __init__.py
│
├── langgraph_resumereview_agent/      # Resume Reviewer Agent (LangGraph)
│   ├── main.py                        # Startup & server configuration
│   ├── agent_executor.py              # Execution handler
│   ├── graph.py                       # LangGraph workflow definition
│   ├── server.py                      # Server setup
│   └── __init__.py
│
├── client/                            # Client utilities
│   ├── agent.py                       # Client agent interface
│   └── __init__.py
│
└── docs/                              # Documentation (expandable)
```

## 🔧 Key Dependencies

| Package | Version | Purpose |
| --- | --- | --- |
| `fastapi` | Latest | Web framework for REST APIs |
| `uvicorn` | Latest | ASGI server |
| `langgraph` | Latest | Workflow orchestration & state management |
| `openai` | Latest | OpenAI API client |
| `groq` | Latest | Groq LLM API client |
| `litellm` | Latest | Unified LLM interface |
| `a2a-sdk` | Latest | AI Agent framework & utilities |
| `google-adk` | Latest | Google Generative AI support |
| `python-dotenv` | Latest | Environment variable management |
| `httpx` | Latest | Async HTTP client |

## 📝 Development Guide

### Understanding Agent Executors

Both agents implement `AgentExecutor` from the a2a-sdk:

```python
class ResumeBuilderAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        # Process user input
        # Execute agent workflow
        # Stream events to event_queue
        
    async def cancel(self, context, event_queue):
        # Handle cancellation
```

**Key Methods:**
- `execute()`: Main execution logic, processes `RequestContext` and queues `EventQueue` events
- `cancel()`: Gracefully cancel ongoing operations

### Adding New Agents

To add a new agent to the project:

1. Create a new directory: `new_agent_module/`
2. Implement the structure:
   ```
   new_agent_module/
   ├── main.py           # Server startup
   ├── agent_executor.py # Executor implementation
   ├── agent.py          # Agent logic
   ├── server.py         # Optional server config
   └── __init__.py
   ```
3. Define `AgentCard` with skills and capabilities
4. Update `requirements.txt` if new dependencies are needed
5. Start server with `python main.py` (update port in main.py)

### Error Handling

Both executors handle errors gracefully:

```python
try:
    # Agent execution
    async for event in self.runner.run_async(...):
        # Process events
except Exception as e:
    await event_queue.enqueue_event(
        new_agent_text_message(f"❌ Error: {str(e)}")
    )
```

## 🌐 API Usage

### Example: Using Resume Builder

```bash
curl -X POST http://localhost:8001/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Build a resume for a senior Python developer"
  }'
```

### Example: Using Resume Reviewer

```bash
curl -X POST http://localhost:8002/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Review my resume for ATS compatibility"
  }'
```

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
# Google Generative AI
GOOGLE_API_KEY=your_google_api_key

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Groq
GROQ_API_KEY=your_groq_api_key

# Optional: Specify default LLM provider
DEFAULT_LLM_PROVIDER=openai
```

## 🐛 Troubleshooting

### Port Already in Use

If a port is already occupied, modify the port in `main.py`:

```python
def main(host='0.0.0.0', port=8001):  # Change port number
    ...
```

### API Key Issues

- Verify all required API keys are set in `.env`
- Check API key validity in respective provider dashboards
- Ensure `.env` file is in the root directory

### Import Errors

If you encounter import errors:

```bash
# Reinstall dependencies with no cache
pip install --no-cache-dir -r requirements.txt

# Restart virtual environment
deactivate
# Reactivate and reinstall
```

### Agent Execution Timeouts

For long-running requests, adjust timeouts or implement request queueing in agent executors.

## 📊 Workflow Examples

### Resume Builder Workflow

```
User Input → Agent Executor → Agent Runner (Google ADK)
   ↓
Session Created → LLM Processing → Streaming Response
   ↓
Event Queue → Client Response
```

### Resume Reviewer Workflow

```
User Input → Agent Executor → LangGraph Workflow
   ↓
State: {input, output} → Graph Nodes (LLM calls)
   ↓
Structured Feedback → Event Queue → Client Response
```

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes following the existing code patterns
3. Test your changes thoroughly
4. Commit with clear messages: `git commit -m "Add feature description"`
5. Push to the branch: `git push origin feature/your-feature`

## 📚 Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [a2a-sdk Documentation](https://github.com/a2a-integration/sdk)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Groq API Documentation](https://console.groq.com/docs)

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review agent executor logs for error details
- Check API key configuration in `.env`
- Verify all dependencies are installed correctly

## 📄 License

Include your project's license here.

---

**Last Updated**: March 8, 2026
