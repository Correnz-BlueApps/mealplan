# Mealplan
#### Video Demo: TODO
#### Description:
##### Crawler
The first Part of this project is a simple crawler, that uses the API "api.chefkoch.de/v2/recipes" to write the database table "recipes" with ids, that will be used by the website. To directly call specific recipes from the chefkoch-API.
The crawler also creates the tables "user", "favorites" and "weeks".

##### Website
###### app.py
The second Part of this project is the website. The file "app.py" uses Flask to create an app and SQLite3 to connect to the database "database.db". Then the routes get defined.

###### Routes in order of website navigation
The landing page states the goals and features of the website. Eating healthy and saving your favorite recipes. It is build with the template "index.html" and called by the route "/".
The navbar at the top has two modes. While not logged in, it leads to the landing page, the sign up page with the route "/register" and the template "register.html" and the log in page with the route "/login" and the template "login.html". It also teases with the option to click the link to the route "/wochenplan" (weekschedule), the central feature of the website. While not logged in the user gets redirected to the log in page though.
The sign up and log in page work as the name suggests using a GET and a POST request at "/register" and "/login" respectivly. Using the former to recive the html- and therein specified css-, png-, jpg- and js-files and using the latter to communicate with the backend and database. The "forms.css" is notable, as it gets used by these two templates exclusivly. When using the POST method of both routes the app checks if all inputs have been filled, doubleing up on the "required" attribute used in the HTML to prevent mistakes and discourage hacking. The "/register" then checks if the password and confirmation match and the username is not already in use. Upon success the app creates a database entry into the table "users" with the name and hashed password, logs in the user and redirects to "/wochenplan". This follows a philosophy to reduce the number of clicks a user needs to perform to reach the desired information. This is in order to reduce friction in the user experience (UX), because every point of friction has the potential to frustrate and shead users.
The route "/login", after checking for frontend hacking, checks if the name exist and password matches. Upon success the app logs in the user and redirects to "/account". Because this is not the first time logging in, the user likely has experienced the features of the "/wochenplan" route and possibly has bookmarked / liked individual recipes and / or weekschedules. It is likely that they are returning to look up the next recipe in their weekschedule. It is possible though that more users want to visite "/wochenplan". Therefore the user behaviour should be observed and the redirection changed to "/wochenplan" if it creates less friction in the UX.
When logged in the navbar does not show the options to navigate to "/register" and "/login" instead it offers a link to the account management page with the route "/account" and the logout page with the route "/logout". Additionally the link to "Wochenplan" no longer gets redirected to the log in page but resolves by rendering the template "wochenplan.html".
"/wochenplan"
"/account"
"/logout"

###### helpers.py