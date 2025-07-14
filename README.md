# Reddit Persona Builder

This project allows you to generate a persona profile for any Reddit user by analyzing their public posts and comments. It uses the Reddit API (via PRAW) to fetch user data and extract key information such as age, occupation, location, goals, frustrations, and more.

## Features
- Fetches recent posts and comments from any Reddit user
- Extracts and summarizes user persona details
- Saves the persona profile to a text file
- Includes a tool to obtain a Reddit API refresh token

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/reddit_persona_builder.git
cd reddit_persona_builder
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
# Activate the virtual environment:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Obtain Reddit API Credentials
- Go to https://www.reddit.com/prefs/apps and create a new script application.
- Note your `client_id` and set the `redirect_uri` to `http://localhost:65010`.

### 5. Get a Refresh Token
Run the following command and follow the instructions:
```bash
python get_refresh_token.py
```
This will open a browser window for Reddit authentication and print your refresh token.

### 6. Configure Credentials Securely
**Do NOT hardcode your credentials in the code or commit them to git!**

Create a `.env` file in the project root (this file should NOT be committed to git):
```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret_or_blank
REFRESH_TOKEN=your_refresh_token
USER_AGENT=your_user_agent
```

Add `.env` to your `.gitignore` file:
```
.env
```

### 7. Update the Code to Use Environment Variables
Modify `main.py` and `get_refresh_token.py` to load credentials from the environment (see [python-dotenv](https://pypi.org/project/python-dotenv/)).

## Usage

### 1. Run the Main Script
Start the tool by running:
```bash
python main.py
```

### 2. Enter a Reddit Profile URL
When prompted, enter the URL of the Reddit user whose persona you want to build. For example:
```
Enter Reddit profile URL: https://www.reddit.com/user/spez/
```

### 3. Wait for Data Collection
The script will fetch the user's recent posts and comments, analyze them, and extract persona information.

### 4. View the Output
After processing, the persona profile will be saved to a file named `user_persona.txt` in the project directory. Open this file to view the generated persona, which includes:
- Name, Age, Occupation, Location, Status, Tier, Archetype
- A representative quote
- Goals & Needs
- Frustrations
- Behaviours & Habits
- Citations (links to the original Reddit posts/comments)

#### Example Output (user_persona.txt)
```
Spez - Reddit User Persona
----------------------------------------
Age: 40  ↪ https://www.reddit.com/r/examplepost
Occupation: CEO at Reddit  ↪ https://www.reddit.com/r/examplepost
Location: San Francisco, CA  ↪ https://www.reddit.com/r/examplepost
Status: Unknown
Tier: Early Adopters
Archetype: The Explorer

Quote: "I want to make Reddit a better place."
  ↪ https://www.reddit.com/r/examplepost

--- Goals & Needs ---
• I want to improve community engagement.
  ↪ https://www.reddit.com/r/examplepost

--- Frustrations ---
• Sometimes the site is slow.
  ↪ https://www.reddit.com/r/examplepost

--- Behaviours & Habits ---
• I often check new subreddits.
  ↪ https://www.reddit.com/r/examplepost
```

## Security Notice
- **Never commit your refresh token or client secrets to git.**
- Always use environment variables or a `.env` file (which is gitignored) for sensitive data.

## License
MIT License 