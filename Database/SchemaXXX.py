import psycopg2
from psycopg2.errors import DuplicateDatabase



class connectionFactory:
  @staticmethod
  def createConnection():
    conn = psycopg2.connect(
      database="postgres", user='postgres', password='password', host='127.0.0.1', port= '5432'
    )
    conn.autocommit = True
    return conn

# establishing the connection
# conn = psycopg2.connect(
#    database="postgres", user='postgres', password='password', host='127.0.0.1', port= '5432'
# )
# conn.autocommit = True

conn = connectionFactory.createConnection()

#Creating a cursor object using the cursor() method
cursor = conn.cursor()


# Games:
#   steam_id -> int, primary -> used as foreign key in other tables
#   name_on_harddrive -> string
#   name_on_steam -> string
#   avg_review_score -> float
x = '''
CREATE TABLE IF NOT EXISTS Games (
  steam_id int NOT NULL,
  name_on_harddrive VARCHAR ( 1000 ) UNIQUE NOT NULL,
  path_on_harddrive VARCHAR ( 1000 ) UNIQUE NOT NULL,
  name_on_steam VARCHAR ( 1000 ) UNIQUE NOT NULL,
  avg_review_score DOUBLE PRECISION NOT NULL,
  PRIMARY KEY (steam_id)
);
'''

cursor.execute(x)

# x = '''
# INSERT INTO Games (steam_id, name_on_harddrive, path_on_harddrive, name_on_steam, avg_review_score) VALUES
#     (1976647, 'Tampopo', 'String', '1985-02-10', 5.4),
#     (2658854, 'Factorio', '/Volumes/GameDrive/Factorio', 'Factorio', 9.2);
# '''
# cursor.execute(x)


# UserTagMappings:
#   steam_id -> int, foreign
#   tag_id -> int, foreign
x = '''
CREATE TABLE IF NOT EXISTS UserDefinedGenres (
  steam_id int NOT NULL,
  genre_name VARCHAR ( 100 ) NOT NULL,
  rank int NOT NULL,
  FOREIGN KEY (steam_id) REFERENCES Games(steam_id),
  PRIMARY KEY (steam_id, genre_name)
);
'''
cursor.execute(x)

# x = '''
# INSERT INTO UserDefinedGenres (steam_id, genre_name) VALUES
#     (1976647, 'Good'),
#     (1976647, 'ol'),
#     (1976647, 'Fun'),
#     (2658854, 'Automation');
# '''
# cursor.execute(x)

# BlacklistedSteamIds:
#   steam_id -> int, primary
x = '''
CREATE TABLE IF NOT EXISTS BlacklistedSteamIds (
  steam_id int NOT NULL PRIMARY KEY
);
'''

cursor.execute(x)


# x = '''
# INSERT INTO BlacklistedSteamIds (steam_id) VALUES
#     (75325785),
#     (83325366);
# '''
# cursor.execute(x)

# INSERT INTO films (code, title, did, date_prod, kind) VALUES
#     ('B6717', 'Tampopo', 110, '1985-02-10', 'Comedy'),
#     ('HG120', 'The Dinner Game', 140, DEFAULT, 'Comedy');

#Closing the connection
conn.close()









# # UserDefinedTags
# #   tag_id -> int, foreign, primary
# #   genre_name -> string
# x = '''
# CREATE TABLE IF NOT EXISTS UserDefinedTag (
#   tag_id serial PRIMARY KEY,
#   tag VARCHAR ( 100 ) UNIQUE NOT NULL
# );
# '''
# cursor.execute(x)






