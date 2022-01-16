
import os
from random import randrange
from organisation import *
from plateau import *
from menu import *
from upemtk import *


def partie(nb_joueurs, bot, mode_bot, reprendre_partie=None,automat=False):
    """
    Fonction principale regroupant les appels des moments fondamentaux
    pour la parte Azul
    """
    hauteur_partie, largeur_partie = 600,1025
    cree_fenetre(largeur_partie,hauteur_partie)
    rectangle(0,0,largeur_partie,hauteur_partie,remplissage="#5D2F25")
    texte(10,5,"sauvegarde en cours ✔",couleur="green",taille=10)
    joueurs,fabriques,sac,defausse,bot,nb_joueurs, mode_bot = init(reprendre_partie, nb_joueurs, bot, mode_bot)
    print("Le sac est actuellement de taille :", len(sac))

    while not partie_fini(joueurs):
        dessin_plateau_joueurs(joueurs)
        dessin_fabriques(fabriques)
        quitter = offre_de_fabriques(fabriques, joueurs, bot, mode_bot,automat=automat)
        if quitter:
            ferme_fenetre()
            return
        decoration_mur(joueurs, defausse)
        fabriques = creer_fabrique_tuiles(nb_joueurs,sac, defausse)
        creer_sauvegarde(sac.extend(defausse),joueurs,fabriques, defausse, bot, mode_bot)

    #--FIN DE PARTIE--
    if partie_fini(joueurs):
        score_fin(joueurs) #Recalcule des points à la fin de la partie
        supprimer_sauvegarde()
        efface_tout()
        vainqueurs = gagnants(joueurs)
        dessin_gagnants(vainqueurs)
        _,x,y=attente_clic_ou_touche()

    ferme_fenetre()

def menu():
    """
    Crée la fenêtre qui permettra au joueur de choisir son mode de jeu et si il choisit un mode avec IA, de choisir
    la difficulté de celle(s)-ci
    """

    hauteur_menu, largeur_menu = 720,450
    hauteur_boutton = hauteur_menu/18
    largeur_boutton = 3*largeur_menu/8

    pos_bouttons = [(40,hauteur_menu/2-50),(largeur_menu/2 +30,hauteur_menu/2-50),(40,hauteur_menu/2 +30),(largeur_menu/2 +30,hauteur_menu/2 +30),(40,hauteur_menu/2 +140),(largeur_menu/2 +30,hauteur_menu/2 +140),(40, hauteur_menu-130),(largeur_menu/2 +30, hauteur_menu-30),(40, hauteur_menu-30),(largeur_menu/2-largeur_boutton/2, 170)]
    nom_buttons = ["1vIA","1vIAvIA","1vIAvIAvIA","1vAutomat","1v1","1v1v1","1v1v1v1","continuer","Regarder","Quitter"]

    pos_bouttons_ia = [(40,hauteur_menu/2-50),(largeur_menu/2 +30,hauteur_menu/2-50),(40,hauteur_menu/2 +30),(largeur_menu/2 +30,hauteur_menu/2 +30),(largeur_menu/2-largeur_boutton/2, 170)]
    nom_buttons_ia = ["facile", "rapide", "longue", "difficile", "Quitter"]
    cree_fenetre(largeur_menu,hauteur_menu)
    rectangle(0,0,largeur_menu,hauteur_menu, remplissage="#5D2F25")
    texte(80,10,"By Berachem MARKRIA and Tristan MARTINEZ :)", couleur="White", taille=8)
    creer_boutons(pos_bouttons, nom_buttons, largeur_boutton, hauteur_boutton, hauteur_menu, largeur_menu)
    texte(pos_bouttons[0][0]-25,pos_bouttons[0][1]-80,"1 Joueur",taille=15,couleur="Orange",police="Copperplate gothic bold")
    texte(pos_bouttons[4][0]-25,pos_bouttons[4][1]-75,"2 à 4 Joueurs",taille=15,couleur="Orange",police="Copperplate gothic bold")
    choix =  choix_mode_jeu(pos_bouttons, nom_buttons, largeur_boutton, hauteur_boutton, hauteur_menu, largeur_menu)
    choix_ia = "pas encore"
    if choix == "continuer":
        if os.path.isfile("recap_partie.txt"):
            ferme_fenetre()
            partie(None, None, None, True)
    elif choix and "IA" in choix or choix == "Regarder":
        rectangle(0,0,largeur_menu,hauteur_menu, remplissage="#5D2F25")
        texte(80,10,"By Berachem MARKRIA and Tristan MARTINEZ :)", couleur="White", taille=8)
        creer_boutons(pos_bouttons_ia, nom_buttons_ia, largeur_boutton, hauteur_boutton, hauteur_menu, largeur_menu)
        choix_ia = choix_mode_jeu(pos_bouttons_ia, nom_buttons_ia, largeur_boutton, hauteur_boutton, hauteur_menu, largeur_menu)
    ferme_fenetre()
    if not choix_ia or choix == "Quitter" or choix_ia == "Quitter":
        pass
    elif choix == "1v1":
        partie(2, [False, False], choix_ia)
    elif choix == "1vIA":
        partie(2, [False, True], choix_ia)
    elif choix == "1vIAvIAvIA":
        partie(4, [False, True, True,True], choix_ia)
    elif choix == "1vIAvIA":
        partie(3,[False, True, True], choix_ia)
    elif choix == "Regarder":
        partie(4, [True, True, True,True], choix_ia)
    elif choix == "1v1v1v1":
        partie(4, [False, False, False, False], choix_ia)
    elif choix == "1v1v1":
        partie(3,[False, False, False], choix_ia)
    elif choix =="1vAutomat":
        partie(2, ["Automat", False],"difficile",automat=True)
    else:
        menu()


