# #############################################################################
# Imports
# #############################################################################
import sqlite3
import sqlite3 as sql


# #############################################################################
# Class Database
# #############################################################################

class Database:

    def __init__(self, connexion):
        """
        End the initialization of the link with the database
        :param connexion: A SQL Connexion
        """

        self.__conn: sql.Connection = connexion
        self.__cursor: sql.Cursor = self.__conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.__cursor.close()
        self.__conn.close()

        return None

    def execute(self, command: str):
        """
        Execute a command on the database
        :param command: A SQL command
        :return: The result
        """
        try:
            self.__cursor.execute(command)
            return self.__cursor.fetchall()
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as e:
            with open("log", "a") as file:
                print(f"{e} due to {command}", file=file)

    def commit(self):
        """
        Commit the current database
        """
        self.__conn.commit()

    # #####################################
    # for origins

    def origin_set(self, position: str, x: int, y: int):
        self.execute(f"DELETE FROM `origin` WHERE `id`='{position}'")
        self.execute(f"INSERT INTO `origin`(`id`,`x`,`y`) VALUES('{position}',{x},{y})")
        self.commit()
        return None

    def origin_get(self, position: str):
        return self.execute(f"SELECT * FROM `origin` WHERE `id`='{position}'")

    # #####################################
    # for categories

    def category_add(self, name_cat: str, color: str):
        self.execute(f"INSERT INTO `category`(name,color) VALUES('{name_cat}','{color}')")
        self.commit()
        return None

    def category_remove(self, id_cat: int):
        self.execute(f"DELETE FROM `category` WHERE `id`={id_cat};")
        self.commit()
        return None

    def category_list(self):
        return self.execute(f"SELECT `id`,`name`,`color` FROM `category`;")

    def category_get(self, id_cat: int):
        return self.execute(f"SELECT `id`,`name` FROM `category` WHERE `id`={id_cat};")

    # #####################################
    # for points

    def point_add(self, point: str, category: int, x: int, y: int):
        self.execute(f"INSERT INTO `point`(`id`,`category`,`pos_x`,`pos_y`) VALUES('{point}',{category},{x},{y});")
        self.commit()
        return None

    def point_update(self, point: str, category: int, x: int, y: int):
        self.execute(f"UPDATE `point` SET `category`={category},`pos_x`={x},`pos_y`={y} WHERE `id`='{point}';")
        self.commit()
        return None

    def point_remove(self, point: str):
        self.execute(f"DELETE FROM `point` WHERE `id`='{point}';")
        self.commit()
        return None

    def point_get(self, point: str):
        return self.execute(f"SELECT * FROM `point` WHERE `id`='{point}';")

    def point_get_category(self, category: int):
        return self.execute(f"SELECT * FROM `point` WHERE `category`={category};")

    def point_get_all(self):
        return self.execute(f"SELECT * FROM `point`;")

    # #####################################
    # for paths

    def path_add(self, name_path: str):
        self.execute(f"INSERT INTO `path`(name) VALUES('{name_path}')")
        self.commit()
        return None

    def path_remove(self, id_path: int):
        self.execute(f"DELETE FROM `path_s_point` WHERE `path`={id_path}")
        self.execute(f"DELETE FROM `path` WHERE `id`={id_path}")
        self.commit()
        return None

    def path_list(self):
        return self.execute(f"SELECT `id`,`name` FROM `path`")

    def path_get(self, id_path: int):
        path = self.execute(f"SELECT `id`,`name` FROM `path` WHERE `id`={id_path}")
        points = self.execute(f"SELECT `point`,`point_next`,`minutes` FROM `path_s_point` WHERE `path`={id_path}")
        return path, points

    def path_point_add(self, id_path: int, id_point: str, id_previous: str = None):

        _next = id_point  # Dans le cas ou id_previous is None

        if id_previous is not None:
            _next = self.execute(f"SELECT `point_next` FROM `path_s_point` WHERE `path`={id_path} AND `point`='{id_previous}'")
            _next = _next[0][0]
            self.execute(f"UPDATE `path_s_point` SET `point_next`='{id_point}' WHERE `path`={id_path} AND `point`='{id_previous}'")

        self.execute(f"INSERT INTO `path_s_point`(`path`,`point`,`point_next`) VALUES({id_path},'{id_point}','{_next}')")

        self.commit()
        return None

    def path_point_get(self, id_path: int, id_point: str):
        return self.execute(f"SELECT * FROM `path_s_point` WHERE `path`={id_path} AND `point`='{id_point}'")

    def path_point_remove(self, id_path: int, id_point: str):
        _next, = self.execute(f"SELECT `point_next` FROM `path_s_point` WHERE `path`={id_path} AND `point`='{id_point}'")[0]
        self.execute(f"UPDATE `path_s_point` SET `point_next`='{_next}' WHERE `path`={id_path} AND `point_next`='{id_point}'")
        self.execute(f"DELETE FROM `path_s_point` WHERE `point`='{id_point}' AND `path`={id_path}")
        self.commit()
        return None

    def path_point_set_time(self, id_path: int, id_point: str, minutes: int):
        self.execute(f"UPDATE `path_s_point` SET `minutes`={minutes} WHERE `path`={id_path} AND `point`='{id_point}'")
        self.commit()
        return None

    # #####################################
    # for paths

    def vehicle_add(self, id: int, type: str, point: str):
        self.execute(f"INSERT INTO `vehicle`(`id`,`type`,`point`) VALUES({id},'{type}','{point}')")
        self.commit()
        return None

    def vehicle_remove(self, id_path: int):
        self.execute(f"DELETE FROM `vehicle` WHERE `id`={id_path};")
        self.commit()
        return None

    def vehicle_list(self):
        return self.execute(f"SELECT * FROM `vehicle`;")

    def vehicle_get(self, id: int):
        return self.execute(f"SELECT * FROM `vehicle` WHERE `id`={id}")

    def vehicle_set_pos(self, id: int, point: str):
        self.execute(f"UPDATE `vehicle` SET `point`='{point}' WHERE `id`={id}")
        self.commit()
        return None

    def vehicle_set_path(self, id: int, path: int):
        self.execute(f"UPDATE `vehicle` SET `path`={path} WHERE `id`={id}")
        self.commit()
        return None

    def vehicle_by_path(self, path: int):
        return self.execute(f"SELECT * FROM `vehicle` WHERE `path`={path}")

    def vehicle_set_hours(self, id: int, start: str, end: str):
        self.execute(f"UPDATE `vehicle` SET `depart`='{start}' ,`arrivee`='{end}' WHERE `id`={id}")
        self.commit()
        return None

    def vehicle_set_fill(self, id: int, mallette: int, kanban: int, consommable: int):
        self.execute(f"UPDATE `vehicle` SET `mallette`='{mallette}' ,`kanban`='{kanban}' \
                     ,`consommable`='{consommable}' WHERE `id`={id}")
        self.commit()
        return None

