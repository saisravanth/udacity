#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    shows = db.relationship('Show', backref='Venue', lazy=True)

    def __repr__(self):
        return f"id:{self.id}, name:{self.name}, city:{self.city}, state:{self.state}, address:{self.address}, phone:{self.phone}, genres:{self.genres}, image_link:{self.image_link}, facebook_link:{self.facebook_link}, website:{self.website}, seeking_talent:{self.seeking_talent}, seeking_description:{self.seeking_description}"


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))


    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    shows = db.relationship('Show', backref='Artist', lazy=True)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

def getNumberOfUpcomingShows(shows):
  count = 0
  for show in shows:
    if show.start_time > datetime.utcnow():
      count += 1
  return count

def getNumberOfPastShows(shows):
  count = 0
  for show in shows:
    if show.start_time <= datetime.utcnow():
      count += 1
  return count

def getUpcomingShows(shows):
  showDetails = []
  for show in shows:
    if show.start_time > datetime.utcnow():
      details = {}
      details['artist_id'] = show.artist_id
      details['artist_name'] = Artist.query.filter_by(id=show.artist_id).first().name
      details['artist_image_link'] = Artist.query.filter_by(id=show.artist_id).first().image_link
      details['start_time'] = str(show.start_time)
      showDetails.append(details)
  return showDetails

def getPastShows(shows):
  showDetails = []
  for show in shows:
    if show.start_time < datetime.utcnow():
      details = {}
      details['artist_id'] = show.artist_id
      details['artist_name'] = Artist.query.filter_by(id=show.artist_id).first().name
      details['artist_image_link'] = Artist.query.filter_by(id=show.artist_id).first().image_link
      details['start_time'] = str(show.start_time)
      showDetails.append(details)
  return showDetails

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  data = []
  cities = set(db.session.query(Venue.city).limit(10).all())
  states = set(db.session.query(Venue.state).limit(10).all())


  cities = [str(city).replace('(', '').replace(')', '').replace(',', '').replace("'", '') for city in cities]
  states = [str(state).replace('(', '').replace(')', '').replace(',', '').replace("'", '') for state in states]

  for i in range(len(cities)):
      item = {}
      item['city'] = cities[i]
      item['state'] = states[i]
      venue_by_city = db.session.query(Venue).filter_by(city=cities[i])
      venues = [{"id":venue.id, "name":venue.name, "num_upcoming_shows":getNumberOfUpcomingShows(venue.shows)} for venue in venue_by_city]
      item['venues'] = venues
      data.append(item)

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response = {}
  search_term = request.form.get('search_term', '')
  venues = db.session.query(Venue).filter(Venue.name.ilike('%' + search_term + '%'))
  count = venues.count()

  data = [{"id":venue.id, "name":venue.name, "num_upcoming_shows":getNumberOfUpcomingShows(venue.shows)} for venue in venues]
  response['count'] = count
  response['data'] = data
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

def row2dict(row):
  d = {}
  for column in row.__table__.columns:
      if column.name == 'genres':
        genres = row.genres
        genres = ''.join(genres)
        genres = genres.strip('{}').split(',')
        d[column.name] = genres
      else:
        d[column.name] = getattr(row, column.name)
  
  d['past_shows'] = getPastShows(row.shows)
  d['past_shows_count'] = getNumberOfPastShows(row.shows)
  d['upcoming_shows'] = getUpcomingShows(row.shows)
  d['upcoming_shows_count'] = getNumberOfUpcomingShows(row.shows)

  return d

