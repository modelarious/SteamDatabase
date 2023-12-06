import psycopg2
from os import getenv


class PostgresConnectionFactory:
    def createConnection(self):
        host = "127.0.0.1"

        # detect if running in docker compose env, if so, point to the database defined there instead
        docker_switch = getenv("DOCKER_ENV")
        if docker_switch:
            host = "database"

        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host=host,
            port="5432",
        )
        # NO conn.autocommit = True - we handle transactions by ourself because we want
        # to ensure several tables get updated, or everything is not committed.
        return conn
