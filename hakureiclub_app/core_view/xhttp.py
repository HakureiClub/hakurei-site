from sanic import Blueprint
from mu_sanic.render_template import render_template
from ..core_model.mongodb import ActiInfo, BlogInfo

xmlhttp = Blueprint('xmlhttp')
blog = BlogInfo()
acti = ActiInfo()


@xmlhttp.route('/event')
async def xindex(request):
    newest = acti.newest()
    blog8th = blog.new8th()
    return render_template('xmlhttp/index.html', **locals())


@xmlhttp.route('/member')
async def member(request):
    return render_template('xmlhttp/member.html')


@xmlhttp.route('/illust')
async def illust(request):
    return render_template('xmlhttp/illust.html')
