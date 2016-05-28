import datetime
import pickle
import random


class MovieSession:
  def __init__(self, session_id, movie_name, start_time, length, cinema_id):
    """
    :param session_id: (unique) Id of this session.
    :param movie_name: Name of a movie to display.
    :param start_time: Datetime object, representing a start time.
    :param length: Length of a session in minutes
    :param cinema_id: Id of a cinema in which this will be showed.
    """
    self.session_id = session_id
    self.movie_name = movie_name
    self.start_time = start_time
    self.length = length
    self.cinema_id = cinema_id

  def __str__(self):
    return '%s at %d, starting at %s and has length of %d min' % \
           (self.movie_name, self.cinema_id, str(self.start_time), self.length)


class MovieSessionContainer:
  def __init__(self):
    self.items = {}

  def insert(self, session):
    key = session.session_id
    if key not in self.items:
      self.items[key] = session
    else:
      raise ValueError('Duplicate id during insertion.')

  def update(self, session):
    key = session.session_id
    if key in self.items:
      self.items[key] = session
    else:
      raise ValueError('Container has no such a key: %d.' % key)

  def delete(self, key):
    if key in self.items:
      self.items.pop(key)
    else:
      raise ValueError('Container has no such a key: %d.' % key)

  def find(self, column, value):
    if column == 'session_id' and value in self.items:
      return self.items[value]
    if column in ['movie_name']:
      return {k: v for k, v in self.items.iteritems() if v.movie_name == value}
    if column in ['start_time']:
      return {k: v for k, v in self.items.iteritems() if v.start_time == value}
    if column in ['length']:
      return {k: v for k, v in self.items.iteritems() if v.length == value}
    if column in ['cinema_id']:
      return {k: v for k, v in self.items.iteritems() if v.cinema_id == value}
    return None

  def has_late_sessions(self, cinema_id):
    """
    :return: If there are any sessions on or after 18:00 for specified cinema_id
    """
    return len([1 for v in self.items.itervalues()
                if v.cinema_id == cinema_id and
                v.start_time >= datetime.time(18)]) > 0

  def has_cinema_id(self, key):
    """
    Checks if particular cinema_id is used across items.
    :param key: Cinema id.
    :return: True if items have this id.
    """
    found = self.find('cinema_id', key)
    return found is not None and len(found) > 0

  def parse_str(self, column, value):
    """
    Parses string into right datatype.
    :param key: Name of a column.
    """
    if column == 'session_id' or column == 'length' or column == 'cinema_id':
      return int(value)
    if column == 'start_time':
      return datetime.datetime.strptime(value, "%H:%M").time()
    return value


class Cinema:
  def __init__(self, cinema_id, cinema_name, location_city, rating):
    """
    :param cinema_id: (unique) Id of this cinema.
    :param cinema_name: Name of a cinema to display.
    :param location_city: Name of a city where this cinema is located.
    :param rating: Float value in range [0,1] indicating user rating.
    """
    self.cinema_id = cinema_id
    self.cinema_name = cinema_name
    self.location_city = location_city
    self.rating = rating

  def __str__(self):
    return '%s, located in %s and rated for %.2f' % \
           (self.cinema_name, self.location_city, self.rating)


