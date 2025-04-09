import requests

AUTH0_DOMAIN = "dev-g685aqnukt2eao2p.us.auth0.com"

def verify_token(auth_header):
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    response = requests.get(
        f"https://{AUTH0_DOMAIN}/userinfo",
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code == 200:
        user_info = response.json()
        return user_info["sub"]  # Return user ID
    return None
