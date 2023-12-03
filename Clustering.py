import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
from io import StringIO


import psycopg2
from os import getenv


def get_user_defined_genres() -> pd.DataFrame:
    conn = create_connection()
    user_defined_genres = get_user_defined_genres_df(conn)
    # create_table(conn)
    # clear_table(conn)
    # for tag_name, download_list in downloads.items():
    #     insert_downloads(conn, tag_name, download_list)
    conn.close()
    return user_defined_genres


def create_connection():
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
    conn.autocommit = True
    return conn


def get_user_defined_genres_df(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
        SELECT *
        FROM userdefinedgenres;
        """
        )
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=columns)
        return df


# def create_table(conn, df):
#     with conn.cursor() as cursor:
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS scorings (
#             steam_id TEXT NOT NULL PRIMARY_KEY
#         )
#         ''')
#     conn.commit()


# def clear_table(conn):
#     with conn.cursor() as cursor:
#         cursor.execute('''
#         DELETE TABLE scorings;
#         ''')
#     conn.commit()


# def insert_downloads(conn, tag_name: str, downloads: List[Download]):
#     with conn.cursor() as cursor:
#         query = 'INSERT INTO downloads (tag_name, save_dir, save_file) VALUES (%s, %s, %s)'
#         data_tuples = [(tag_name, ) + astuple(d) for d in downloads]
#         cursor.executemany(query, data_tuples)
#     conn.commit()


# Your data as a multiline string
data = """
260790\tPrecision Platformer\t1
260790\tPlatformer\t2
1966900\tAction Roguelike\t1
1966900\tPlatformer\t2
1966900\tPrecision Platformer\t3
123456\t2D\t1
123456\tRoguelite\t2
123456\tPrecision Platformer\t3
"""

# Use StringIO to convert the string to a file-like object
data = StringIO(data)

# Read the data into a Pandas DataFrame assuming the data is separated by whitespace
df = pd.read_csv(data, sep="\t", header=None, names=["steam_id", "genre_name", "rank"])

df = get_user_defined_genres()

# find the max rank per steam_id - transform is a cool trick to get a
# vector with the same index as the original dataframe
df["max_rank"] = df.groupby("steam_id")["rank"].transform("max")

# calculate the score of a tag by 1 - ((rank - 1) / max_rank)
# so if there are 20 tags, and we're scoring the 1st tag. it would be 1-(0/20) = 1.00
# and if we're scoring the 5th tag it would be 1-(4/20) = 0.8
# The higher the rank, the higher the score
# XXX XXX XXX XXX YYY XXX I can also see doing this calculation pretending the max_rank is always 20 - that way a title with less tag information doesn't get the few tags it has diluted
df["scoring"] = 1 - ((df["rank"] - 1) / df["max_rank"])

# transform to the following state:
# genre_name  2D             2D Platformer   4 Player Local    Action
# steam_id
# 260790      0.666667       0.055556        0.333333          0.833333
# 1966900     0.550000       0.000000        0.000000          0.300000
per_tag_scoring = df.pivot(
    index="steam_id", columns="genre_name", values="scoring"
).fillna(0)

df = per_tag_scoring
df.index = df.index.map(int)

# calculate pairwise distances
dist_array = pdist(df.values, metric="cityblock")

# gather all pairs of steam_ids
steam_id_pairs = [
    (df.index[i], df.index[j]) for i in range(len(df)) for j in range(i + 1, len(df))
]
distances_df = pd.DataFrame(
    {
        "steam_id_1": [pair[0] for pair in steam_id_pairs],
        "steam_id_2": [pair[1] for pair in steam_id_pairs],
        "distance": dist_array,
    }
)

# Find the index of the minimum distance
# min_distance_index = distances_df['distance'].idxmin()

# Get the row corresponding to the minimum distance
# min_distance_row = distances_df.loc[min_distance_index]
sorted_distances_df = distances_df.sort_values(by="distance")
print(sorted_distances_df)
