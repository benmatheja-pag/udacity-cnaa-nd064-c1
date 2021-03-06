import logging
import logging.config
import sqlite3

from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
from logging.config import dictConfig

# Define the Flask application
app = Flask(__name__)
dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': 'stdout [%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'defaulterr' : {
            'format': 'stderr [%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers':
    {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "console.error": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "defaulterr",
            "stream": "ext://sys.stderr",
        },
    },
    'loggers': {
        'werkzeug': {
            'handlers': ['console'],
            'level': "ERROR",
            'propagate': False,
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'console.error']
    }
})
# Function to get a database connection.
# This function connects to database with the name `database.db`
# It is counting the performed connections into a single table
open_connections = 0


def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection.execute('INSERT INTO connections VALUES (null)')
    connection.commit()

    return connection

# Function to get a post using its ID


def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                              (post_id,)).fetchone()
    connection.close()
    if post:
        app.logger.debug('Article %s retrieved', dict(post).get('title'))
    return post


# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    app.logger.debug('Requesting Post with %s', post_id)
    if post is None:
        app.logger.error('Article could not be found')
        return render_template('404.html'), 404

    else:
        return render_template('post.html', post=post)

# Define the About Us page


@app.route('/about')
def about():
    app.logger.debug('The "About Us" page is retrieved.')
    return render_template('about.html')

# Define the post creation functionality


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                               (title, content))
            connection.commit()
            app.logger.info('New Article created: %s', title)
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

# Define the healthz check endpoint


@app.route('/healthz', methods=['GET'])
def healthcheck():
    resp = jsonify(result="OK - healthy")
    return resp

# Return the total amount of posts in the database
# Return the total amount of connections in the database


@app.route('/metrics', methods=['GET'])
def metrics():
    connection = get_db_connection()
    rows = connection.execute('SELECT COUNT(*) FROM posts').fetchall()
    for row in rows:
        number_of_posts = list(row)[0]

    rows = connection.execute('SELECT COUNT(*) FROM connections').fetchall()
    for row in rows:
        connections = list(row)[0]
    resp = jsonify(status='OK', posts_count=number_of_posts,
                   db_connection_count=connections)
    return resp


# start the application on port 3111
if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'your secret key'
    app.run(host='0.0.0.0', port='3111')
