import sqlite3
import os

DATABASE = 'blog.db'


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with the schema."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()


def get_user_by_username(username):
    """Fetch a user by username."""
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    """Fetch a user by ID."""
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    conn.close()
    return user


def create_user(username, password):
    """Create a new user."""
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def create_post(title, content, author_id):
    """Create a new blog post."""
    conn = get_db()
    conn.execute(
        'INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)',
        (title, content, author_id)
    )
    conn.commit()
    conn.close()


def get_all_posts():
    """Fetch all posts with author info, newest first."""
    conn = get_db()
    posts = conn.execute('''
        SELECT posts.*, users.username as author_name
        FROM posts
        JOIN users ON posts.author_id = users.id
        ORDER BY posts.created_at DESC
    ''').fetchall()
    conn.close()
    return posts


def get_post_by_id(post_id):
    """Fetch a single post by ID."""
    conn = get_db()
    post = conn.execute('''
        SELECT posts.*, users.username as author_name
        FROM posts
        JOIN users ON posts.author_id = users.id
        WHERE posts.id = ?
    ''', (post_id,)).fetchone()
    conn.close()
    return post


def delete_post(post_id, author_id):
    """Delete a post (only if the user is the author)."""
    conn = get_db()
    conn.execute(
        'DELETE FROM posts WHERE id = ? AND author_id = ?',
        (post_id, author_id)
    )
    conn.commit()
    conn.close()


def search_posts(query):
    """Search posts by title or content."""
    conn = get_db()
    sql = "SELECT posts.*, users.username as author_name FROM posts JOIN users ON posts.author_id = users.id WHERE posts.title LIKE '%" + query + "%' OR posts.content LIKE '%" + query + "%' ORDER BY posts.created_at DESC"
    posts = conn.execute(sql).fetchall()
    conn.close()
    return posts
