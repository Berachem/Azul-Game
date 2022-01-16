"""Module qui répertorie les fonctions relatives aux joueurs directement :
comptage de points, création des joueurs..."""

import os
from upemtk import *
from plateau import *
from random import randint, shuffle



hauteur,largeur = 1000,1000
pos_zone_centre = (350,100)
l_couleurs = ["#D58270", "#9BD570", "#70D5C1", "#707FD5", "#D270D5"]

if "patern_tuiles.txt" in os.listdir():
    with open("patern_tuiles.txt","r") as f:
        l_couleurs = eval(f.readline())
else:
    l_couleurs = ["#D58270", "#9BD570", "#70D5C1", "#707FD5", "#D270D5"]

def creer_sac_tuile():
    """Créer un sac de 100 tuiles de couleurs de façon aléatoire, composé de 20 couleurs de chaque"""
    sac = [0]*100
    print("Le sac de tuiles vient d'etre cree et est de taille 100.")
    for i in range(len(l_couleurs)):
        for j in range(20):
            sac[i*20+j]=l_couleurs[i]
    shuffle(sac)
    return sac


def creer_fabrique_tuiles(nb_joueurs,sac, defausse):
    """
    Renvoie une liste de dictionnaires contenant les données liées aux tuiles
    comme leur position et leurs tuiles de départ (il y en a 4).
    Ces 4 tuiles sont retirés aux hasard du sac
    """
    base = (largeur//2-90,hauteur//2)
    cote_carre = 200
    l_coord_fabriques = [(base[0],base[1]),
                         (base[0]+cote_carre,base[1]),
                         (base[0]+cote_carre,base[1]-cote_carre),
                         (base[0],base[1]-cote_carre),
                         (base[0]+cote_carre//2,base[1]-cote_carre//2),
                         (base[0]+cote_carre//2,base[1]),
                         (base[0]+cote_carre//2,base[1]-cote_carre),
                         (base[0],base[1]-cote_carre//2),
                         (base[0]+cote_carre,base[1]-cote_carre//2),
                         ]
    fabriques = []
    nb_fabriques = 5+(nb_joueurs-2)*2
    for i in range(nb_fabriques):
        if sac == []:
            sac = defausse
        if sac != []:
            fabriques.append({"pos": l_coord_fabriques[i],
                            "tuiles" : [sac.pop(randint(0,len(sac)-1)) for _ in range(4)]})
    return fabriques


def creation_joueurs(nb_joueurs,bot):
    """
    Renvoie la liste joueurs:
    chaque element est un dictionnaire regroupant les attributs d'un joueur :
        nom, score,penalites, pos_plateau, grille_a_placement,grille_connexions
    """
    joueurs = []
    pos_plateaux = [(0, 375), (700, 375),(0,100), (700, 100)]
    for i in range(nb_joueurs):
        if i == 0 or i == 2:
            joueurs.append({"nom":f'joueur {i+1}',
            "bot" : bot[i],
            "score":0,
            "penalites":0,
            "pos_plateau" : (pos_plateaux[i][0]+50,pos_plateaux[i][1]),
            "pos_mur" : (pos_plateaux[i][0]+170,pos_plateaux[i][1]+30),
            "pos_lignes_motif":(pos_plateaux[i][0]+125,pos_plateaux[i][1]+30),
            "pos_plancher":(pos_plateaux[i][0]+25, pos_plateaux[i][1]+170),
            "pos_score":(pos_plateaux[i][0]+50,pos_plateaux[i][1]-20),
            "motif" : [["" for _ in range(i)] for i in range(1,6)],
            "plancher": ["" for _ in range(7)],
            "mur" : creation_grille_connexion(),
            "sens":"gauche"})
        else:
            joueurs.append({"nom":f'joueur {i+1}',
            "bot" : bot[i],
            "score":0,
            "penalites":0,
            "pos_plateau" : (pos_plateaux[i][0]+50,pos_plateaux[i][1]),
            "pos_mur" : (pos_plateaux[i][0]+25,pos_plateaux[i][1]+30),
            "pos_lignes_motif":(pos_plateaux[i][0]+170,pos_plateaux[i][1]+30),
            "pos_plancher":(pos_plateaux[i][0]+25, pos_plateaux[i][1]+170),
            "pos_score":(pos_plateaux[i][0]+50,pos_plateaux[i][1]-20),
            "motif" : [["" for _ in range(i)] for i in range(1,6)],
            "plancher": ["" for _ in range(7)],
            "mur" : creation_grille_connexion(),
            "sens":"droite"})
    return joueurs


def zone_clique(x, y, pos_x, pos_y, taille):
    """
    renvoie true les coordonnées (x;y) se trouve dans la plage de la pos_x à la pos_x
    """
    return pos_x <= x <= pos_x+taille and pos_y <= y <= pos_y + taille


def choisie_tuile(fabriques, tuiles_zone_centre, tuile_permier_joueur, x, y):
    """
    recuperer les tuiles de la zone du clique
    """
    nb_tuiles_zone_centre = len(tuiles_zone_centre)
    dimension_zone_centre = min(nb_tuiles_zone_centre, 7), nb_tuiles_zone_centre//7
    r = 40
    for i in range(len(fabriques)):
        if x > fabriques[i]["pos"][0]-r and x < fabriques[i]["pos"][0]+r and y > fabriques[i]["pos"][1]-r and y < fabriques[i]["pos"][1]+r and fabriques[i]["tuiles"]:
            # si les coordonne du clic sont encadrer par la fabrique
            tuiles, tuiles_zone_centre = choisie_zone_cercle(x, y, fabriques[i]["pos"][0], fabriques[i]["pos"][1], fabriques[i], tuiles_zone_centre)
            fabriques[i]['tuiles'] = []
            return tuiles, fabriques, tuiles_zone_centre, tuile_permier_joueur, "fabrique"
    if tuiles_zone_centre != []:
        # si le centre n'est pas vide, appel la fonction qui verifie si on clic dans la zone centre et qui fait les modification
        resultat = recup_tuiles_dans_zone_centre(tuiles_zone_centre, tuile_permier_joueur, nb_tuiles_zone_centre, x, y, fabriques)
        if resultat:
            resultat = list(resultat)
            resultat.append("centre")
            return resultat
            # si des modification on eu lieu, alors on les renvoie, cela veut dire que le joueur a choisi des tuiles
    return [], fabriques, tuiles_zone_centre, tuile_permier_joueur, None



def choisie_zone_cercle(x, y, pos_x, pos_y, fabrique, tuiles_zone_centre):
    """
    savoir quel tuile de la fabrique on a cliquer et récupérer toute les tuiles
    de cette couleur
    """
    if y <= pos_y:
        if x <= pos_x:
            tuiles, tuiles_zone_centre = recup_tuiles(fabrique, 0, tuiles_zone_centre)
            # si c'est la zone en haut a gauche, recupere les tuile de la meme couleur que celle de cette zone
        elif x > pos_x:
            tuiles, tuiles_zone_centre = recup_tuiles(fabrique, 1, tuiles_zone_centre)
            # si c'est la zone en haut a droite, recupere les tuile de la meme couleur que celle de cette zone
    elif y >= pos_y:
        if x <= pos_x:
            tuiles, tuiles_zone_centre = recup_tuiles(fabrique, 2, tuiles_zone_centre)
            # si c'est la zone en bas a gauche, recupere les tuile de la meme couleur que celle de cette zone
        elif x > pos_x:
            tuiles, tuiles_zone_centre = recup_tuiles(fabrique, 3, tuiles_zone_centre)
            # si c'est la zone en bas a droite, recupere les tuile de la meme couleur que celle de cette zone
    return tuiles, tuiles_zone_centre


def recup_tuiles_dans_zone_centre(tuiles_zone_centre, tuile_permier_joueur, nb_tuiles_zone_centre, x, y, fabriques):
    """
    verifie si l'on clique sur une tuile du centre et recupere les tuiles choisi
    """
    for i in range(nb_tuiles_zone_centre):
        if zone_clique(x, y, 350+25*(i%11), 100+25*(i//11), 25):
            tuiles, tuiles_zone_centre, tuile_permier_joueur = recup_centre(tuiles_zone_centre[i], tuiles_zone_centre, tuile_permier_joueur)
            return tuiles, fabriques, tuiles_zone_centre, tuile_permier_joueur


def recup_centre(tuile_choisi, tuiles_zone_centre, tuile_permier_joueur):
    """
    recuperer toute les tuiles de la zone centre de la meme couleur que
    la tuile choisie
    """
    tuiles = []
    nombre = tuiles_zone_centre.count(tuile_choisi)
    # corespond au nombre de tuile de la meme couleur que la tuile choisie
    for i in range(nombre):
        tuiles_zone_centre.remove(tuile_choisi)
    # supprime toute les tuiles de la meme couleur sue la tuile choisi
    resultat = [tuile_choisi]*nombre
    if tuile_permier_joueur:
        resultat.append("premier_joueur")
        tuile_permier_joueur = False
    # le resultat correspond au tuiles choisit, auquel on rajoute la tuile premier joueur si besoin
    return resultat, tuiles_zone_centre, tuile_permier_joueur


def recup_tuiles(fabrique, tuille_choisi, tuiles_zone_centre):
    """
    recupere les tuiles de la meme couleur que la tuile choisie
    et place le reste dans la zone du centre
    """
    tuiles = []
    for element in fabrique["tuiles"]:
        if element == fabrique["tuiles"][tuille_choisi]:
            tuiles.append(element)
            # rajoute la tuile dans les tuiles que l'on a choisit si elle est de la meme couleur
        else:
            tuiles_zone_centre.append(element)
            # la met dans la zone du centre si elle n'est pas de la meme couleur
    return tuiles, tuiles_zone_centre


def zone_clique(x, y, pos_x, pos_y, taille):
    """
    verifie si on a cliquer dans la zone qui commence à pos_x, pos_y
    qui est d'une certaine taille
    """
    return x >= pos_x and x <= pos_x+taille and y >= pos_y and y <= pos_y + taille


def verif_clique_dans_ligne_motif(nb_tuiles, tuiles_choisi, joueur, sens, x, y):
    """
    verifie pour chaque case si on a cliquer sur la case de la ligne motif
    et si oui renvoie le placement des tuiles sur la ligne qui correspond
    """
    for i in range(len(joueur["motif"])):
        for a in range(len(joueur["motif"][i])):
            x_case, y_case = position_case_ligne_motif(joueur["pos_lignes_motif"], sens, a, i)
            if zone_clique(x, y, x_case, y_case, 20):
                if verif_ligne_mur_valide(joueur["mur"][i], tuiles_choisi):
                    return placement_tuiles_dans_ligne_motif(nb_tuiles, i, tuiles_choisi, joueur)

def verif_clique_dans_plancher(nb_tuiles, tuiles_choisi, joueur, x, y):
    """
    place les tuiles dans le plangher si on a cliquer dessus
    """
    if zone_clique(x, y, joueur["pos_plancher"][0], joueur["pos_plancher"][1], 140):
        for c in range(nb_tuiles):
            if joueur["plancher"].count("") == 0:
                return joueur
                # si le plancher est remplie alors on arrete de le remplir
            joueur["plancher"].insert(0, tuiles_choisi[c])
            joueur["plancher"].remove("")
        return joueur


def verif_ligne_mur_valide(ligne, tuiles):
    for case in ligne:
        if case[0] == tuiles[0]:
            return case[1] == False

def placement_tuiles_dans_ligne_motif(nb_tuiles, ligne, tuiles_choisi, joueur):
    """
    place les tuiles que l'on avait choisie dans une des ligne en fonction de :
        la ligne que l'on a choisit de remplir
        les tuiles deja presente sur la ligne
        les tuiles que l'on a choisit (notament les cas particulier
        comme la tuile premier joueur)
    """
    while True:
        taille_ligne = len(joueur["motif"][ligne])
        ind_courant = avoir_ind_courant(joueur["motif"][ligne])
        for c in range(nb_tuiles):
            if ind_courant+c < taille_ligne:
                if joueur["motif"][ligne][0] == tuiles_choisi[c] or joueur["motif"][ligne][0] == "" and tuiles_choisi[c] != "premier_joueur":
                    if tuiles_choisi[0] == "premier_joueur":
                        joueur["motif"][ligne][ind_courant+c-1] = tuiles_choisi[c]
                    else:
                        joueur["motif"][ligne][ind_courant+c] = tuiles_choisi[c]
                else:
                    if joueur["nom"] != "Automat":
                        joueur["plancher"].insert(0, tuiles_choisi[c])

            elif tuiles_choisi[c] == "premier_joueur":
                taille_ligne -= 1
                if joueur["nom"] != "Automat":
                    joueur["plancher"].insert(0, tuiles_choisi[c])
            else:
                if joueur["nom"] != "Automat":
                    joueur["plancher"].insert(0, tuiles_choisi[c])
        return joueur


def position_case_ligne_motif(pos_ligne_motif, sens, colonne, ligne):
    """
    renvoie la position de la case en fontion du sens des lignes
    """
    x_debut, y_debut = pos_ligne_motif
    if sens=="gauche":
        x_case = x_debut-colonne*25
    else:
        x_case = x_debut+colonne*25
    return x_case, y_debut+ligne*25


def avoir_ind_courant(ligne):
    """
    renvoie le nombre de case remplie dans la ligne motif
    """
    ind_courant = 0
    for case in ligne:
        if case !="":
            ind_courant+=1
    return ind_courant


def fabriques_sont_vides(fabriques):
    """Renvoie True si toutes les fabriques ne comportent plus de tuiles
    sinon False"""
    for f in fabriques:
        if len(f["tuiles"]) != 0: return False
    return True


def remettre_tuile_dans_fabrique(nb_tuiles, fabriques, tuiles_choisi, tuiles_zone_centre, x, y):
    """
    remet les tuiles dans la fabrique, en mettant d'abord celle selectionner,
    puis celle qui sont sencé être dans la zone centre
    """
    r = 40
    for i in range(len(fabriques)):
        if x > fabriques[i]["pos"][0]-r and x < fabriques[i]["pos"][0]+r and y > fabriques[i]["pos"][1]-r and y < fabriques[i]["pos"][1]+r and not fabriques[i]["tuiles"]:
            for a in range(nb_tuiles):
                fabriques[i]["tuiles"].append(tuiles_choisi[a])
            for a in range(4-nb_tuiles):
                fabriques[i]["tuiles"].append(tuiles_zone_centre.pop(-1))
            return fabriques


def remettre_tuile_dans_zone_centre(nb_tuiles, tuiles_choisi, tuiles_zone_centre, x, y):
    """
    remet dans le centre les tuies que l'on avait selectionner avant si il y a
    un clic au centre
    """
    if zone_clique(x, y, 350, 100, 275):
        for i in range(nb_tuiles):
            if tuiles_choisi[i] != "premier_joueur":
                tuiles_zone_centre.append(tuiles_choisi[i])
            # on garde la tuile premier joueur et on met le reste dans zone centre
        return tuiles_zone_centre


def offre_de_fabriques(fabriques, joueurs, bot, mode_bot,automat=False):
    """
    Fonction qui s'occupe de l'offre des fabriques en proposant aux joueurs des tuiles
    et qui gèrent les différents choix et la gestion des tuiles choisis sur les plateaux
    des joueurs
    si le joueur et une IA alors elle appelle la fonction qui gère l'IA
    """
    tuiles_zone_centre = []
    tuile_permier_joueur = True
    tour,num_joueur = 0,0
    
    while not(fabriques_sont_vides(fabriques)) or len(tuiles_zone_centre)  != 0 :
        # tant qu'il reste des tuile a placer quelque part
        tuiles_choisi = []
        num_joueur = num_joueur%len(joueurs)

        efface("tour")
        texte(360,10,f"Le joueur {num_joueur+1} choisie !", taille=20,couleur="White",tag="tour",police="Copperplate gothic bold")

        # pour savoir quel joueur joue
        if bot[num_joueur]: # si le joueur est une IA
            tuiles_choisi, tuile_permier_joueur = gestion_choix_ordi(joueurs[num_joueur], fabriques, tuiles_zone_centre, tuile_permier_joueur, mode_bot,automat=automat)
            # gere les choix de l'ordi
            attente_clic()
        else:
            tuiles_choisi, tuile_permier_joueur = gestion_choix_joueur(num_joueur, joueurs, fabriques, tuiles_choisi, tuiles_zone_centre, tuile_permier_joueur)
            if not tuiles_choisi:
                return True
            # gere les choix du joueure
        print("Le joueur ",num_joueur+1," a choisi les tuiles : ",tuiles_choisi)
        if num_joueur+1 == len(joueurs):
            print("--------------------------------------------------------------------")
        dessin_fabriques(fabriques)
        dessin_lignes_motif(joueurs[num_joueur])
        dessin_plancher(joueurs[num_joueur])
        dessin_zone_centre(pos_zone_centre[0],pos_zone_centre[1],tuiles_zone_centre)
        # dessine les dernieres modifications et affiche au terminal quel tuiles ont ete choisi et le plancher du joueur
        num_joueur+=1
        tour+=1
        # change le tour, le joueur qui joue, et le sens qui sert a savoir dans quel sens est le plateau du joueur


def gestion_choix_ordi(joueur, fabriques, tuiles_zone_centre, tuile_permier_joueur, mode_bot,automat=False):
    """
    simule une IA en prennant des fabrique au hazard qui ne sont pas vide et
    en choisissant au hazard une tuile dedans, si toute les fabriques sont vide
    il prend dans la zone du centre
    """
    nb_fabrique = len(fabriques)
    tuiles_choisi= None
    tuile_plus_nombreuse = recherche_tuiles_plus_ou_moins_nombreuse(tuiles_zone_centre, 1)
    tuile_moins_nombreuse = recherche_tuiles_plus_ou_moins_nombreuse(tuiles_zone_centre, -1)
    # recherche la tuile la plus nombreuse dans la zone du centte
    # recherche la tuile la moins nombreuse dans la zone du centte
    while True:

        if mode_bot == "difficile":
            tuiles_choisi, tuiles_zone_centre, tuile_permier_joueur, ligne = gestion_choix_mode_difficile(joueur, fabriques, tuiles_zone_centre, tuile_permier_joueur)
        elif fabriques_sont_vides(fabriques) or (mode_bot == "longue" and tuile_plus_nombreuse[1] > 2):
            if tuiles_zone_centre:
                choix_tuile = gestion_bot_zone_centre(mode_bot, tuile_plus_nombreuse, tuile_moins_nombreuse, tuiles_zone_centre)
                tuiles_choisi, tuiles_zone_centre, tuile_permier_joueur = recup_centre(choix_tuile, tuiles_zone_centre, tuile_permier_joueur)
            # si les fabriques sont vide il prend la zone du centre
        else:
            if mode_bot == "longue":
                tuile_plus_nombreuse, choix_tuile, choix_fabrique = gestion_choix_mode_long(fabriques)
            elif mode_bot == "rapide":
                tuile_moins_nombreuse, choix_tuile, choix_fabrique = gestion_choix_mode_rapide(fabriques)
            else:
                choix_fabrique = randint(0, nb_fabrique-1)
                choix_tuile = randint(0, 3)
                # choisit une fabrique au hazard
            if fabriques[choix_fabrique]["tuiles"] != []:
                tuiles_choisi, tuiles_zone_centre = recup_tuiles(fabriques[choix_fabrique], choix_tuile, tuiles_zone_centre)
                fabriques[choix_fabrique]["tuiles"] = []
            # si la fabrique n'est pas vide, choisit une des tuiles au hazard et recupere toute celle de la meme couleur
        if tuiles_choisi:
            # si les tuiles on ete choisi on les place dans les ligne motif
            ############################################################################attente_touche_jusqua(400)
            nb_lignes = len(joueur["motif"])
            nb_tuiles = len(tuiles_choisi)

            if mode_bot == "longue":
                return gestion_placement_bot_long(joueur, nb_lignes, nb_tuiles, tuiles_choisi, tuile_permier_joueur)
            elif mode_bot == "difficile":
                joueur = placement_tuiles_dans_ligne_motif(nb_tuiles, ligne, tuiles_choisi, joueur)
                return tuiles_choisi, tuile_permier_joueur
            elif mode_bot == "facile":
                return gestion_placement_bot_facile(joueur, nb_lignes, nb_tuiles, tuiles_choisi, tuile_permier_joueur)
            else:
                return gestion_placement_bot_rapide(joueur, nb_lignes, nb_tuiles, tuiles_choisi, tuile_permier_joueur)

def gestion_choix_mode_difficile(joueur, fabriques, tuiles_zone_centre, tuile_permier_joueur):
    """
    sert à savoir quel tuile vas être choisit par le bot, et à quellle ligne,
    si le bot est en mode difficile
    il cherche la meilleurs option dans les tuiles proposer c'est à dir celle
    qui va lui donné le meilleur score sur le coup
    meilleur_coup enregistre le score, la ligne, la couleur de la tuile
    le numéro de la fabrique et si elle se trouve dans une fabrique ou dans la
    zone du centre (si c'est la zone du centre alors le numéro de fabrique sera 10)
    on peut surement grouper les deux dernière valeur mais dans mon cas cela provoquait des bugs
    """
    meilleur_coup = [-100, 0, "", 10, tuiles_zone_centre]
    for num_fabrique in range(len(fabriques)):
        for tuile in fabriques[num_fabrique]["tuiles"]:
            meilleur_coup = verif_meilleur_coup(joueur, tuile, meilleur_coup, fabriques[num_fabrique]["tuiles"], num_fabrique, tuile_permier_joueur)
    for tuile in tuiles_zone_centre:
        meilleur_coup = verif_meilleur_coup(joueur, tuile, meilleur_coup, tuiles_zone_centre, 10, tuile_permier_joueur)
    if meilleur_coup[3] == 10:
        tuiles_choisi, tuiles_zone_centre, tuile_permier_joueur = recup_centre(meilleur_coup[2], tuiles_zone_centre, tuile_permier_joueur)
        return tuiles_choisi, tuiles_zone_centre, tuile_permier_joueur, meilleur_coup[1]
    else:
        tuiles_choisi, tuiles_zone_centre = recup_tuiles(fabriques[meilleur_coup[3]], fabriques[meilleur_coup[3]]["tuiles"].index(meilleur_coup[2]), tuiles_zone_centre)
        fabriques[meilleur_coup[3]]["tuiles"] = []
        return tuiles_choisi, tuiles_zone_centre, tuile_permier_joueur, meilleur_coup[1]

def gestion_choix_mode_long(fabriques):
    """
    sert à choisir quel tuile vas être choisit par le bot si il est en mode partie longue
    ils prendra le plus de tuiles possible
    """
    tuile_plus_nombreuse = [None, 0]
    choix_fabrique = None
    for num_fabrique in range(len(fabriques)):
        tuile_plus_nombreuse_fabrique = recherche_tuiles_plus_ou_moins_nombreuse(fabriques[num_fabrique]["tuiles"], 1)
        if tuile_plus_nombreuse_fabrique[1] > tuile_plus_nombreuse[1]:
            tuile_plus_nombreuse = tuile_plus_nombreuse_fabrique
            choix_tuile = fabriques[num_fabrique]["tuiles"].index(tuile_plus_nombreuse_fabrique[0])
            choix_fabrique = num_fabrique
    return tuile_plus_nombreuse, choix_tuile, choix_fabrique

def gestion_placement_bot_long(joueur, nb_lignes, nb_tuiles, tuiles_choisi, tuile_permier_joueur):
    """
    sert à placer les tuiles que le bot à choisit si il est en mode long
    il mettra les tuiles le plus bas possible
    """
    for i in range(nb_lignes):
        if joueur["motif"][nb_lignes-1-i][0] == "" or joueur["motif"][nb_lignes-1-i][0] == tuiles_choisi[0]:
            if [tuiles_choisi[0], False] in joueur["mur"][nb_lignes-1-i]:
                # pour qu'il choisisse la ligne la plus basse du mur qui ne soit pas remplie par une autre couleur
                # et qui n'a pas encore été mis dans le mur
                # simule un semblant de plan de jeu (meme si en realite l'ordi est un peu bete)
                joueur = placement_tuiles_dans_ligne_motif(nb_tuiles, nb_lignes-1-i, tuiles_choisi, joueur)
                return tuiles_choisi, tuile_permier_joueur
    joueur = placement_tuiles_dans_ligne_motif(nb_tuiles, nb_lignes-1-i, tuiles_choisi, joueur)
    return tuiles_choisi, tuile_permier_joueur

def gestion_choix_mode_rapide(fabriques):
    """
    sert à choisir quel tuile vas être choisit par le bot si il est en mode partie rapide
    ils prendra le moins de tuiles possible
    """
    tuile_moins_nombreuse = [None, 10]
    choix_fabrique = None
    for num_fabrique in range(len(fabriques)):
        tuile_moins_nombreuse_fabrique = recherche_tuiles_plus_ou_moins_nombreuse(fabriques[num_fabrique]["tuiles"], -1)
        if tuile_moins_nombreuse_fabrique[1] < tuile_moins_nombreuse[1]:
            tuile_moins_nombreuse = tuile_moins_nombreuse_fabrique
            choix_tuile = fabriques[num_fabrique]["tuiles"].index(tuile_moins_nombreuse[0])
            choix_fabrique = num_fabrique
    return tuile_moins_nombreuse, choix_tuile, choix_fabrique

def gestion_placement_bot_rapide(joueur, nb_lignes, nb_tuiles, tuiles_choisi, tuile_permier_joueur):
    """
    sert à placer les tuiles que le bot à choisit si il est en mode rapide
    il mettra les tuiles le plus haut possible
    """
    for i in range(nb_lignes):
        if joueur["motif"][i][0] == "" or joueur["motif"][i][0] == tuiles_choisi[0]:
            if [tuiles_choisi[0], False] in joueur["mur"][i]:
                # pour qu'il choisisse la ligne la plus haute du mur qui ne soit pas remplie par une autre couleur
                # et qui n'a pas encore été mis dans le mur
                # simule un semblant de plan de jeu (meme si en realite l'ordi est un peu bete)
                joueur = placement_tuiles_dans_ligne_motif(nb_tuiles, i, tuiles_choisi, joueur)
                return tuiles_choisi, tuile_permier_joueur
    joueur = placement_tuiles_dans_ligne_motif(nb_tuiles, i, tuiles_choisi, joueur)
    return tuiles_choisi, tuile_permier_joueur

def gestion_placement_bot_facile(joueur, nb_lignes, nb_tuiles, tuiles_choisi, tuile_permier_joueur):
    """
    sert à placer les tuiles que le bot à choisit si il est en mode facile
    il mettra les tuiles de manière aléatoire
    """
    ligne = randint(0, nb_lignes-1)
    joueur = placement_tuiles_dans_ligne_motif(nb_tuiles, ligne, tuiles_choisi, joueur)
    return tuiles_choisi, tuile_permier_joueur

def gestion_bot_zone_centre(mode_bot, tuile_plus_nombreuse, tuile_moins_nombreuse, tuiles_zone_centre):
    """
    gère les actions des bots dans le cas où il ne reste des tuiles que sur la zone du centre
    un prendra le plus de tuile possible
    l'autre le moins
    le dernier prendra de façon aléatoire
    """
    if mode_bot == "longue":
        return tuile_plus_nombreuse[0]
    elif mode_bot == "rapide":
        return tuile_moins_nombreuse[0]
    else:
        return tuiles_zone_centre[randint(0, len(tuiles_zone_centre)-1)]

def gestion_choix_joueur(num_joueur, joueurs, fabriques, tuiles_choisi, tuiles_zone_centre, tuile_permier_joueur):
    """
    fonction regroupant toutes les interaction du joueur avec la fabrique, les grillage, les tuilles etc...
    renvoie les modification lorsque les selection sont "valide" c'est à dire
    que le joueur a tout choisi, les tuilles comme les lignes dans lesquels il les met
    si le joueur appuie sur echap, alors cela ferme la fenetre
    """
    nb_tuiles = 0
    zone = []
    while True:
        nb_tuiles = len(tuiles_choisi)
        touche = attente_clic_ou_touche()
        if touche[2] == 'Touche':
            if touche[1] == 'Escape':
                return False, False
        elif tuiles_choisi == []: # si il n'a pas choisit de tuile (ou qu'il a renoncer au choix precedent)
            tuiles_choisi, fabriques, tuiles_zone_centre, tuile_permier_joueur, zone = choisie_tuile(fabriques, tuiles_zone_centre, tuile_permier_joueur, touche[0], touche[1])
            dessin_fabriques(fabriques)
            dessin_zone_centre(pos_zone_centre[0],pos_zone_centre[1],tuiles_zone_centre)
            # choisit ses tuiles et met a jour l'affichage
        else: # si il a choisit ses tuiles
            if touche[2] == 'ClicGauche':
                if verif_clique_dans_ligne_motif(nb_tuiles, tuiles_choisi, joueurs[num_joueur], joueurs[num_joueur]["sens"], touche[0], touche[1]):
                    return tuiles_choisi, tuile_permier_joueur
                elif verif_clique_dans_plancher(nb_tuiles, tuiles_choisi, joueurs[num_joueur], touche[0], touche[1]):
                    return tuiles_choisi, tuile_permier_joueur
                # termine la fonction si il a cliquer sur la ligne motif ou le plancher (en faisant les modification que cela implique)
                elif (zone == "fabrique" and remettre_tuile_dans_fabrique(nb_tuiles, fabriques, tuiles_choisi, tuiles_zone_centre, touche[0], touche[1])) or (zone == "centre" and remettre_tuile_dans_zone_centre(nb_tuiles, tuiles_choisi, tuiles_zone_centre, touche[0], touche[1])):
                    # zone correspond a la zone dans laquel il avait cliquer precedement, si il reclique dans cette zone
                    # alors en plus des modification faites par les fonctions remettre, on annule les tuiles coisit
                    # et on reactive la tuile premier joueur si necessaire
                    if "premier_joueur" in tuiles_choisi:
                        tuile_permier_joueur = True
                    tuiles_choisi = []
                    dessin_fabriques(fabriques)
                    dessin_zone_centre(pos_zone_centre[0],pos_zone_centre[1],tuiles_zone_centre)


#=============================================================
# AMORCE PHASE 2
#=============================================================

def decoration_mur(joueurs, defausse):
    """
    Fonction qui s'occupe de remplie les murs de fabriques de chaque joueur et actualise leurs murs
    """
    for j in joueurs:
        rempli_case_mur(j, defausse)
        dessin_mur(j)
        print(j["nom"], " est à",j["score"]," points!")
    attente_clic()
    vider_plancher(joueurs)
    efface("score")
    efface("tuile")
    dessin_plateau_joueurs(joueurs)



def rempli_case_mur(joueur, defausse):
    """
    Ajoute la tuile dans le mur du joueur en ajoutant les points gagnés au score du joueur
    (et ça efface la ligne motif concernée)
    """
    for i in range(len(joueur["motif"])):
        couleur_dernier_ind = joueur["motif"][i][-1]
        couleur_ind_zero = joueur["motif"][i][0]
        if couleur_ind_zero==couleur_dernier_ind and couleur_ind_zero != "":
            if [couleur_ind_zero,False] in joueur["mur"][i]:
                mettre_tuiles_dans_defausse(joueur["mur"][i], defausse)
                ind_couleur_dans_ligne =joueur["mur"][i].index([couleur_ind_zero,False])
                joueur["mur"][i][ind_couleur_dans_ligne][1]=True
                joueur["score"] += obtenir_points(i,ind_couleur_dans_ligne,joueur)
                joueur["motif"][i] = ["" for i in range(len(joueur["motif"][i]))]
    applique_penalite(joueur)


def mettre_tuiles_dans_defausse(ligne, defausse):
    for tuiles in ligne:
        defausse.append(tuiles[0])

def obtenir_points(ligne,colonne, joueur):
    """
    renvoie les points gagnées sur le mur du joueur en plaçant une tuile dans son mur
    dans la ligne et la colonne précisée
    """
    points = 1
    taille_mur = len(joueur["mur"][ligne])
    if colonne < taille_mur-1:
        for i in range(colonne+1,taille_mur):
            if joueur["mur"][ligne][i][1] : # == True
                points+=1
            else:
                break
    if colonne > 0:
        for i in range(colonne-1,-1,-1):
            if joueur["mur"][ligne][i][1] : # == True
                points+=1
            else:
                break
    if ligne > 0:
        for i in range(ligne-1,-1,-1):
            if joueur["mur"][i][colonne][1] : # == True
                points+=1
            else:
                break
    if ligne < taille_mur-1:
        for i in range(ligne+1,taille_mur):
            if joueur["mur"][i][colonne][1] : # == True
                points+=1
            else:
                break
    return points


def score_fin(joueurs):
    """
    calcul du score de fin pour tous les joueurs
    """
    for joueur in joueurs:
        joueur["score"] += 2*nb_ligne_mur_remplie(joueur)+nb_colonne_mur_remplie(joueur)*7+nb_couleur_mur_remplie(joueur)*10

def nb_ligne_mur_remplie(joueur):
    """
    Renvoie le nombre de ligne du mur du joueur remplis
    """
    nb_ligne_remplie = 0
    for ligne in joueur["mur"]:
        if ligne_remplie(ligne) is True:
            nb_ligne_remplie += 1
    return nb_ligne_remplie

def recherche_tuiles_plus_ou_moins_nombreuse(zone, signe):
    tuiles_plus_ou_moins_nombreuse = [None, -15*signe]
    for tuile in zone:
        if zone.count(tuile)*signe > tuiles_plus_ou_moins_nombreuse[1]*signe:
            tuiles_plus_ou_moins_nombreuse = [tuile, zone.count(tuile)]
    return tuiles_plus_ou_moins_nombreuse

def ligne_remplie(ligne):
    for case in ligne:
        if case[1] is False:
            return False
    return True


def nb_colonne_mur_remplie(joueur):
    nb_colonne_remplie = 0
    for colonne in range(len(joueur["mur"])):
        if colonne_remplie(joueur, colonne) is True:
            nb_colonne_remplie += 1
    return nb_colonne_remplie


def colonne_remplie(joueur, colonne):
    for ligne in range(len(joueur["mur"])):
        if joueur["mur"][ligne][colonne][1] is False:
            return False
    return True


def nb_couleur_mur_remplie(joueur):
    nb_case_couleur_remplie = dict()
    for c in l_couleurs:
        nb_case_couleur_remplie[c]=0
    nb_couleur_remplie = 0
    for ligne in joueur["mur"]:
        for case in ligne:
            if case[1] is True:
                nb_case_couleur_remplie[case[0]] += 1
    for couleur in nb_case_couleur_remplie:
        if nb_case_couleur_remplie[couleur] == (len(joueur["mur"][1])):
            nb_couleur_remplie += 1
    return nb_couleur_remplie

def applique_penalite(joueur):
    pena = obtenir_penalite(joueur["plancher"])
    if joueur["score"]+pena <=0:
        joueur["score"] = 0
    else:
        joueur["score"] += pena


def obtenir_penalite(plancher):
    l = ["-1","-1","-2","-2","-2","-3","-3"]
    pena = 0
    for i in range(len(l)):
        if plancher[i] != "":
            pena += int(l[i])
    return pena

def vider_plancher(joueurs):
    for joueur in joueurs:
       joueur["plancher"] = ["" for _ in range(7)]
    efface("plancher")


def partie_fini(joueurs,automat=False):
    if automat: # Règle de fin de partie si c'est un Automate
        for joueur in joueurs:
             if a_3_lignes_pleines_ET_5_tuiles_same_color(joueur):
                 return True
        return False
    else:# Règle de fin de partie classique
        for joueur in joueurs:
            for i in range(len(joueur["mur"])):
                remplie = True
                for case in joueur["mur"][i]:
                    if case[1] == False:
                        remplie = False
                        break
                if remplie:
                    return True
        return False


def gagnants(joueurs):
    gagnant = [joueurs[0]]
    for j in joueurs:
        if j["score"]>gagnant[-1]["score"]:
            gagnant = [j]
        elif j["score"]==gagnant[-1]["score"] and j!=gagnant[-1]:
            gagnant.append(j)
    return gagnant

def a_3_lignes_pleines_ET_5_tuiles_same_color(joueur):
    dico = dict()
    for c in l_couleurs:
        dico[c]=0
    nb_remplie = 0
    for i in range(len(joueur["mur"])):
        l_remplie = True
        for case in joueur["mur"][i]:
            if case[1] == False:
                l_remplie=False
            else:
                dico[case[0]]+=1
        if l_remplie:
            nb_remplie+=1
    return nb_remplie>=3 and list(filter(lambda x : x>=5,dico.values()))

def verif_meilleur_coup(joueur, tuile, meilleur_coup, zone, num_zone, tuile_premier_joueur):
    """
    modifie le meilleurs coup si la tuile que l'on choisit rapporte plus de points
    """
    for ligne in range(len(joueur["mur"])):
        if (joueur["motif"][ligne][0] == "" or  joueur["motif"][ligne][0] == tuile) and [tuile,False] in joueur["mur"][ligne]:
            plancher = list(joueur["plancher"])
            nb_ajout = zone.count(tuile)-(ligne+1)
            for _ in range(nb_ajout):
                plancher.insert(0, tuile)
            if tuile_premier_joueur and num_zone == 10:
                plancher.insert(0, tuile)
            points = obtenir_points(ligne, joueur["mur"][ligne].index([tuile,False]), joueur)+obtenir_penalite(plancher)
            if points > meilleur_coup[0] or (points ==  meilleur_coup[0] and zone.count(tuile) > zone.count(meilleur_coup[2])):
                meilleur_coup = [points, ligne, tuile, num_zone, zone]
    return meilleur_coup


if __name__=="__main__":
    pass
