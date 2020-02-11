""" Register application routes. """
from flask.app import Flask

def register_routes(app: Flask, root: str = "/api"):  # pylint: disable= unused-argument
    """ Register application routes. """
    # pylint: disable= import-outside-toplevel
    from app.launcher import register_routes as register_launcher_routes
    from app.gpt2 import register_routes as register_gpt2_routes
    
    # Initialize Rest+ API
    register_launcher_routes(app, root)
    register_gpt2_routes(app, root)
