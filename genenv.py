import secrets

VARS = ["FLASK_SECRET_KEY", "NEO4J_PASSWORD"]
TOKEN_LENGTH=24
OUTPUT_FILE=".env"

def generate_token(length: int) -> str:
    return secrets.token_urlsafe(length)

def main():
    with open(OUTPUT_FILE, "w") as file:
        for var in VARS:
            token = generate_token(TOKEN_LENGTH)
            file.write(f"{var}={token}\n")

if __name__ == "__main__":
    main()
