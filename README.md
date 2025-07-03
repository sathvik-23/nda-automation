# NDA Agno - PandaDoc API Integration

This project integrates PandaDoc's API with the Agno framework to manage document templates and create documents programmatically.

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
# Activate your virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

#### Option A: Using Environment Variables (Recommended)
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your PandaDoc API key
PANDADOC_API_KEY=your_actual_api_key_here
```

#### Option B: Direct Configuration
Edit `main.py` and replace `"your_actual_api_key"` with your actual API key.

### 4. Get Your PandaDoc API Key

1. Go to [PandaDoc Developer Dashboard](https://developers.pandadoc.com/)
2. Sign in to your account
3. Navigate to API Keys section
4. Create a new API key or copy an existing one

### 5. Test the Connection

```bash
python test_connection.py
```

### 6. Run the Application

```bash
# Basic template listing
python main.py

# Interactive agent demo
python interactive_demo.py

# Usage examples
python usage_examples.py
```

## 📁 Project Structure

```
nda-agno/
├── venv/                    # Virtual environment
├── agno_agent/
│   ├── __init__.py         # Package initialization
│   └── panda_tools.py      # PandaDoc API integration
├── main.py                 # Main application
├── test_connection.py      # API connection test
├── interactive_demo.py     # Interactive agent demo
├── usage_examples.py       # Usage examples
├── setup.sh               # Setup script
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🛠️ Features

- **List Templates**: Retrieve all available templates from your PandaDoc account
- **Template Details**: Get detailed information about specific templates
- **Document Creation**: Create documents from templates (ready for implementation)
- **Agent Integration**: Full Agno framework integration with natural language queries
- **Error Handling**: Comprehensive error handling for API calls
- **Environment Configuration**: Secure API key management

## 🤖 Agent Capabilities

The PandaDoc Agent can understand natural language queries like:

- "List my templates"
- "How many templates do I have?"
- "Tell me about my first template"
- "What templates are available?"
- "Show me template details for [template_id]"

## 🔧 Usage Examples

### Basic Template Listing

```python
from agno_agent.panda_tools import PandaDocTool

# Initialize tool
panda_tool = PandaDocTool(api_key="your_api_key")

# List templates
templates = panda_tool.list_templates()
for template in templates.get("results", []):
    print(f"- {template.get('name')} (ID: {template.get('id')})")
```

### Using the Agent

```python
from agno.agent import Agent
from agno_agent.panda_tools import create_pandadoc_functions

# Create agent
pandadoc_functions = create_pandadoc_functions("your_api_key")
agent = Agent(
    name="PandaDoc Assistant",
    tools=pandadoc_functions,
    markdown=True
)

# Natural language interaction
response = agent.run("List all my templates")
print(response)
```

### Get Template Details

```python
# Get details for a specific template
template_id = "your_template_id"
details = panda_tool.get_template_details(template_id)
print(f"Template has {len(details.get('fields', []))} fields")
```

## 🎯 Available Scripts

- **`main.py`**: Basic template listing and agent setup
- **`test_connection.py`**: Test API connectivity
- **`interactive_demo.py`**: Interactive chat with the agent
- **`usage_examples.py`**: Programmatic usage examples
- **`setup.sh`**: Automated setup script

## 📚 Next Steps

1. **Document Creation**: Implement document creation from templates
2. **Document Sending**: Add functionality to send documents for signatures
3. **Webhook Integration**: Handle PandaDoc webhooks for status updates
4. **Template Management**: Create, update, and delete templates
5. **Advanced Agent Features**: Add more sophisticated document workflows

## 🔗 Resources

- [PandaDoc API Documentation](https://developers.pandadoc.com/reference/)
- [Agno Framework Documentation](https://docs.agno.ai/)
- [Authentication Guide](https://developers.pandadoc.com/reference/authorization)

## 🤝 Support

If you encounter any issues:
1. Check that your API key is correct
2. Verify your PandaDoc account has templates
3. Ensure all dependencies are installed
4. Check the API rate limits

For more help, refer to the PandaDoc API documentation or open an issue.

## ✅ Verification

Your integration is working if:
- `test_connection.py` shows "Connection successful"
- `main.py` lists your templates
- `interactive_demo.py` responds to natural language queries
- You can see your actual PandaDoc templates in the output
