from flask import Flask, url_for, request, render_template
from main import app

# requests being the package to retrieve API requests responses
import requests

#Global variables
apiKey = "89bf4a8b688cd3ae5e0932562b79234d"
pageToDisplay = 1
maxPages = "To be implemented"

# Function to retrieve the base url to access images (posters, logos, etc..) through the configuration url
def getPosterBasePath():
    basePath = "https://api.themoviedb.org/3/configuration"
    url = basePath + '?api_key=' + apiKey
    r = requests.get(url)
    data = r.json()
    images = data['images']
    posterBasePath = images['secure_base_url']
    print (posterBasePath)
    return posterBasePath


# Function to send the page number to display based on the Previous or Next button when clicked
def pagesNavigation(move, max_pages):
	global pageToDisplay
	if (move == "previous" and pageToDisplay > 1):
		pageToDisplay = pageToDisplay - 1
	elif (move == "next" and pageToDisplay < max_pages):
		pageToDisplay = pageToDisplay + 1
	return pageToDisplay


# Server - Display index page with trending movies of the week when app is initiated / loaded
@app.route('/')
def index():

    # build the URL initially
    basePath = "https://api.themoviedb.org/3/"
    requesType = "trending/"
    mediaType = "movie/"
    timeWindow = "week"
    url = basePath + requesType + mediaType + timeWindow + '?api_key=' + apiKey
    print (url)

    # Fetch results for given URL
    r = requests.get(url)
    data = r.json()
    movies = data['results']

    # Render the page
    if request.method == 'GET':
        #send user the page/form. e.g, movies = movies means movies as variable to pass to the html template and movies being the dictionary from the api response
        return render_template('index.html', movies = movies, posterBasePath = getPosterBasePath(), poster_size = "w92")
    else:
        # To be formatted with proper page later
        return "<h2>Invalid Request</h2>"


# Server - Display list or movies resulted from the filters added by the user
@app.route('/results', methods=['POST'])
def results():

    # build the URL initially
    basePath = "https://api.themoviedb.org/3/"
    requesType = "discover/"
    mediaType = "movie"

    # fetch actions done by the user through the POST method. This mainy allow us to identify whether the user has clicked Next or Previous
    next = request.form.get('next')
    previous = request.form.get('previous')
    
    # increment or decrement the page number depending on whether the user has clicked Next or Previous
    if next:
        pagesNavigation("next", 7)
    elif previous:
        pagesNavigation("previous", 7)
    print ("Page Displayed: " + str(pageToDisplay))

    url = basePath + requesType + mediaType + '?api_key=' + apiKey + "&page=" + str(pageToDisplay)

    # fetch selected values sent by the user through the POST method
    year = request.form['years']
    rating = request.form['rating']

    # complete the URL base on added filters
    if year != "any":
        # casting year as integer in case it is not "any". The the drop down menu in the html page evaluates year as an integer.
        year = int(year)
        url = url + "&primary_release_year=" + str(year)
    if rating != "any":
        # casting rating as integer in case it is not "any". The the drop down menu in the html page evaluates rating as an integer.
        rating = int(rating)
        url = url + "&vote_average.gte=" + str(rating)

    print ("Year Selection: " + str(year))
    print ("Rating Selection: " + str(rating))
    print (url)

    # Fetch results for given URL
    r = requests.get(url)
    data = r.json()
    movies = data['results']
    total_pages = data['total_pages']
    total_results = data['total_results']

    # Filters should come through the POST method
    if request.method == 'POST':

        # Render the page
        return render_template('results.html', movies = movies, posterBasePath = getPosterBasePath(), poster_size = "w92", selectedYear=year, selectedRating=rating, page=pageToDisplay, total_pages=total_pages)

    else:
        # To be formatted with proper page later
        return "<h2>Invalid Request</h2>"
    