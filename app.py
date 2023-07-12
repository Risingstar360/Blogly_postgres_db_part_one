from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "mightyleeds11"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def home():
    return redirect("/user-page")


@app.route('/user-page')
def users_list():
    """All registered users"""
    with app.app_context():
        users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)


@app.route('/user-page/new', methods=["GET"])
def users_new_form():
    """Form to register new user"""
    return render_template('new-user.html')


@app.route("/user-page/new", methods=["POST"])
def users_new():
    """Submit form for new user"""
    with app.app_context():
        new_user = User(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            image_url=request.form['image_url'] or None)
        db.session.add(new_user)
        db.session.commit()

    return redirect("/user-page")


@app.route('/user-page/<int:user_id>')
def users_show(user_id):
    """Show selected user details"""
    with app.app_context():
        user = User.query.get_or_404(user_id)
        posts = user.posts  # Fetch the posts for the user
    return render_template('show-user.html', user=user, posts=posts)


@app.route('/user-page/<int:user_id>/edit')
def users_edit(user_id):
    """Form to edit a registered user"""
    with app.app_context():
        user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)


@app.route('/user-page/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Form to update an already registered user"""
    with app.app_context():
        user = User.query.get_or_404(user_id)
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']
        db.session.add(user)
        db.session.commit()

    return redirect("/user-page")


@app.route('/user-page/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Delete a registered user"""
    with app.app_context():
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

    return redirect("/user-page")


@app.route('/user-page/<int:user_id>/posts/new', methods=["GET"])
def posts_new_form(user_id):
    """Form to create a new post"""
    with app.app_context():
        user = User.query.get_or_404(user_id)
    return render_template('new-post.html', user=user)


@app.route('/user-page/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Submit form for new post"""
    with app.app_context():
        user = User.query.get_or_404(user_id)
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, user=user)
        db.session.add(post)
        db.session.commit()

    return redirect(f"/user-page/{user_id}")


@app.route('/user-page/<int:user_id>/posts/<int:post_id>')
def posts_show(user_id, post_id):
    """Show selected post details"""
    with app.app_context():
        post = Post.query.get_or_404(post_id)
    return render_template('show-post.html', post=post)


@app.route('/user-page/<int:user_id>/posts/<int:post_id>/edit')
def posts_edit(user_id, post_id):
    """Form to edit a post"""
    with app.app_context():
        post = Post.query.get_or_404(post_id)
    return render_template('edit-post.html', post=post)


@app.route('/user-page/<int:user_id>/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(user_id, post_id):
    """Form to update a post"""
    with app.app_context():
        post = Post.query.get_or_404(post_id)
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.add(post)
        db.session.commit()

    return redirect(f"/user-page/{user_id}/posts/{post_id}")


@app.route('/user-page/<int:user_id>/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(user_id, post_id):
    """Delete a post"""
    with app.app_context():
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()

    return redirect(f"/user-page/{user_id}")


if __name__ == "__main__":
    app.run(debug=True)
