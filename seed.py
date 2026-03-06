"""
Seed script to populate the database with sample users and posts.
"""

from database import init_db, create_user, create_post, get_user_by_username

# Sample users
USERS = [
    {'username': 'alice', 'password': 'password123'},
    {'username': 'bob', 'password': 'letmein'},
    {'username': 'charlie', 'password': 'qwerty2024'},
]

# Sample blog posts
POSTS = [
    {
        'title': 'Getting Started with Python',
        'content': 'Python is a versatile programming language that is great for beginners. In this post, we will cover the basics of Python syntax, data types, and control flow. Whether you are new to programming or coming from another language, Python offers a clean and readable syntax that makes it easy to learn.',
        'author': 'alice',
    },
    {
        'title': 'Understanding Web Security',
        'content': 'Web security is a critical aspect of modern software development. From SQL injection to cross-site scripting, there are many attack vectors that developers need to be aware of. In this post, we discuss common vulnerabilities and how to protect your applications.',
        'author': 'bob',
    },
    {
        'title': 'My Favorite Recipes',
        'content': 'I love cooking and experimenting in the kitchen. Today I want to share my top 3 recipes: homemade pasta with pesto, grilled salmon with lemon butter, and chocolate lava cake. Each recipe is simple to follow and uses ingredients you probably already have.',
        'author': 'charlie',
    },
    {
        'title': 'A Guide to Flask',
        'content': 'Flask is a lightweight web framework for Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. Flask offers suggestions but does not enforce any dependencies or project layout.',
        'author': 'alice',
    },
    {
        'title': 'Exploring Machine Learning',
        'content': 'Machine learning is transforming industries from healthcare to finance. In this introductory post, we look at supervised vs unsupervised learning, neural networks, and practical tools like scikit-learn and TensorFlow that help you build intelligent systems.',
        'author': 'bob',
    },
    {
        'title': 'Travel Diary: Tokyo',
        'content': 'Tokyo is an incredible city that blends tradition and modernity. From the serene Meiji Shrine to the bustling streets of Shibuya, there is something for everyone. The food scene alone makes it worth the trip — sushi, ramen, and yakitori are absolute must-tries.',
        'author': 'charlie',
    },
    {
        'title': 'Tips for Remote Work',
        'content': 'Working from home has become the new normal for many. Here are my top tips: create a dedicated workspace, stick to a routine, take regular breaks, and communicate often with your team. Remote work can be highly productive if done right.',
        'author': 'alice',
    },
    {
        'title': 'Introduction to Databases',
        'content': 'Databases are the backbone of most applications. In this post, we compare relational databases like SQLite and PostgreSQL with NoSQL options like MongoDB. We also discuss when to use each type and best practices for data modeling.',
        'author': 'bob',
    },
    {
        'title': 'Book Review: The Pragmatic Programmer',
        'content': 'The Pragmatic Programmer by David Thomas and Andrew Hunt is a must-read for every software developer. The book covers topics from career development to coding best practices. One of the key takeaways is the importance of being a pragmatic, not dogmatic, developer.',
        'author': 'charlie',
    },
    {
        'title': 'Building a Personal Portfolio',
        'content': 'A personal portfolio website is essential for showcasing your work. In this post, we walk through how to design and build a portfolio using HTML, CSS, and JavaScript. We cover layout tips, color schemes, and how to present your projects effectively.',
        'author': 'alice',
    },
]


def seed():
    """Seed the database with fake users and posts."""
    print('[*] Initializing database...')
    init_db()

    print('[*] Creating users...')
    for user_data in USERS:
        success = create_user(user_data['username'], user_data['password'])
        if success:
            print(f'    Created user: {user_data["username"]}')
        else:
            print(f'    User already exists: {user_data["username"]}')

    print('[*] Creating posts...')
    for post_data in POSTS:
        user = get_user_by_username(post_data['author'])
        if user:
            create_post(post_data['title'], post_data['content'], user['id'])
            print(f'    Created post: "{post_data["title"]}" by {post_data["author"]}')
        else:
            print(f'    Skipped post (author not found): "{post_data["title"]}"')

    print('[✓] Seeding complete!')


if __name__ == '__main__':
    seed()
