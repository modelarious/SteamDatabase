import psycopg2

class PostgresConnectionFactory:
  def createConnection(self):
    conn = psycopg2.connect(
      database="postgres", user='postgres', password='postgres', host='127.0.0.1', port= '5432'
    )
    # NO conn.autocommit = True - we handle transactions by ourself because we want
    # to ensure several tables get updated, or everything is not committed.
    return conn