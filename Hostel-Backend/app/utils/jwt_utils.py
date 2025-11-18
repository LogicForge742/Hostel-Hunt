from flask_jwt_extended import create_access_token, create_refresh_token

def generate_tokens(identity):
    return {
        "access_token": create_access_token(identity=str(identity)),
        "refresh_token": create_refresh_token(identity=str(identity)),
    }
