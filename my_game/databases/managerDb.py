import sqlite3


def create_table():
    data = sqlite3.connect('my_game/databases/game_data.db')
    cursor = data.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT UNIQUE,           
        max_countEnemies INTEGER,
        max_general_level INTEGER,
        max_level_health INTEGER,
        max_level_stamina INTEGER,
        max_level_cooldown INTEGER,
        max_level_melee_attack INTEGER,
        max_damage_done INTEGER
    )
    ''')

    data.commit()
    data.close()


def add_player(nickname):
    data = sqlite3.connect('my_game/databases/game_data.db')
    cursor = data.cursor()

    cursor.execute('''
    INSERT INTO scores (nickname, max_countEnemies, max_general_level, 
                        max_level_health, max_level_stamina,
                        max_level_cooldown, max_level_melee_attack, 
                        max_damage_done)
    VALUES (?, 0, 0, 0, 0, 0, 0, 0)
    ''', (nickname,))

    data.commit()
    data.close()


def reset_data():
    data = sqlite3.connect('my_game/databases/game_data.db')
    cursor = data.cursor()

    cursor.execute('''
    DROP TABLE IF EXISTS scores
    ''')

    data.commit()

    create_table()

    data.close()


def update_data(player, attribute, new_value):
    data = sqlite3.connect('my_game/databases/game_data.db')
    cursor = data.cursor()

    query_select = f'''
    SELECT {attribute} FROM scores
    WHERE nickname = ?
    '''

    cursor.execute(query_select, (player.nickname,))
    current_value = cursor.fetchone()

    if current_value:
        current_value = current_value[0]

        if new_value > current_value:
            query_update = f'''
            UPDATE scores 
            SET {attribute} = ?
            WHERE nickname = ?
            '''
            cursor.execute(query_update, (new_value, player.nickname))

    data.commit()
    data.close()


def update_all_data(player):
    update_data(player, 'max_general_level', player.level)
    update_data(player, 'max_level_health', player.level_health)
    update_data(player, 'max_level_stamina', player.level_stamina)
    update_data(player, 'max_level_cooldown', player.level_cooldown)
    update_data(player, 'max_level_melee_attack', player.level_melee_attack)
    update_data(player, 'max_countEnemies', player.countEnemies)
    update_data(player, 'max_damage_done', player.damage_done)


def get_player_ratings():
    with sqlite3.connect('my_game/databases/game_data.db') as data:
        cursor = data.cursor()
        cursor.execute('''SELECT nickname, max_countEnemies, 
        max_general_level, max_level_health,
        max_level_stamina, max_level_cooldown,
        max_level_melee_attack, max_damage_done  
        FROM scores ORDER BY max_countEnemies DESC''')
        return cursor.fetchall()