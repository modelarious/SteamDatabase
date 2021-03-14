import psycopg2

class PostgresConnectionFactory:
  @staticmethod
  def createConnection():
    conn = psycopg2.connect(
      database="postgres", user='postgres', password='password', host='127.0.0.1', port= '5432'
    )
    conn.autocommit = True
    return conn