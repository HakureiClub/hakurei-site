from sanic import Blueprint
from mu_sanic.render_template import render_template
from ..core_model.mongodb import ActiInfo, BlogInfo 

acti = ActiInfo()
blog = BlogInfo()
main = Blueprint('index')

@main.route('/')
async def index(request):
    newest = acti.newest()
    blog8th = blog.new8th()
    return render_template('index.html',**locals())

@main.route('/illust')
async def illust(request):
    return render_template('illust.html')

@main.route('/blog/<url>')
async def blogindex(request,url):
    print(url)
    blogcontent = blog.find(url)
    return render_template('blog/index.html',**locals())
