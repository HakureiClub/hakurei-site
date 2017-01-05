from sanic import Blueprint
from sanic.response import text,html
from mu_sanic.render_template import render_template
from ..core_model.github_auth import authit,getuser
from ..core_model.mongodb import ActiInfo , BlogInfo , AuthInfo
import markdown2
from mu_sanic.config import loop

blog = BlogInfo()
acti = ActiInfo()
ainfo = AuthInfo() 
admincp = Blueprint('admincp')

async def login_manger(request):
    the_cookie = request.cookies.get('github_login')
    the_token = request.cookies.get('github_token')
    if not the_cookie == None or not the_token == None :
        code = await getuser.getorg(the_cookie,the_token)
        if not code == 200 : 
            return text('你沒有權限噢')
    else:
        res = html('Redirect',status = 302)
        res.headers['Location'] = authit.getGitHubAuth()
        return res 


@admincp.route('/')
async def adminindex(request):
    if await login_manger(request) == None:
        allev = acti.all()
        return render_template('admin/index.html',**locals())
    return await login_manger(request)


@admincp.route('/editor')
async def adminindex(request):
    if await login_manger(request) == None:
        blogtitle = 'nopost'
        blogpost = blog.all()
        return render_template('admin/editor.html',**locals())
    return await login_manger(request)


@admincp.route('/edit/<posted>')
async def adminindex(request,posted):
    if await login_manger(request) == None:
        blogpost = blog.all()
        blogcontent = blog.find(posted)['markdown']
        blogtitle = blog.find(posted)['title']
        return render_template('admin/editor.html',**locals())
    return await login_manger(request)


@admincp.route('/delev/<name>')
async def delev(request,name):
    if await login_manger(request) == None:
        acti.remove(name)
        res = html('Redirect',status = 302)
        res.headers['Location'] = '/admin/'
        return res 
    return await login_manger(request)
    

@admincp.route('/new-post')
async def adminindex(request):
    if await login_manger(request) == None:
        if request.method == 'POST' :
            title = request.form.get('title')
            blog.init(title,str(request.form.get('markdown')))
            return text('OK')
    return await login_manger(request)

@admincp.route('/add_event')
async def add_event(request):
    if await login_manger(request) == None:
        if request.method == 'POST' :
            name = request.form.get('name')
            time = request.form.get('time')
            place = request.form.get('place')
            acti.init(name,time,place)
            res = html('Redirect',status = 302)
            res.headers['Location'] = '/admin/'
            return res 
    return await login_manger(request)