class CinemaContainer:
  def __init__(self, usage_callback):
    """
    Container for Cinema objects. Simulates very basic behavior of a table.
    :param usage_callback: Callback that checks if Cinema has no usages
    across MovieSession objects.
    """
    self.items = {}
    self.usage_callback = usage_callback
    self.cinema_ids = []

  def insert(self, cinema):
    key = cinema.cinema_id
    if key not in self.items:
      self.items[key] = cinema
      self.cinema_ids.append(key)
    else:
      raise ValueError('Duplicate id during insertion.')

  def update(self, cinema):
    key = cinema.cinema_id
    if key in self.items:
      self.items[key] = cinema
    else:
      raise ValueError('Container has no such a key: %d.' % key)

  def delete(self, key):
    if key in self.items:
      self.__delete(key)
    else:
      raise ValueError('Container has no such a key: %d.' % key)

  def find(self, column, value):
    if column == 'cinema_id' and value in self.items:
      return self.items[value]
    if column in ['cinema_name']:
      return {k: v for k, v in self.items.iteritems() if v.cinema_name == value}
    if column in ['location_city']:
      return {k: v for k, v in self.items.iteritems() if v.location_city ==
              value}
    if column in ['rating']:
      return {k: v for k, v in self.items.iteritems() if v.rating == value}
    return None

  def filter(self, strategy):
    return {k: v for (k, v) in self.items.iteritems() if strategy(k)}

  def parse_str(self, column, value):
    """
    Parses string into right datatype.
    :param key: Name of a column.
    """
    if column == 'cinema_id':
      return int(value)
    if column == 'rating':
      return float(value)
    return value

  def __delete(self, key):
    if not self.usage_callback(key):
      self.items.pop(key)
      self.cinema_ids.remove(key)
    else:
      raise ValueError('Cinema is used in some sessions, do not leave them '
                       'without a home!')

  def __getstate__(self):
    """
    :return: Object __dict__ without a callback (since it's bounded to
    an instance).
    """
    d = dict(self.__dict__)
    del d['usage_callback']
    return d


default_cities = ['Kyiv', 'Kharkiv', 'Odessa', 'Lviv']
default_movies = ['Jaws', 'Alien', 'Birdman', 'Clockwork Orange',
                  'Pulp Fiction', 'Kill Bill', 'The Revenant']


def gen_cinema_data(usage_callback, length=5):
  """
  Generates cinema data from scratch.
  :param usage_callback: Callback for CinemaContainer.
  :param length: Length of a sequence to generate.
  :return: CinemaContainer object.
  """
  data = CinemaContainer(usage_callback)
  for i in xrange(length):
    data.insert(Cinema(i, 'Cinema %02d' % i, random.choice(default_cities),
                       random.random()))
  return data


def gen_session_data(cinema_ids, length=10):
  """
  Generates session data from scratch.
  :param cinema_ids: Existing cinema ids.
  :param length: Length of a sequence to generate.
  :return: MovieSessionContainer object.
  """
  data = MovieSessionContainer()
  for i in xrange(length):
    data.insert(MovieSession(i, random.choice(default_movies),
                             datetime.time(random.randint(12, 23)), 90,
                             random.choice(cinema_ids)))
  return data


class DBImitation:
  def __init__(self, filenames):
    """
    Constructs kind of helper for our file I/O routine.
    :param filenames: Tuple of strings, containing names of files to operate
    with.
    """
    self.cinema_fn, self.session_fn = filenames

  def read_or_generate(self):
    """
    Tries to read from a file, otherwise - generates random data.
    :return: Tuple of lists for Cinema and MovieSessions respectively.
    """
    cinema_file = None
    session_file = None
    try:
      cinema_file = open(self.cinema_fn, 'rb')
      session_file = open(self.session_fn, 'rb')
    except IOError:
      print 'Error opening files'
    if cinema_file and session_file:
      try:
        cinema_data = pickle.load(cinema_file)
        session_data = pickle.load(session_file)
        cinema_data.usage_callback = session_data.has_cinema_id
        print 'Done reading'
      except pickle.PickleError:
        print 'Error loading dumps'
        cinema_data = gen_cinema_data(lambda x: False)
        session_data = gen_session_data(cinema_data.cinema_ids)
        cinema_data.usage_callback = session_data.has_cinema_id
      cinema_file.close()
      session_file.close()
    else:
      cinema_data = gen_cinema_data(lambda x: False)
      session_data = gen_session_data(cinema_data.cinema_ids)
      cinema_data.usage_callback = session_data.has_cinema_id
    return cinema_data, session_data

  def write(self, cinema_data, session_data):
    try:
      cinema_file = open(self.cinema_fn, 'wb')
      session_file = open(self.session_fn, 'wb')
    except IOError:
      print 'Error opening files'
      return
    try:
      pickle.dump(cinema_data, cinema_file)
      pickle.dump(session_data, session_file)
      print 'Done writing'
    except pickle.PickleError:
      print 'Error writing dumps'
    cinema_file.close()
    session_file.close()
