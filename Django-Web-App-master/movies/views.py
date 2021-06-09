from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

# Connect to your AirTable database
AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
             'Table%201', #'Movies',
             api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    # Search everywhere in the AirTable database. Convert all to lowercase for case insensitivity
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({name}))")
    # this is our "context" dictionary to hold data to send from our backend (django view) to frontend (django html)
    stuff_for_frontend = {"search_result": search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)

def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'http://www.filmfodder.com/reviews/images/poster-not-available.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.insert(data)
            messages.success(request, "New Movie Added: {}".format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, "Got an error while trying to create a new movie: {}".format(e))

    return redirect('/')

def edit(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'http://www.filmfodder.com/reviews/images/poster-not-available.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.update(movie_id, data)
            messages.success(request, "Movie Edited: {}".format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, "Got an error while trying to update a movie: {}".format(e))
    return redirect('/')

def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        AT.delete(movie_id)
        messages.warning(request, "Movie Deleted: {}".format(movie_name))
    except Exception as e:
        messages.warning(request, "Got an error while trying to delete a movie: {}".format(e))
    return redirect('/')





