from model.produit import Produit
from data.data import Dataconnect
from constantes import IP, USER, PASSWORD, DB


class Home:
    """class home """
    def __init__(self, data):
        self.data = data

    def choix(self, val):
        """class method for check the result """
        while True:
            try:
                choix = int(input("Veuillez entrer un nombre : "))
                if choix <= val and choix > 0:
                    return choix
                    break
            except ValueError:
                print("")

    def search(self, home):
        """class method for browse the category and the product  """
        data = self.data
        data.req("SELECT * from category ")
        row = data.req_return
        maxi = len(row)
        i = 0
        print("nombre de categories dispo:", maxi)
        while i < maxi:
            print(i + 1, row[i][1])
            i += 1

        choix = home.choix(maxi)
        req = "select * from produit where category_id ='" + str(choix) + "'"
        data.req(req)
        rowproduit = data.req_return
        maxi = len(rowproduit)
        list_product = []
        i = 0
        print("nombre de produit dispo:", maxi)
        while i < maxi:
            product = Produit(rowproduit[i][0],
                              rowproduit[i][1], rowproduit[i][2],
                              rowproduit[i][3], rowproduit[i][4],
                              rowproduit[i][5])
            print(i + 1, product.nom)
            list_product.append(product)
            i += 1

        choixproduit = home.choix(maxi)
        print("produit selectionner", "\n")
        choixproduit = int(choixproduit - 1)
        print("nom:", list_product[choixproduit].nom)
        print("description:", list_product[choixproduit].description)
        # cpt = 0
        # tab = list_product[choixproduit - 1].magasin.split(",")
        # max = len(tab)
        cpt = 0

        print("magasin:")

        tab = data.getMagasin(list_product[choixproduit].id,  list_product[choixproduit].category_id)
        cpt = 0
        max = len(tab)
        while cpt < max:
            store = data.getStore(tab[cpt])
            print(store.nom)
            cpt += 1
        print("url:", list_product[choixproduit].url)
        print("nutriScrore:",
              list_product[choixproduit].nutri_score)

        if list_product[choixproduit].nutri_score > 1:
            print("1 - trouver un substitue de "
                  "meilleur qualité  ?")
            print("2 - Sauvegarder alliment.")
            print("3 - Nouvelle recherche.")
            choixs = home.choix(3)
            if choixs == 1:
                value = 0
                while value == 0:
                    pro = list_product[choixproduit]
                    value = list_product[choixproduit].substitution(data,
                                                                        pro)
                home.start()
            elif choixs == 2:
                pro = None
                list_product[choixproduit].save(data, pro)
                home.start()
            elif choixs == 3:
                data = Dataconnect(IP, USER, PASSWORD, DB)
                home = Home(data)
                data.close()
                data = Dataconnect(IP, USER, PASSWORD, DB)
                home = Home(data)
                home.start()

        else:
            # TOUT MARCHE
            print("il n'existe pas mieux! ")
            print("1 - Sauvegarder alliment.")
            print("2 - Nouvelle recherche.")
            choixt = home.choix(2)
            if choixt == 1:
                list_product[choixproduit].save(data)
                home.start()
            else:
                data.close()
                data = Dataconnect(IP, USER, PASSWORD, DB)
                home = Home(data)
                home.start()

    def start(self):
        """class method for lunch the home """
        data = self.data
        home = Home(data)
        print("1 - Quel aliment souhaitez-vous remplacer ?")
        print("2 - Retrouver mes aliments substitués.")
        print("3 - recrée base")
        choix = home.choix(3)
        if choix == 1:
            home.search(home)

        elif choix == 2:
            from data.databasse import favory_read
            data.close()
            data = Dataconnect(IP, USER, PASSWORD, DB)
            favory_read(data)

        elif choix == 3:
            from data.databasse import create_table, drop_data,\
                create_data, add_entity, add_store
            drop_data()
            create_data()
            data_init = Dataconnect(IP, USER, PASSWORD, DB)
            create_table(data_init)
            add_store(data_init)
            add_entity(data_init)
            data_init.close()