# #############################################################################
# Methods
# #############################################################################


def connect():
    """
    Connect to a database
    :return: A Database
    """

    conn = sql.connect("database.db")
    if conn is not None:
        conn.execute("PRAGMA foreign_keys = 1;")
        return Database(conn)
    else:
        return None


def set_tables(database: Database):
    """
    Create all the tables if they are not created already
    """

    if type(database) == Database:
        # Table des catégories
        database.execute("""
            CREATE TABLE IF NOT EXISTS `category` (
                `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
                `name`  TEXT    NOT NULL,
                `color` TEXT    NOT NULL
            );
        """)
        # Table des points
        database.execute("""
            CREATE TABLE IF NOT EXISTS `point` (
                `id`        TEXT    PRIMARY KEY,
                `category`  INTEGER NOT NULL REFERENCES `category`(`id`),
                `pos_x`     DOUBLE NOT NULL DEFAULT 0,
                `pos_y`     DOUBLE NOT NULL DEFAULT 0
            );
        """)
        # Table des itinéraires
        database.execute("""
            CREATE TABLE IF NOT EXISTS `path` (
                `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
                `name`  TEXT    NOT NULL
            );
        """)
        # Table des points sur itinéraire
        database.execute("""
            CREATE TABLE IF NOT EXISTS `path_s_point` (
                `id`            INTEGER PRIMARY KEY AUTOINCREMENT,
                `path`          INTEGER NOT NULL    REFERENCES `path`(`id`),
                `point`         TEXT NOT NULL       REFERENCES `point`(`id`),
                `point_next`    TEXT                REFERENCES `point`(`id`),
                `minutes`       INTEGER
            );
        """)
        # Table des véhicules
        database.execute("""
            CREATE TABLE IF NOT EXISTS `vehicle` (
                `id`        INTEGER NOT NULL,
                `type`      TEXT    NOT NULL,
                `path`      INTEGER REFERENCES `path`(`id`),
                `point`     TEXT    REFERENCES `point`(`id`),
                `depart`    TEXT,
                `arrivee`   TEXT,
                `mallette`  INTEGER NOT NULL DEFAULT 0,
                `kanban`    INTEGER NOT NULL DEFAULT 0,
                `consommable` INTEGER NOT NULL DEFAULT 0
            );
        """)
        # Table des origines map
        database.execute("""
            CREATE TABLE IF NOT EXISTS `origin` (
                `id`    CHAR(4),
                `x`     INTEGER NOT NULL,
                `y`     INTEGER NOT NULL,
                PRIMARY KEY (`id`)
            );
        """)
        # Commit
        database.commit()


def fill_tables(database: Database):
    """
    Insert data in the table for easier test
    """

    if type(database) == Database:
        database.execute("DELETE FROM `category`;")
        database.execute("DELETE FROM `point`;")
        database.execute("DELETE FROM `path`;")
        database.execute("DELETE FROM `path_s_point`;")
        database.execute("DELETE FROM `vehicle`;")
        print("[db] tables emptied")

        database.category_add("Arrêt", "violet")
        database.category_add("Point", "orange")
        print("[db] tables filled")


def execute(database: Database, cmd: str):
    global __cursor

    if type(database) == Database:
        return database.execute(cmd)

    return None


if __name__ == "__main__":

    with connect() as base:
        """
        print(base.vehicle_list())

        print(base.vehicle_add(721, "P80"))

        print(base.vehicle_list())
"""
        run = True
        while run:
            cmd = input("> ")
            if cmd == "exit":
                run = False
            elif cmd == "commit":
                base.commit()
            elif cmd == "set_table":
                set_tables(base)
            elif cmd == "fill_table":
                fill_tables(base)
            elif cmd == "init":
                set_tables(base)
                fill_tables(base)
                base.commit()
            else:
                ans = base.execute(cmd)
                if type(ans) == list:
                    for row in ans:
                        print(row)
                else:
                    print(ans)
