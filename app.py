from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import (
    init_db, get_user_by_username, get_user_by_id, create_user,
    create_post, get_all_posts, get_post_by_id, delete_post, search_posts
)

app = Flask(__name__)
app.secret_key = 'super-secret-key-do-not-use-in-production'


# ─── Helpers ────────────────────────────────────────────────────────────────────

def get_current_user():
    """Return the current logged-in user, or None."""
    user_id = session.get('user_id')
    if user_id:
        return get_user_by_id(user_id)
    return None


# ─── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Home page — list all blog posts."""
    posts = get_all_posts()
    user = get_current_user()
    return render_template('index.html', posts=posts, user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('register'))

        success = create_user(username, password)
        if success:
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already taken.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = get_user_by_username(username)

        if user and user['password'] == password:
            session['user_id'] = user['id']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Log out the current user."""
    session.pop('user_id', None)
    flash('Logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    """Create a new blog post (requires login)."""
    user = get_current_user()
    if not user:
        flash('You must be logged in to create a post.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('new_post'))

        create_post(title, content, user['id'])
        flash('Post created!', 'success')
        return redirect(url_for('index'))

    return render_template('new_post.html', user=user)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    """View a single blog post."""
    post = get_post_by_id(post_id)
    if not post:
        flash('Post not found.', 'error')
        return redirect(url_for('index'))
    user = get_current_user()
    return render_template('view_post.html', post=post, user=user)


@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post_route(post_id):
    """Delete a blog post (only the author can delete)."""
    user = get_current_user()
    if not user:
        flash('You must be logged in to delete a post.', 'error')
        return redirect(url_for('login'))

    post = get_post_by_id(post_id)
    if not post:
        flash('Post not found.', 'error')
        return redirect(url_for('index'))

    if post['author_id'] != user['id']:
        flash('You can only delete your own posts.', 'error')
        return redirect(url_for('index'))

    delete_post(post_id, user['id'])
    flash('Post deleted.', 'success')
    return redirect(url_for('index'))


@app.route('/search')
def search():
    """Search posts by title or content."""
    query = request.args.get('q', '')
    results = []
    if query:
        results = search_posts(query)
    user = get_current_user()
    return render_template('search.html', query=query, results=results, user=user)


# ─── Main ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
