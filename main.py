from data.databasse import create_data, create_table, add_entity
from view.home import Home
from data.data import Dataconnect
from constantes import IP, USER, PASSWORD, DB


def main():
    """ launches  the app """
    while True:
        try:
            data = Dataconnect(IP, USER, PASSWORD, DB)
        except Exception as e:
            print(e)
            create_data()
            data_init = Dataconnect(IP, USER, PASSWORD, DB)
            create_table(data_init)
            add_entity(data_init)
            data_init.close()
        home = Home(data)
        home.start()
