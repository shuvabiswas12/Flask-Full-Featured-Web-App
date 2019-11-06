from flask import Blueprint, render_template, request
from App.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    # posts = Post().query.all()
    page = request.args.get('page', 1, type=int)
    print('Page = ', page)
    posts = Post().query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)
    return render_template("index.html", posts=posts, title='Home')


