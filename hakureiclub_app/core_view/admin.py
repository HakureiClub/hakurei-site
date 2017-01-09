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


def lm_require(func):
    async def wrapper(request):
        the_cookie = request.cookies.get('github_login')
        the_token = request.cookies.get('github_token')
        if not the_cookie == None or not the_token == None :
            code = await getuser.getorg(the_cookie,the_token)
            if not code == 200 : 
                return text('你沒有權限噢')
            else:
                return func(request)
        else:
            res = html('Redirect',status = 302)
            res.headers['Location'] = authit.getGitHubAuth()
            return res 
    return wrapper


@lm_require
@admincp.route('/')
async def adminindex(request):
    allev = acti.all()        
    return render_template('admin/index.html',**locals())


@lm_require
@admincp.route('/editor')
async def admineditor(request):
    blogtitle = 'nopost'
    blogpost = blog.all()
    return render_template('admin/editor.html',**locals())


@lm_require
@admincp.route('/edit/<posted>')
async def adminedit(request,posted):
    blogpost = blog.all()
    blogcontent = blog.find(posted)['markdown']
    blogtitle = blog.find(posted)['title']
    return render_template('admin/editor.html',**locals())


@lm_require
@admincp.route('/delev/<name>')
async def delev(request,name):
    acti.remove(name)
    res = html('Redirect',status = 302)
    res.headers['Location'] = '/admin/'
    return res 
    

@lm_require
@admincp.route('/new-post')
async def adminindex(request):
    if request.method == 'POST' :
        title = request.form.get('title')
        blog.init(title,str(request.form.get('markdown')))
        return text('OK')

@lm_require
@admincp.route('/add_event')
async def add_event(request):
    if request.method == 'POST' :
        name = request.form.get('name')
        time = request.form.get('time')
        place = request.form.get('place')
        acti.init(name,time,place)
        res = html('Redirect',status = 302)
        res.headers['Location'] = '/admin/'
        return res 

