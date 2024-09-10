import pandas as pd
from scipy.spatial.distance import pdist
import psycopg2
from os import getenv
import subprocess


RECOMMENDATION_TABLE_NAME = "recommendations"
RECOMMENDATION_CSV_LOCATION = (
    f"C:\\Users\\micha\\Github\\SteamDatabase\\{RECOMMENDATION_TABLE_NAME}.csv"
)

COPY_CSV_SQL = f"""
COPY {RECOMMENDATION_TABLE_NAME}
FROM '{RECOMMENDATION_CSV_LOCATION}'
DELIMITER ',' CSV;
"""


def run_recommendations() -> pd.DataFrame:
    conn = create_connection()
    user_defined_genres = get_user_defined_genres_df(conn)
    recommendations = calculate_recommendations(user_defined_genres)
    create_table(conn)
    clear_table(conn)
    insert_recommendations(conn, recommendations)
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
        cursor.execute("SELECT * FROM userdefinedgenres;")
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=columns)
        return df


def create_table(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            f"""
        CREATE TABLE IF NOT EXISTS {RECOMMENDATION_TABLE_NAME} (
            steam_id_1 TEXT NOT NULL,
            steam_id_2 TEXT NOT NULL,
            distance FLOAT NOT NULL,
            PRIMARY KEY (steam_id_1) 
        )
        """
        )
    conn.commit()


def clear_table(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            f"""
        TRUNCATE TABLE {RECOMMENDATION_TABLE_NAME};
        """
        )
    conn.commit()


def calculate_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    # find the max rank per steam_id - transform is a cool trick to get a
    # vector with the same index as the original dataframe
    df["max_rank"] = df.groupby("steam_id")["rank"].transform("max")

    # calculate the score of a tag by 1 - ((rank - 1) / max_rank)
    # so if there are 20 tags, and we're scoring the 1st tag. it would be 1-(0/20) = 1.00
    # and if we're scoring the 5th tag it would be 1-(4/20) = 0.8
    # The higher the rank, the higher the score
    # XXX XXX XXX XXX YYY XXX I can also see doing this calculation pretending the max_rank is always 20 - that way a title with less tag information doesn't get the few tags it has diluted
    df["scoring"] = 1 - ((df["rank"] - 1) / df["max_rank"])

    # per tag scoring.
    # transform to the following state:
    # genre_name  2D             2D Platformer   4 Player Local    Action
    # steam_id
    # 260790      0.666667       0.055556        0.333333          0.833333
    # 1966900     0.550000       0.000000        0.000000          0.300000
    df = df.pivot(index="steam_id", columns="genre_name", values="scoring").fillna(0)
    df.index = df.index.map(int)

    # calculate pairwise distances
    dist_array = pdist(df.values, metric="cityblock")

    # gather all pairs of steam_ids
    steam_id_pairs = [
        (df.index[i], df.index[j])
        for i in range(len(df))
        for j in range(i + 1, len(df))
    ]
    distances_df = pd.DataFrame(
        {
            "steam_id_1": [pair[0] for pair in steam_id_pairs],
            "steam_id_2": [pair[1] for pair in steam_id_pairs],
            "distance": dist_array,
        }
    )

    # Creating a mirror DataFrame with swapped steam_ids and adding the two together.
    # this is because we want to be able to look up via steam_id_1, and the way we did
    # calculations only provided things like
    # 1, 2, <some score>
    # 1, 3, <some score>
    # 2, 3, <some score>
    # and we would want to be able to look up via `steam_id_1`, so we wouldn't be able to
    # find anything to do with id 3
    swapped_df = distances_df.rename(
        columns={"steam_id_1": "steam_id_2", "steam_id_2": "steam_id_1"}
    )
    return pd.concat([distances_df, swapped_df])


# drastically faster than any direct insertions. Direct insertions took ~70 seconds while this takes ~5 seconds
def insert_recommendations(conn, df: pd.DataFrame):
    df.to_csv(RECOMMENDATION_CSV_LOCATION, index=False, header=False)
    set_full_permissions(RECOMMENDATION_CSV_LOCATION)
    with conn.cursor() as cursor:
        cursor.execute(COPY_CSV_SQL)
    conn.commit()


# I HATE using subprocess for this, but it's the only way to make this work for windows
def set_full_permissions(file_path):
    try:
        subprocess.run(["icacls", file_path, "/grant", "Everyone:F"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while setting permissions: {e}")


# run_recommendations()




# Your data as a multiline string
# data = """
# 260790\tPrecision Platformer\t1
# 260790\tPlatformer\t2
# 1966900\tAction Roguelike\t1
# 1966900\tPlatformer\t2
# 1966900\tPrecision Platformer\t3
# 123456\t2D\t1
# 123456\tRoguelite\t2
# 123456\tPrecision Platformer\t3
# """

# data = StringIO(data)

