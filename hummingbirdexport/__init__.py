#! ../env/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader

from hummingbirdexport.controllers.main import main
from hummingbirdexport import assets

from hummingbirdexport.extensions import (
    assets_env,
    debug_toolbar
)


def create_app():
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. hummingbirdexport.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # register our blueprints
    app.register_blueprint(main)

    return app
