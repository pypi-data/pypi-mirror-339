from flask import Flask, jsonify
from tesseral_flask import (
    require_auth,
    organization_id,
    access_token_claims,
    credentials,
)

app = Flask(__name__)
app.before_request(
    require_auth(
        publishable_key="publishable_key_7nvw48k6r4wazcpna9stb8tid",
        config_api_hostname="config.tesseral.com",
    )
)


@app.get("/")
def hello_world():
    return jsonify(
        {
            "organization_id": organization_id(),
            "access_token_claims": access_token_claims().json(),
            "credentials": credentials(),
        }
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)
