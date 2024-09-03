from flask import render_template, request, redirect, url_for, Blueprint
from defaultapp.models import Post
from flask_security import  current_user

main = Blueprint('main', __name__)


@main.route("/")
def base_url():
    if current_user.is_authenticated:
        return redirect(url_for('bkhapps.eval_individual'))
    else:
        return redirect(url_for('users.login'))
    

@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