def choix_mode_jeu(pos_bouttons, nom_buttons, largeur_boutton, hauteur_boutton, hauteur_menu, largeur_menu):
    """Fonction qui renvoie le mode de jeu choii par l'utilisateur selon le clique"""
    while True:
        x,y,touche = attente_clic_ou_touche()
        if touche == 'Touche':
            if y == 'Escape':
                return False
        print(f'Il y a eu un clic en ({x}, {y}).')
        for i in range(len(nom_buttons)):
            if pos_bouttons[i][0]-20<= x <= pos_bouttons[i][0]+largeur_boutton and pos_bouttons[i][1]-hauteur_boutton<= y <= pos_bouttons[i][1]+20:
                return nom_buttons[i]


def init(reprendre_partie, nb_joueurs, bot, mode_bot):
    """
    initialose les varible principale e fonction de si on reprend une
    sauvegarde ou si on joue une autre partie
    """
    if reprendre_partie:
        joueurs,fabriques,sac,defausse,bot,mode_bot = charger_sauvegarde("recap_partie.txt")
        nb_joueurs = len(joueurs)
    else:

        sac = creer_sac_tuile()
        joueurs = creation_joueurs(nb_joueurs,bot)
        defausse = []
        fabriques = creer_fabrique_tuiles(nb_joueurs,sac, defausse)
    return joueurs,fabriques,sac,defausse,bot,nb_joueurs,mode_bot


def creer_boutons(pos_bouttons, nom_buttons, largeur_boutton, hauteur_boutton, hauteur_menu, largeur_menu):
    """ affiche le menu avec les boutons pour le choix du mode de jeu """
    l_couleurs_titre = ["#D58270", "#9BD570", "#70D5C1", "#707FD5"]
    l_couleurs = ["#D58270", "#D58270", "#D58270", "#D58270", "#9BD570","#70D5C1","#D270D5", "red", "red", "red"]
    expr = "AZUL"
    for i in range(len(expr)):
        texte(largeur_menu/4+i*60 , 30, expr[i], couleur = l_couleurs_titre[i] , taille=50,police="Copperplate gothic bold")

    for i in range(len(nom_buttons)):
            rectangle(pos_bouttons[i][0]-20,pos_bouttons[i][1]+20, pos_bouttons[i][0]+largeur_boutton   ,pos_bouttons[i][1]-hauteur_boutton,couleur=l_couleurs[i%len(l_couleurs)],epaisseur=5)
            texte(pos_bouttons[i][0]+10,pos_bouttons[i][1]-30, nom_buttons[i], couleur="White",taille=16,police="Copperplate gothic bold")

def creer_sauvegarde(sac,joueurs,fabriques, defausse, bot, mode_bot):
    """
    Création un fichier de la forme:

    Joueurs :
    [ LISTE CONCERNANT LES JOUEURS ]
    Fabriques :
    [ LISTE CONCERNANT LES FABRIQUES ]
    Sac :
    [ LISTE CONCERNANT LE SAC ]
    Defausse :
    [ LISTE CONCERNANT LA DEFAUSSE ]
    Bot :
    [ LISTE CONCERNANT QUELS JOUEURS SONT DES BOTS ]
    """
    with open("recap_partie.txt","w") as f:

        f.write("Joueurs :\n")
        f.write(str(joueurs)+"\n")
        f.write("Fabriques :\n")
        f.write(str(fabriques)+"\n")
        f.write("Sac :\n")
        f.write(str(sac)+"\n")
        f.write("Defausse :\n")
        f.write(str(defausse)+"\n")
        f.write("Bot :\n")
        f.write(str(bot)+"\n")
        f.write("Mode bot :\n")
        f.write(str(mode_bot)+"\n")


def charger_sauvegarde(fichier):
    """
    Permet de charger les données enregistrées dans un fichier donné et renvoie une liste contenant
    toutes ces données
    """
    with open(fichier,"r") as f:
        l_attributs = list()
        contenu = f.readlines()
        l_attributs.append(eval(contenu[1][:-1]))
        l_attributs.append(eval(contenu[3][:-1]))
        l_attributs.append(eval(contenu[5][:-1]))
        l_attributs.append(eval(contenu[7][:-1]))
        l_attributs.append(eval(contenu[9][:-1]))
        l_attributs.append(contenu[11][:-1])
        for i in range(len(l_attributs)):
            if l_attributs[i] ==None:
                         l_attributs[i]=list()
        return l_attributs

def supprimer_sauvegarde():
    """
    Fonction qui supprime le fichier de sauvegarde
    """
    if "recap_partie.txt" in os.listdir():
        os.remove("recap_partie.txt")

if __name__ == "__main__":
    menu()

