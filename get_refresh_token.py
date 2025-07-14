import praw
import random
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

# === CONFIGURATION ===
CLIENT_ID = ""
REDIRECT_URI = "http://localhost:65010"
USER_AGENT = "obtain_refresh_token:v1.0 (by u/username)"


# === Local HTTP server to catch the redirect ===
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = self.path.split("?")[1]
        code = dict(x.split("=") for x in params.split("&"))["code"]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Token received. You can close this tab.")
        # Save the code to the server object (even if Pyright can't infer it)
        self.server.token_code = code


# === Open Reddit Auth Flow in Browser ===
def get_code():
    state = str(random.randint(100000, 999999))
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=None,
        redirect_uri=REDIRECT_URI,
        user_agent=USER_AGENT,
    )
    url = reddit.auth.url(["identity", "read", "history"], state=state, duration="permanent")
    print("🔗 Opening Reddit OAuth URL in your browser...")
    webbrowser.open(url)
    httpd: HTTPServer = HTTPServer(("localhost", 65010), Handler)
    httpd.handle_request()
    return getattr(httpd, "token_code", None)


# === Main Function to Print Refresh Token ===
def main():
    code = get_code()
    if code is None:
        print(" Error: No code received.")
        return

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=None,
        redirect_uri=REDIRECT_URI,
        user_agent=USER_AGENT,
    )
    refresh_token = reddit.auth.authorize(code)
    print("\nYour refresh token is:\n")
    print(refresh_token)
    print("\n Save this securely. You’ll use it in your main.py.")


if __name__ == "__main__":
    main()
