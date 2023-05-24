import requests
import json
import sqlite3
from password_strength import PasswordPolicy
from flask import redirect, session
from functools import wraps

API="YOUR API KEY"

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
    
def query_api(endpoint, query):
    url = f"https://imdb-api.com/en/API/{endpoint}/{API}/{query}"
    if endpoint == "Title":
        url += "/Trailer"
    payload = {}
    headers= {}
    
    response = requests.request("GET", url, headers=headers, data = payload)
    data = response.content.decode("utf-8")
    
    data = json.loads(data)
    return data


def query_db(query, *args):
    conn = sqlite3.connect('movies.db', check_same_thread=False)
    c = conn.cursor()
    results = None  # initialize the results variable
    try:
        c.execute(query, args)
        conn.commit()
        results = c.fetchall()
    except sqlite3.Error as error:
        print("Error executing SQLite query:", error)
    finally:
        c.close()
        conn.close()
    return results


def password_check(password):
    policy = PasswordPolicy.from_names(length=8, uppercase=1, numbers=1, nonletters=1)
    feedback = policy.test(password)
    requirements_not__met = ", ".join(type(req).__name__ for req in feedback)
    return feedback


def get_watched_movies():
    watched_movies = query_db(
            "SELECT id FROM movies JOIN user_list_items AS list_items ON movies.id = list_items.movie_id "
            "JOIN user_movie_lists AS lists ON list_items.list_id = lists.list_id "
            "WHERE lists.user_id = ? AND lists.list_name = ?", session["user_id"], "Watched Movies"
            )
    watched_movies_ids = [m[0] for m in watched_movies]
    return watched_movies_ids
