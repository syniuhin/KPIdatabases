import datetime
from model import Cinema, DBImitation, MovieSession
import os


def flow():
  db = DBImitation(('cinema.p', 'session.p'))
  cinema_data = None
  session_data = None
  done = False
  while not done:
    print """
      load: Load data from file if exists, generate otherwise
      save: Save data

      fc <column, value>: Find cinema
      fs <column, value>: Find session

      lc: List cinemas
      ls: List sessions
      filter: List filtered cinemas

      dc <id>: Delete cinema by id
      ds <id>: Delete session by id

      ic <id, name, city, rating>: Insert cinema
      is <id, name, time, length, cinema_id>: Insert session

      uc <id, name, city, rating>: Update cinema
      us <id, name, time, length, cinema_id>: Update session

      q: Quit
      """

    command = raw_input('Enter command:\n')
    os.system('clear')
    try:
      if command == 'load':
        cinema_data, session_data = db.read_or_generate()
      elif command == 'save':
        db.write(cinema_data, session_data)
      elif command == 'filter':
        filter_strategy = lambda c_id: session_data.has_late_sessions(c_id)
        for i, session in cinema_data.filter(filter_strategy).iteritems():
          print i, session
      elif command == 'q':
        done = True
      elif command[0] == 'f':
        ps = command.split()[1:]
        column, value = (ps[0], ps[1])
        if command[1] == 'c':
          value = cinema_data.parse_str(column, value)
          for i, cinema in cinema_data.find(column, value).iteritems():
            print i, cinema
        elif command[1] == 's':
          value = session_data.parse_str(column, value)
          for i, session in session_data.find(column, value).iteritems():
            print i, session
      elif command[0] == 'l':
        if command[1] == 'c':
          for i, cinema in cinema_data.items.iteritems():
            print i, cinema
        elif command[1] == 's':
          for i, session in session_data.items.iteritems():
            print i, session
      elif command[0] == 'd':
        _id = int(command.split()[1])
        if command[1] == 'c':
          cinema_data.delete(_id)
        elif command[1] == 's':
          session_data.delete(_id)
      elif command[0] == 'i':
        ps = command.split()[1:]
        if command[1] == 'c':
          cinema_data.insert(Cinema(int(ps[0]), ps[1], ps[2], float(ps[3])))
        elif command[1] == 's':
          session_data.insert(
            MovieSession(int(ps[0]), ps[1],
                         datetime.datetime.strptime(ps[2], "%H:%M").time(),
                         int(ps[3]), int(ps[4])))
      elif command[0] == 'u':
        ps = command.split()[1:]
        if command[1] == 'c':
          cinema_data.update(Cinema(int(ps[0]), ps[1], ps[2], float(ps[3])))
        elif command[1] == 's':
          session_data.update(
            MovieSession(int(ps[0]), ps[1],
                         datetime.datetime.strptime(ps[2], "%H:%M").time(),
                         int(ps[3]), int(ps[4])))
      else:
        raise ValueError('Wrong command!')
    except ValueError as error:
      print error.message
      pass


flow()
