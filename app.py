from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, query_api, query_db, password_check, get_watched_movies

# Configure application
app = Flask(__name__)
app.secret_key = "secret_key"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Route for serving favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            flash("Enter username!")
            return render_template("login.html")

        # Ensure password was submitted
        elif not password:
            flash("Enter password!")
            return render_template("login.html")
        
        #Query database for username
        rows = query_db("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], password):
            flash("Invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Get and remember user's movie lists
        session["lists"] = query_db(
            "SELECT list_id, list_name FROM user_movie_lists WHERE user_id=?", session["user_id"]
            )

        # Redirect user to home page
        flash("Login successfull")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
    
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # When requested via GET., display reg form
    if request.method == "GET":
        return render_template("register.html")
    # When requested via POST
    else:
        # Get the submitted form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            flash("Enter username!")
            return render_template("register.html")

        # Ensure password was submitted
        elif not password:
            flash("Enter password!")
            return render_template("register.html")

        # Ensure confirmation was submitted
        elif not confirmation:
            flash("Enter confirmation!")
            return render_template("register.html")

        # Ensure password and confirmation of the password match
        elif password != confirmation:
            flash("Password and confirmation password do not match")
            return render_template("register.html")

        # Ensure username is not taken
        user_db = query_db("SELECT * FROM users WHERE username = ?;", username)
        if len(user_db) != 0:
            flash("Username already taken")
            return render_template("register.html")
        
        # Check password strength
        requirements_not_met = password_check(password)
        if len(requirements_not_met) != 0:
            flash(f"Password requirements not met: {requirements_not_met}")
            return render_template("register.html")
        
        # Generating hash value
        password_hash = generate_password_hash(password)

        # Add user to the database
        query_db("INSERT INTO users (username, password_hash) VALUES (?,?);", username, password_hash)

        # Get user id
        user_id = query_db("SELECT * FROM users WHERE username = ?", username)[0][0]

        # Create Watched Movie list
        query_db("INSERT INTO user_movie_lists (list_name, user_id) VALUES (?, ?)", "Watched Movies", user_id)

        # Redirect to login page
        return render_template("login.html")


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    """Change Password"""
    # When requested via GET, display change passwod form
    if request.method == "GET":
        return render_template("change_password.html")

    # When requested via POST
    else:
        # Get the submitted form
        username = request.form.get("username")
        password = request.form.get("password")
        new_password = request.form.get("new_password")

        # Ensure username was submitted
        if not username:
            flash("Enter username!")
            return render_template("change_password.html")
        
        # Ensure password was submitted
        elif not password:
            flash("Enter password!")
            return render_template("change_password.html")
        
        # Ensure confirmation was submitted
        elif not new_password:
            flash("Enter password!")
            return render_template("change_password.html")
        
        # Ensure password and confirmation of the password match
        elif password == new_password:
            flash("New password is the same as your old password, enter a different password")
            return render_template("change_password.html")
        
        # Check password strength
        requirements_not_met = password_check(password)
        if len(requirements_not_met) != 0:
            flash(f"Password requirements not met: {requirements_not_met}")
            return render_template("change_password.html")

        # Query database for username
        rows = query_db("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], password):
            flash("Invalid username and/or password")
            return render_template("change_password.html")

        # Generating hash value
        password_hash = generate_password_hash(new_password)

        # Add new password to database
        query_db("UPDATE users SET password_hash = ? WHERE username = ?;", password_hash, username)

        # After registering redirect to login page
        return render_template("login.html")
    


@app.route("/")
def index():
    box_office = query_api("BoxOffice", "")
    if box_office["errorMessage"]:
        flash(f"{box_office['errorMessage']} please try again later!")
        return render_template("index.html")
    return render_template("index.html", box_office=box_office["items"])


@app.route("/find_movie", methods = ["GET"])
def find_movie():
    query = request.args.get("query")
    if query:
        # Search for movies
        movies = query_api("SearchMovie", query)
        if movies["errorMessage"]:
            flash(f"{movies['errorMessage']} please try again later!")
            return render_template("find_movie.html")

        # If user is loged in
        if session.get("user_id"):
            # Query the database to find the movies the user has already watched
            watched_movies = get_watched_movies()
            # Render the "find_movie.html"s
            return render_template("find_movie.html", movies=movies["results"], watched_movies=watched_movies)
        else:
            return render_template("find_movie.html", movies=movies["results"])
    else:
        # If the search query is None, redirect the user back to the previous page
        if request.referrer:
            return redirect(request.referrer)
        else:
            return render_template("index.html")

        

@app.route("/movie/<string:id>", methods=["GET", "POST"])
def movie(id):
    # Retrieve the movie data
    movie_data = query_api("Title", id)
    if movie_data["errorMessage"]:
        flash(f"{movie_data['errorMessage']} please try again later!")
        return render_template("/movie.html", movie_data=None)
    
    # If user is loged in
    if session.get("user_id"):
        # Query the database to find the movies the user has already watched
        watched_movies = get_watched_movies()
        # Render the "movie.html" 
        return render_template("/movie.html", movie_data=movie_data, watched_movies=watched_movies)
    return render_template("/movie.html", movie_data=movie_data)



@app.route("/create_list", methods=["GET", "POST"])
@login_required
def create_list():
    # If the request method is POST
    if request.method == "POST":
        # Get the name of the new movie list from the form data
        list_name = request.form.get("title")
        
        # If the user did not provide a name for the list
        if not list_name:
            flash("Please provide a title for the list!")
            return render_template("create_list.html")
        
        # Add the list to the database
        else:
            query_db(
                "INSERT INTO user_movie_lists (list_name, user_id) VALUES (?, ?)", list_name, session["user_id"])
            
            # Get and remember the user's movie lists
            session["lists"] = query_db(
                "SELECT list_id, list_name FROM user_movie_lists WHERE user_id=?", session["user_id"])
            
            # Display a success message and return the create_list.html template
            flash(f"Created {list_name}")
            return render_template("create_list.html")
    
    # If the request method is GET, display the create_list.html template
    return render_template("create_list.html")

    

@app.route('/addtolist', methods=["GET",'POST'])
def addtolist():
    # Get the movie data from the AJAX request
    movie_data = request.get_json()
        # Add the movie to the user's movie list
    query_db("INSERT INTO user_list_items (list_id, movie_id) VALUES (?, ?)", movie_data["list_id"], movie_data["id"])
    
    # Add the movie to the database if it doesn't already exist
    query_db(
        "INSERT INTO movies (id, title, year, rating, genre, plot, stars, trailer, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        movie_data["id"], movie_data["title"], movie_data["year"], movie_data["imDbRating"], movie_data["genres"], 
        movie_data["plot"], movie_data["stars"], movie_data['linkEmbed'], movie_data["image"]
        )
    flash(f"{movie_data['title']} added to the list")
    return redirect(request.referrer)


@app.route('/removefromlist', methods=['POST'])
def removefromlist():
    # get the name of the list and the ID of the movie to be removed from the AJAX request
    list_name = request.json['list_name']
    movie_id = request.json['movie_id']

    # Remove movie from the user's movie list
    query_db("DELETE FROM user_list_items WHERE list_id=(SELECT list_id FROM user_movie_lists WHERE list_name=? AND user_id=?) AND movie_id=?", list_name, session["user_id"], movie_id)
    flash(f"Movie removed from  {list_name}")
    return "Movie removed from list"


@app.route('/list/<string:name>', methods=["GET", "POST"])
def list(name):
    # Get all the movies in the user's selected movie list
    movies = query_db(
        "SELECT m.id, m.title, m.year, m.rating, m.genre, m.plot, m.stars, m.trailer, m.image FROM movies AS m "
        "JOIN user_list_items AS list_items ON m.id = list_items.movie_id "
        "JOIN user_movie_lists AS lists ON list_items.list_id = lists.list_id "
        "WHERE lists.user_id = ? AND lists.list_name = ?", session["user_id"], name
        )
    # Display the movies in the selected movie list
    return render_template("list.html", movies=movies, name=name)





if __name__ == "__main__":
    app.debug=True
    app.run()
