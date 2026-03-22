from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # app.root_path is the 'app' package directory.
    project_root = os.path.abspath(os.path.join(app.root_path, '..'))
    env_file = os.path.abspath(os.path.join(app.root_path,'..','..', ".wol_env"))

    SECRET_KEY = None
    PASTEBIN_PASSWORD = None

    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("SERVER_TOKEN="):
                    SECRET_KEY = line.split("=", 1)[1].strip()
                elif line.startswith("PASTEBIN_PASSWORD="):
                    PASTEBIN_PASSWORD = line.split("=", 1)[1].strip()
    
    if not SECRET_KEY:
        print(f"WARNING: SECRET_KEY not found in {env_file}. Using a temporary, insecure key. Please set a permanent SECRET_KEY.")
        SECRET_KEY = os.urandom(24).hex()

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['PASTEBIN_PASSWORD'] = PASTEBIN_PASSWORD
    app.config['PASTEBIN_ENABLED'] = PASTEBIN_PASSWORD is not None


    from . import routes
    app.register_blueprint(routes.main)

    return app
