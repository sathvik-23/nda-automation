import os
from dotenv import load_dotenv
from agno.models.google import Gemini
from agno.agent import Agent
from agno.tools.googlesheets import GoogleSheetsTools

# 1️⃣ Load env variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")  # Should match exactly what you set in GCP console

if not all([GOOGLE_API_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_PROJECT_ID, GOOGLE_REDIRECT_URI]):
    raise ValueError("One or more required environment variables are missing.")

SHEET_ID = "1luEYAusYNBC_RwgFOycEWJbndp2UKrUP8Q3RI-xopbI"
SHEET_RANGE = "Form Responses 1!A1:E"

# 2️⃣ Gemini model
gemini_model = Gemini(id="gemini-1.5-flash", api_key=GOOGLE_API_KEY)

# 3️⃣ Google Sheets tool with OAuth-based credential setup
sheets_tool = GoogleSheetsTools(
    spreadsheet_id=SHEET_ID,
    spreadsheet_range=SHEET_RANGE,
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
    creds_path="credentials.json",  # File with your OAuth 2.0 client ID + secret
    token_path="token.json",        # Will be created on first login
    read=True
)

# 4️⃣ Define sheet reader agent
sheet_agent = Agent(
    name="Sheet Reader",
    model=gemini_model,
    tools=[sheets_tool],
    instructions=[
        "You are a spreadsheet reader.",
        "Your job is to help users extract information from the configured Google Sheet range.",
        "The spreadsheet ID and range are already configured, so you do not need to ask the user for them.",
        "Use the `read_sheet` tool directly to access the sheet data."
    ],
    markdown=True,
    debug_mode=True,
    show_tool_calls=True,
)

# 5️⃣ Run
if __name__ == "__main__":
    print(">>> Reading Google Sheet...")
    sheet_agent.print_response("Read the contents of the spreadsheet", stream=True)