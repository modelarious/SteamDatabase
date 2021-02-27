class GameDAOPostgres:

    @staticmethod
    def commitGame(gameModel):
        #lmao don't sql injection yourself I guess
        sql = "INSERT INTO Games (steam_id, name_on_harddrive, path_on_harddrive, name_on_steam, avg_review_score) VALUES (%s);"
        data = (21354671253467, 'Fake', 'Entry', 'Oh Yeah', 9.2, )
        cur.execute(sql, data) # Note: no % operator


# x = '''
# INSERT INTO Games (steam_id, name_on_harddrive, path_on_harddrive, name_on_steam, avg_review_score) VALUES
#     (1976647, 'Tampopo', 'String', '1985-02-10', 5.4),
#     (2658854, 'Factorio', '/Volumes/GameDrive/Factorio', 'Factorio', 9.2);
# '''
# cursor.execute(x)