@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  if request.method == 'GET' and request.method != 'DELETE':
    venue = db.session.query(Venue).filter_by(id=venue_id).first()
    if venue is None:
      message = 'URL: {http://localhost:5000/veues/' + str(venue_id) + '} was not found !!'
      flash(message=message)
      return redirect(url_for('venues'))    

    data_ = {}
    data_ = row2dict(venue)
 
  return render_template('pages/show_venue.html', venue=data_)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  try:
      form = VenueForm()
      name = request.form.get('name') 
      city = request.form.get('city')
      state = request.form.get('state')
      address = request.form.get('address')
      phone = request.form.get('phone')
      facebook_link = request.form.get('facebook_link')
      genres = request.form.getlist('genres')
      image_link = "" 
      website = ""
      seeking_talent = True
      seeking_description = "Looking for young talent to join the team" 

      venue =  Venue(name=name, city=city, state=state, address=address, phone=phone, facebook_link=facebook_link, genres=genres, image_link=image_link, website=website,seeking_talent=seeking_talent, seeking_description=seeking_description)
      
      db.session.add(venue)
      db.session.commit()

      flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
      db.session.rollback() 
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      print(sys.exc_info())
  finally:
      db.session.close() 
  
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  try:
    print("venue_id: ", venue_id)
    venue_id = int(request.get_json()["id"])
    print("venue_id from json: ", venue_id)
    db.session.query(Show).filter_by(venue_id=venue_id).delete()
    db.session.query(Venue).filter_by(id=venue_id).delete()
    db.session.commit()
    message = 'Venue with ID: '+ str(venue_id) + ' has been removed !!'
    flash(message=message)
  except:
    db.session.rollback()
    print(sys.exe_info())
  finally:
    db.session.close()
  
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  data = []
  ids = list(db.session.query(Artist.id).distinct())
  names = list(db.session.query(Artist.name).distinct())

  ids = [str(id).replace('(', '').replace(')', '').replace(',', '').replace("'", '') for id in ids]
  names = [str(name).replace('(', '').replace(')', '').replace(',', '').replace("'", '').replace("\\n", '') for name in names]

  for i in range(len(ids)):
      item = {}
      item['id'] = ids[i]
      item['name'] = names[i]
      data.append(item)  

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  response = {}
  search_term = request.form.get('search_term', '')
  artists = db.session.query(Artist).filter(Artist.name.ilike('%' + search_term + '%'))
  count = artists.count()

  data = [{"id":artist.id, "name":artist.name, "num_upcoming_shows":getNumberOfUpcomingShows(artist.shows)} for artist in artists]
  response['count'] = count
  response['data'] = data

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  artist = db.session.query(Artist).filter_by(id=artist_id).first()
  if artist is None:
    message = 'URL: {http://localhost:5000/artists/' + str(artist_id) + '} was not found !!'
    flash(message=message)
    return redirect(url_for('artists'))    

  data_ = {}
  data_ = row2dict(artist)

  return render_template('pages/show_artist.html', artist=data_)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = db.session.query(Artist).filter_by(id=artist_id).first()

  if artist is None:
    message = 'Artist with ID: '+ str(artist_id) + ' does not exist !!'
    flash(message=message)
    return redirect(url_for('index'))
 
  artist={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.phone,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
  }

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  try:
      form = ArtistForm()
      artist = db.session.query(Artist).filter_by(id=artist_id).first()

      artist.name = request.form.get('name') 
      artist.city = request.form.get('city')
      artist.state = request.form.get('state')
      artist.phone = request.form.get('phone')
      artist.facebook_link = request.form.get('facebook_link')
      artist.genres = request.form.getlist('genres')
      artist.image_link = "" 
      artist.website = ""
      artist.seeking_venue = True
      artist.seeking_description = "Looking for venues that can accomodate 1000 people !!" 
    
      db.session.commit()

      flash('Artist ' + request.form['name'] + ' was successfully updated !!')
  except:
      db.session.rollback() 
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
      print(sys.exc_info())
  finally:
      db.session.close()   
  
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue = db.session.query(Venue).filter_by(id=venue_id).first()

  if venue is None:
    message = 'Venue with ID: '+ str(venue_id) + ' does not exist !!'
    flash(message=message)
    return redirect(url_for('index'))

  venue={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  
  try:
    form = VenueForm()
    venue = db.session.query(Venue).filter_by(id=venue_id).first()

    venue.name = request.form.get('name') 
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.phone = request.form.get('phone')
    venue.facebook_link = request.form.get('facebook_link')
    venue.genres = request.form.getlist('genres')
    venue.image_link = "" 
    venue.website = ""
    venue.seeking_talent = True
    venue.seeking_description = "Looking for young, bright talent !!" 
    
    db.session.commit()

    flash('Venue ' + request.form['name'] + ' was successfully updated !!')
  except:
    db.session.rollback() 
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    print(sys.exc_info())
  finally:
    db.session.close()   

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')

  try:
      form = ArtistForm()
      name = request.form.get('name') 
      city = request.form.get('city')
      state = request.form.get('state')
      phone = request.form.get('phone')
      facebook_link = request.form.get('facebook_link')
      genres = request.form.getlist('genres')
      image_link = "" 
      website = ""
      seeking_venue = True
      seeking_description = "Looking for venues that can accomodate 1000 people !!" 

      artist =  Artist(name=name, city=city, state=state, phone=phone, facebook_link=facebook_link, genres=genres, image_link=image_link, website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
      
      db.session.add(artist)
      db.session.commit()

      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
      db.session.rollback() 
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
      print(sys.exc_info())
  finally:
      db.session.close()   
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data = []
  shows = db.session.query(Show).all()

  for show in shows:
    details = {}
    details['venue_id'] = show.venue_id
    details['venue_name'] = Venue.query.filter_by(id=show.venue_id).first().name
    details['artist_id'] = show.artist_id
    details['artist_name'] = Artist.query.filter_by(id=show.artist_id).first().name
    details['artist_image_link'] = Artist.query.filter_by(id=show.artist_id).first().image_link
    details['start_time'] = str(show.start_time)
    data.append(details)
  
  print("len of shows: ", len(data))
  print("first show start_time: ", data[1])

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  
  try:
    form = ShowForm()
    artist_id = request.form.get('artist_id') 
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')
      
    show =  Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
      
    db.session.add(show)
    db.session.commit()

    flash('Show with Artist ID: ' + request.form['artist_id'] + ' & Venue ID: ' + request.form['venue_id'] + ' was successfully listed!')
  except:
    db.session.rollback() 
    flash('An error occurred. Show with Artist ID: ' + request.form['artist_id'] + ' & Venue ID: ' + request.form['venue_id'] + ' could not be listed.')
    print(sys.exc_info())
  finally:
    db.session.close()   

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
