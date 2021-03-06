from sanic import Blueprint
from sanic.response import text, html
from mu_sanic.render_template import render_template
from ..core_model.github_auth import authit, getuser
from ..core_model.mongodb import ActiInfo, BlogInfo, AuthInfo

blog = BlogInfo()
acti = ActiInfo()
ainfo = AuthInfo()
admincp = Blueprint('admincp')


def lm_require(func):
    async def wrapper(request, *args, **kwargs):
        the_cookie = request.cookies.get('github_login')
        the_token = request.cookies.get('github_token')
        if the_cookie is not None or the_token is not None:
            code = await getuser.getorg(the_cookie, the_token)
            if code is not 200:
                return text('你沒有權限噢')
            else:
                return await func(request)
        else:
            res = html('Redirect', status=302)
            res.headers['Location'] = authit.getGitHubAuth()
            return res
    return wrapper


@admincp.route('/')
@lm_require
async def adminindex(request):
    allev = acti.all()
    return render_template('admin/index.html', **locals())


@admincp.route('/editor')
@lm_require
async def admineditor(request):
    blogtitle = 'nopost'
    blogpost = blog.all()
    return render_template('admin/editor.html', **locals())


@admincp.route('/edit/<posted>')
@lm_require
async def adminedit(request, posted):
    blogpost = blog.all()
    blogcontent = blog.find(posted)['markdown']
    blogtitle = blog.find(posted)['title']
    return render_template('admin/editor.html', **locals())


@admincp.route('/delev/<name>')
@lm_require
async def delev(request, name):
    acti.remove(name)
    res = html('Redirect', status=302)
    res.headers['Location'] = '/admin/'
    return res


@admincp.route('/new-post')
@lm_require
async def admnewpost(request):
    if request.method == 'POST':
        title = request.form.get('title')
        blog.init(title, str(request.form.get('markdown')))
        return text('OK')


@admincp.route('/add_event')
@lm_require
async def add_event(request):
    if request.method == 'POST':
        name = request.form.get('name')
        time = request.form.get('time')
        place = request.form.get('place')
        acti.init(name, time, place)
        res = html('Redirect', status=302)
        res.headers['Location'] = '/admin/'
        return res
