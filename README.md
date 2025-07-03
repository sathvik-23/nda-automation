# NDA Agent - Advanced Document Management with AI

A comprehensive AI-powered agent for managing NDA (Non-Disclosure Agreement) documents using PandaDoc API, Google Sheets integration, and intelligent workflow automation.

## 🚀 Features

- **🤖 AI-Powered Agent**: Natural language interface using Agno framework
- **📄 Document Management**: Create, send, and track NDAs via PandaDoc
- **📊 Analytics**: Track statistics and generate reports
- **📱 Google Sheets Integration**: Log activities and maintain records
- **🔔 Email Notifications**: Automated alerts for document events
- **⚡ Workflow Automation**: Complete NDA processes from creation to signature
- **🏥 Health Monitoring**: Component status tracking and diagnostics

## 📁 Project Structure

```
nda-agno/
├── agents/
│   └── nda_agent/
│       ├── __init__.py         # Package initialization
│       ├── nda_agent.py        # Main agent implementation
│       ├── pandadoc_api.py     # PandaDoc API integration
│       ├── google_sheets.py    # Google Sheets integration
│       ├── notifier.py         # Email notification system
│       └── config.py           # Configuration management
├── main.py                     # Main application entry point
├── test_connection.py          # Component testing
├── interactive_demo.py         # Interactive chat demo
├── usage_examples.py           # Usage examples
├── requirements.txt            # Dependencies
├── .env.example               # Configuration template
└── README.md                  # This file
```

## 🛠️ Installation & Setup

### 1. Clone and Setup Environment

```bash
git clone <your-repo-url>
cd nda-agno
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Required Configuration

#### PandaDoc API (Required)
```bash
PANDADOC_API_KEY=your_actual_api_key_here
```
Get your API key from: [PandaDoc Developer Dashboard](https://developers.pandadoc.com/)

#### Google Sheets (Optional)
```bash
GOOGLE_SHEETS_CREDENTIALS_PATH=path/to/credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
```
Setup guide: [Google Sheets API Quickstart](https://developers.google.com/sheets/api/quickstart/python)

#### Email Notifications (Optional)
```bash
NOTIFICATION_EMAIL=your_email@example.com
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_app_password
```

### 4. Test Installation

```bash
python test_connection.py
```

## 🎯 Usage

### Basic Usage

```bash
# Start the main application
python main.py

# Interactive chat with the agent
python interactive_demo.py

# Run usage examples
python usage_examples.py
```

### Programmatic Usage

```python
from agents.nda_agent import NDAAgent, Config

# Initialize agent
config = Config()
nda_agent = NDAAgent(config)

# Natural language interaction
response = nda_agent.run("List my PandaDoc templates")
print(response)

# Create NDA workflow
result = nda_agent.create_nda_workflow(
    template_id="your_template_id",
    recipient_email="john@example.com",
    recipient_name="John Doe",
    company_name="Acme Corp"
)
```

## 🤖 Agent Capabilities

### Natural Language Commands

The agent understands natural language queries like:

- **Template Management**
  - "List my templates"
  - "Show template details for [template_id]"
  - "How many templates do I have?"

- **Document Management**
  - "Create a new NDA document"
  - "Send document [doc_id] for signature"
  - "Check document status for [doc_id]"

- **Analytics & Reporting**
  - "Get my NDA statistics"
  - "Show recent activity"
  - "Check for pending signatures"

- **Workflow Automation**
  - "Create an NDA workflow for John Doe at Acme Corp"
  - "Send daily summary"
  - "Log a manual action"

### Programmatic Functions

```python
# Create complete NDA workflow
nda_agent.create_nda_workflow(
    template_id="template_123",
    recipient_email="client@company.com",
    recipient_name="Client Name",
    company_name="Client Company"
)

# Get statistics
stats = nda_agent.get_nda_statistics()

# Check pending signatures
pending = nda_agent.check_pending_signatures()

