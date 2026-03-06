# Blog App — Security Benchmarking Target

A simple blog web application built with **Python/Flask** and **SQLite**, intentionally containing known security vulnerabilities for the purpose of **benchmarking security scanning tools**.

> ⚠️ **WARNING**: This application contains **intentional security vulnerabilities**. Do **NOT** deploy this to any public-facing server. It is designed strictly for local testing and security tool evaluation.

---

## Features

- User registration and login system
- Create, view, and delete blog posts
- Public search bar (searches posts by title or content)
- Clean HTML/CSS frontend (Jinja2 templates)
- Seed script with 3 fake users and 10 fake posts

---

## Project Structure

```
website1/
├── app.py              # Main Flask application
├── database.py         # Database initialization and helper functions
├── seed.py             # Seed script to populate the DB
├── requirements.txt    # Python dependencies
├── blog.db             # SQLite database (created at runtime)
├── README.md           # This file
└── templates/
    ├── base.html       # Base layout template
    ├── index.html      # Home page (list all posts)
    ├── login.html      # Login form
    ├── register.html   # Registration form
    ├── new_post.html   # Create a new post
    ├── view_post.html  # View a single post
    └── search.html     # Search page
```

---

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed the database with fake data
python seed.py

# 3. Run the application
python app.py
```

The app will be available at **http://127.0.0.1:5000**.

### Seeded Users

| Username  | Password      |
|-----------|---------------|
| alice     | password123   |
| bob       | letmein       |
| charlie   | qwerty2024    |

---

## VULNERABILITY NOTES

This section documents the **intentional** security vulnerabilities embedded in this application for benchmarking purposes.

### 1. SQL Injection (CWE-89)

| Detail          | Value |
|-----------------|-------|
| **OWASP Category** | **A03:2021 — Injection** |
| **File**        | `database.py` |
| **Function**    | `search_posts(query)` |
| **Line Area**   | Lines 120–130 (the `search_posts` function) |
| **Trigger Route** | `GET /search?q=<payload>` (handled in `app.py`, function `search()`) |

**Description:**  
The `search_posts()` function builds a SQL query using **Python string concatenation** with unsanitized user input. The search query parameter (`q`) from the URL is directly interpolated into the SQL string without using parameterized queries or any input sanitization.

**Vulnerable Code:**
```python
sql = "SELECT posts.*, users.username as author_name FROM posts JOIN users ON posts.author_id = users.id WHERE posts.title LIKE '%" + query + "%' OR posts.content LIKE '%" + query + "%' ORDER BY posts.created_at DESC"
posts = conn.execute(sql).fetchall()
```

**Example Payloads:**

1. **Extract all posts (tautology):**
   ```
   GET /search?q=' OR '1'='1
   ```

2. **UNION-based data extraction — dump usernames and passwords:**
   ```
   GET /search?q=' UNION SELECT 1,username,password,4,5,6 FROM users--
   ```
   This returns all usernames and plaintext passwords by injecting a UNION SELECT that maps to the same column count as the original query.

3. **Extract SQLite version:**
   ```
   GET /search?q=' UNION SELECT 1,sqlite_version(),3,4,5,6--
   ```

4. **Extract table names from the schema:**
   ```
   GET /search?q=' UNION SELECT 1,name,sql,4,5,6 FROM sqlite_master--
   ```

5. **Boolean-based blind injection:**
   ```
   GET /search?q=' AND 1=1--
   GET /search?q=' AND 1=2--
   ```

---

### 2. Plaintext Password Storage (CWE-256)

| Detail          | Value |
|-----------------|-------|
| **OWASP Category** | **A02:2021 — Cryptographic Failures** |
| **Files**       | `database.py` (function `create_user`), `app.py` (function `login`) |
| **Line Area**   | `database.py` lines 68–80 (`create_user`), `app.py` lines 57–65 (`login` POST handler) |

**Description:**  
User passwords are stored in the SQLite database as **plaintext strings**. No hashing algorithm (e.g., bcrypt, argon2, scrypt) is applied before storage. During login, passwords are compared using a direct string equality check (`user['password'] == password`).

**Impact:**  
If the database file (`blog.db`) is compromised, all user credentials are immediately exposed. Combined with the SQL injection vulnerability above, an attacker can trivially extract all usernames and passwords via a UNION-based injection.

**Evidence — Seeded passwords in the DB:**
```
alice    → password123
bob      → letmein
charlie  → qwerty2024
```

---

### Summary Table

| # | Vulnerability | OWASP | CWE | File | Function |
|---|---------------|-------|-----|------|----------|
| 1 | SQL Injection | A03:2021 — Injection | CWE-89 | `database.py` | `search_posts()` |
| 2 | Plaintext Passwords | A02:2021 — Cryptographic Failures | CWE-256 | `database.py` | `create_user()` |

---

## License

This project is for **educational and security research purposes only**. No license is granted for production use.
