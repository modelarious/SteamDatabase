import psycopg2

class PostgresConnectionFactory:
  def createConnection(self):
    conn = psycopg2.connect(
      database="postgres", user='postgres', password='postgres', host='database', port= '5432'
    )
    # NO conn.autocommit = True - we handle transactions by ourself because we want
    # to ensure several tables get updated, or everything is not committed.
    return conn