# Send daily summary
nda_agent.send_daily_summary()
```

## 📊 Features in Detail

### 1. PandaDoc Integration
- List and manage templates
- Create documents from templates
- Send documents for signature
- Track document status
- Manage document workflows

### 2. Google Sheets Integration
- Log all NDA activities
- Track document history
- Generate statistics
- Maintain audit trails

### 3. Email Notifications
- Document creation alerts
- Signature completion notifications
- Daily activity summaries
- Error notifications

### 4. Workflow Automation
- Complete NDA processes
- Automated status tracking
- Integration between all components
- Custom workflow configurations

## 🔧 Configuration Options

### Agent Settings
```bash
AGENT_NAME=NDA Agent
AGENT_DESCRIPTION=AI agent for NDA document management
DEBUG_MODE=False
VERBOSE_LOGGING=False
```

### PandaDoc Settings
```bash
PANDADOC_API_KEY=your_api_key
```

### Google Sheets Settings
```bash
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=spreadsheet_id
```

### Email Settings
```bash
NOTIFICATION_EMAIL=notifications@company.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_app_password
```

## 🏥 Health Monitoring

The agent includes comprehensive health monitoring:

```python
# Check component health
health_status = nda_agent.health_check()
print(health_status)
```

Monitors:
- PandaDoc API connectivity
- Google Sheets service status
- Email notification configuration
- Overall system health

## 📈 Analytics & Reporting

### Statistics Available
- Total documents created
- Documents sent for signature
- Documents signed/completed
- Pending signatures
- Recent activity logs

### Reporting Features
- Daily summaries via email
- Activity logging to Google Sheets
- Real-time status checking
- Custom report generation

## 🔄 Workflow Examples

### Complete NDA Process
```python
# 1. Create document from template
result = nda_agent.create_nda_workflow(
    template_id="nda_template_123",
    recipient_email="client@company.com",
    recipient_name="John Smith",
    company_name="Acme Corporation"
)

# 2. Document is automatically logged to Google Sheets
# 3. Email notification sent to administrator
# 4. Document ready for sending
```

### Daily Operations
```python
# Check pending signatures
pending = nda_agent.check_pending_signatures()

# Send daily summary
nda_agent.send_daily_summary()

# Get current statistics
stats = nda_agent.get_nda_statistics()
```

## 🚨 Error Handling

The agent includes comprehensive error handling:
- API connection failures
- Invalid configurations
- Network timeouts
- Email delivery issues
- Google Sheets access problems

## 🔒 Security

- Environment variable configuration
- API key protection
- Secure SMTP authentication
- Google OAuth2 integration
- Audit logging

## 📚 API Documentation

### Main Agent Class
```python
class NDAAgent:
    def __init__(self, config: Config)
    def run(self, query: str) -> str
    def create_nda_workflow(self, ...) -> Dict
    def get_nda_statistics(self) -> Dict
    def check_pending_signatures(self) -> Dict
    def send_daily_summary(self) -> Dict
    def health_check(self) -> Dict
```

### Configuration Class
```python
class Config:
    def __init__(self)
    def get_pandadoc_config(self) -> Dict
    def get_google_sheets_config(self) -> Dict
    def get_notification_config(self) -> Dict
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Resources

- [PandaDoc API Documentation](https://developers.pandadoc.com/reference/)
- [Google Sheets API Guide](https://developers.google.com/sheets/api)
- [Agno Framework Documentation](https://docs.agno.ai/)

## 🆘 Support

For issues and questions:
1. Check the health status: `python test_connection.py`
2. Review configuration in `.env`
3. Check logs for error details
4. Verify API keys and permissions

## 🎉 Getting Started

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Configure environment**: Edit `.env` file
3. **Test connection**: `python test_connection.py`
4. **Start using**: `python main.py`
5. **Try interactive mode**: `python interactive_demo.py`

Your NDA Agent is ready to streamline your document management workflow!
