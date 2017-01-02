from sanic import Blueprint
from sanic.response import html
import json
from ..core_model.github_auth import authit , getuser
from mu_sanic import render_template
from datetime import datetime, timedelta
oauthvw = Blueprint('oauthvw')

@oauthvw.route('/callback')
async def goauth(request):
    logincode = await authit.getToken(request.args.get('code'))
    actoken = logincode.get('access_token') 
    awgituser = await getuser.getusername(actoken)
    gituser = awgituser.get('login')
    resp = html('Redirect',status = 302)
    resp.headers['Location'] = '/admin/'
    resp.cookies['github_login'] = gituser
    resp.cookies['github_token'] = actoken
    resp.cookies['github_login']['path'] = '/'
    resp.cookies['github_token']['path'] = '/'
    resp.cookies['github_login']['expires'] = datetime.now() + timedelta(seconds=30)
    resp.cookies['github_token']['expires'] = datetime.now() + timedelta(seconds=30)
    return resp
    

    
