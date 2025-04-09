import click
import webbrowser
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

AUTH0_DOMAIN = "dev-g685aqnukt2eao2p.us.auth0.com"
AUTH0_CLIENT_ID = "TYkTWhDRlsTxygskkyUAYVmNIlBr7bbr"
REDIRECT_URI = "http://localhost:3000/callback"
SESSION_TOKEN_FILE = os.path.expanduser("~/.session_token")

@click.command("login")
def login_user():
    """Log in to the NOTECLI app."""
    click.echo("🔒 Opening browser for login...")
    auth_url = (
        f"https://{AUTH0_DOMAIN}/authorize?"
        f"client_id={AUTH0_CLIENT_ID}&"
        f"response_type=token&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope=openid profile email"
    )
    webbrowser.open(auth_url)
    click.echo("Waiting for authentication...")

    # Start the HTTP server to capture the callback
    token = start_http_server()
    if token:
        save_token(token)
        click.echo("✅ Logged in successfully!")
    else:
        click.echo("❌ Failed to retrieve access token. Ensure the callback URL is correct and retry.")

def save_token(token):
    """Save the token to a file."""
    with open(SESSION_TOKEN_FILE, "w") as f:
        json.dump({"access_token": token}, f)

def get_token():
    """Retrieve the token from the temporary file."""
    if os.path.exists(SESSION_TOKEN_FILE):
        with open(SESSION_TOKEN_FILE, "r") as f:
            data = json.load(f)
            return data.get("access_token")
    return None

def start_http_server():
    """Start an HTTP server to capture the callback request."""
    class CallbackHandler(BaseHTTPRequestHandler):
        token = None

        def do_GET(self):
            """Handle GET requests."""
            if self.path.startswith("/callback"):
                # Serve HTML with JavaScript to extract the token
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Authentication Complete</title>
                        <script>
                            // Extract the token from the URL fragment
                            const fragment = window.location.hash.substring(1);
                            const params = new URLSearchParams(fragment);
                            const accessToken = params.get("access_token");

                            // Send the token to the local server
                            if (accessToken) {
                                fetch("http://localhost:3000/token", {
                                    method: "POST",
                                    headers: { "Content-Type": "application/json" },
                                    body: JSON.stringify({ token: accessToken })
                                }).then(() => {
                                    document.body.innerHTML = "Login successful! You can close this window.";
                                }).catch(err => {
                                    document.body.innerHTML = "Failed to send token to the server.";
                                });
                            } else {
                                document.body.innerHTML = "No access token found in the URL.";
                            }
                        </script>
                    </head>
                    <body>
                        Logging you in...
                    </body>
                    </html>
                """)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not Found.")

        def do_POST(self):
            """Handle POST requests."""
            if self.path == "/token":
                # Receive the token from the frontend
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                CallbackHandler.token = data.get("token")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Token received successfully.")
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not Found.")

        def log_message(self, format, *args):
            # Suppress server logs for cleaner output
            return

    server_address = ('localhost', 3000)
    httpd = HTTPServer(server_address, CallbackHandler)
    try:
        click.echo("🌐 HTTP server running at http://localhost:3000/callback...")
        while not CallbackHandler.token:
            httpd.handle_request()  # Handle one request at a time
        return CallbackHandler.token
    except Exception as e:
        click.echo(f"Error while running HTTP server: {e}")
        return None

if __name__ == "__main__":
    login_user()
