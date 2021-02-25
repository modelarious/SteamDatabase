import psycopg2
from psycopg2.errors import DuplicateDatabase





#establishing the connection
conn = psycopg2.connect(
   database="postgres", user='postgres', password='password', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

sql = '''DROP DATABASE IF EXISTS mydb;'''
cursor.execute(sql)

#Preparing query to create a database
sql = '''CREATE database mydb''';

# postgres doesn't support "IF NOT EXISTS" for 'Create database'
try:
    #Creating a database
    cursor.execute(sql)
    print("Database created successfully........")
except DuplicateDatabase:
    pass




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

# UserTagMappings:
#   steam_id -> int, foreign
#   tag_id -> int, foreign
x = '''
CREATE TABLE IF NOT EXISTS UserDefinedTagMappings (
  steam_id int NOT NULL,
  tag_name VARCHAR ( 100 ) NOT NULL,
  FOREIGN KEY (steam_id) REFERENCES Games(steam_id)
);
'''
cursor.execute(x)



# BlacklistedSteamIds:
#   steam_id -> int, primary
x = '''
CREATE TABLE IF NOT EXISTS BlacklistedSteamIds (
  steam_id int NOT NULL PRIMARY KEY
);
'''

cursor.execute(x)


#Closing the connection
conn.close()









# # UserDefinedTags
# #   tag_id -> int, foreign, primary
# #   tag_name -> string
# x = '''
# CREATE TABLE IF NOT EXISTS UserDefinedTag (
#   tag_id serial PRIMARY KEY,
#   tag VARCHAR ( 100 ) UNIQUE NOT NULL
# );
# '''
# cursor.execute(x)






