from sanic import Sanic
from mu_sanic import config
from hakureiclub_app.core_view.index import main
from hakureiclub_app.core_view.xhttp import xmlhttp
from hakureiclub_app.core_view.admin import admincp
from hakureiclub_app.core_view.oauth import oauthvw

hakureiclub_app_runapp = Sanic(__name__)
hakureiclub_app_runapp.blueprint(main)
hakureiclub_app_runapp.blueprint(admincp, url_prefix='/admin')
hakureiclub_app_runapp.blueprint(xmlhttp, url_prefix='/xhttp')
hakureiclub_app_runapp.blueprint(oauthvw, url_prefix='/oauth')
hakureiclub_app_runapp.static("/static","./%s/core_static" % config.your_app)
hakureiclub_app_runapp.run(host="0.0.0.0", port=8000, debug=True,loop=config.loop)
