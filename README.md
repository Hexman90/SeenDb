# SeenDb

## Description:
This is a web application that allows users to search for movies, create custom movie lists, and keep track of the movies they have watched. Once a user registers, an automatic watched movies list is created for them.


### Features
Search movies: Users can search for movies by title, and the search results include the movie title, year, and poster.

Create custom movie lists: Users can create their own movie lists and add movies to them. They can also remove movies from their lists.

Watched movies list: Once a user registers, an automatic watched movies list is created for them. Users can add movies to this list with a single click using the "Seen" button on the movie page.

Single-click watched movies: After adding a movie to the watched list, the next time the user searches for that movie, the web app indicates that the user has already watched the movie.

Trending movies: On the homepage, users can see a list of box office movies.


### Usage
Register to create an account and automatically generate a watched movies list.

Search for movies by entering the movie title into the search bar.

Click on a movie to go to its movie page.

On the movie page, add the movie to your watched list by clicking the "Seen" button above the trailer.

Add movies to your custom movie lists by clicking the "add to list" button on the movie page.

Remove movies from your custom movie lists by going to the list and clicking the "remove" button next to the movie.


#### Technologies Used:
Python Flask framework,
HTML, CSS, and JavaScript
SQLite database


## Conclusion:
This web app allows users to search for movies, create custom movie lists, and keep track of the movies they have watched. It also provides users with a list of box office movies on the homepage.


#### App files:
2. app.py: This is the main file that runs the Flask web application. It contains all the routes that the user can navigate through, such as registering and logging in. The file also includes functions to handle user authentication and authorization.

3. helpers.py: This file contains helper functions that are imported into app.py to reduce the amount of code and make app.py more readable. These functions help with tasks such as checking if a user is logged in or not, query the database and query the api.

3. movies.db: This file is the SQLite database where user data is stored, such as the registered users with their IDs, usernames, and hashed passwords, and the movies that the user has in the lists

4. static folder: This folder contains the static files used in the web application such as:
- styles.css which is used to style the web application 
- script.js which contains functions that are used to handle user interactions with the web application, such as adding a movie to a list and removing a movie from a list using AJAX.

5. templates folder: This folder contains all the HTML templates used to render the pages of the web application. The templates include:
- login.html: This template is used for the login page where users can enter their credentials to access the web application.
- register.html: This template is used for the registration page where users can create an account.
- change_password.html: This template is used for the page where users can change their password.
- find_movie.html: This template is used to display movies that match a user's search query.
- movie.html: This template is used to display the details of a movie, such as the title, year of release, rating, genre, poster, cast, and plot. It also displays similar movies to the one being viewed.
- list.html: This template is used to display the movies in a specific list created by the user.
- create_list.html: This template is used to create a new list for the user.
