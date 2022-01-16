"""
Module qui contient toutes les fonctions principales liés à l'affichages du plateau
et ses sous éléments visuels
"""
import os
from upemtk import *
from organisation import *
l_couleurs = ["#D58270", "#9BD570", "#70D5C1", "#707FD5", "#D270D5"]

if "patern_tuiles.txt" in os.listdir():
    with open("patern_tuiles.txt","r") as f:
        l_couleurs = eval(f.readline())
else:
    l_couleurs = ["#D58270", "#9BD570", "#70D5C1", "#707FD5", "#D270D5"]
    
if "config_mur.txt" in os.listdir():
    with open("config_mur.txt","r") as f:
        config_mur = eval(f.readline())
else:
    config_mur = l_couleurs

def creation_grille_connexion():
    """
    Création de la grille "de droite", qui servira à comptabiliser les points
        [ligne1, ligne2...ligne5]
    Chaque ligne est une liste dont chaque element celle-ci est une liste avec 2 éléments : la couleur et un bool
    ex :
        ligne 1 : [["red", False],["cyan", False], ["yellow", False], ["black", False], ["blue", False] ]
        ligne 2 : [["blue", False],["red", False], ["cyan", False], ["yellow", False], ["black", False] ]
        ligne n : ...

    Il faut qu'à chaque ligne il y ait un décalage des couleurs de 1 vers la droite
    """
    resultat = []
    
    for i in range(5):
        lst = []
        for a in range(5):
            lst.append([config_mur[a], False])
        # crer une liste de couple pour chaque couleur
        ancienne_couleur = config_mur[0]
        for i in range(5):
            config_mur[(i+1)%5], ancienne_couleur = ancienne_couleur, config_mur[(i+1)%5]
        # change la couleur de l'element en fonction de l'element precedent pour obtenir le tableau souhaiter
        resultat.append(lst)
    return resultat



def dessin_lignes_motif(joueur):
    '''
    creer le quadrillage lignes motif  au coordonnees x y dans un certains sens
    le sens du quadrillage dépend du joueur:
        joueur de "côté gauche" :  ◿
        joueur de "côté droit" : ◺
    '''

    for i in range(1,6):
        for a in range(i):
            if joueur["sens"] == "gauche":
                dessin_tuile(joueur["motif"][i-1][a], joueur["pos_lignes_motif"][0]-a*25, joueur["pos_lignes_motif"][1]+(i-1)*25, id="tuile")
            else:
                dessin_tuile(joueur["motif"][i-1][a], joueur["pos_lignes_motif"][0]+a*25, joueur["pos_lignes_motif"][1]+(i-1)*25, id="tuile")
        # dessine a case qui vont vers la gauche si c'est la ligne du premier joueur
        # dessine a case qui vont vers la droite si c'est la ligne du deuxième joueur
    # repete les dessin 5 fois


def dessin_mur(joueur):
    """ dessine un tableau de 5 case par 5 case avec un espacement entre eux """
    for i in range(5):
        for a in range(5):
            if joueur["mur"][i][a][1] == False:
                dessin_tuile("", joueur["pos_mur"][0]+a*25, joueur["pos_mur"][1]+i*25,contour=joueur["mur"][i][a][0])
            else:
                dessin_tuile(joueur["mur"][i][a][0], joueur["pos_mur"][0]+a*25, joueur["pos_mur"][1]+i*25,contour=joueur["mur"][i][a][0])


def dessin_tuile(couleur, x, y,contour = "black",id="contour"):
    """dessine une tuile de couleur : couleur aux coordonnées (x,y)"""
    if couleur == "premier_joueur":
        couleur = "white"
    taille_tuile = 20

    rectangle(x,y,x+taille_tuile,y+taille_tuile,couleur=contour,epaisseur=2 ,remplissage=couleur,tag=id)



def dessin_plancher(joueur):
    """Fonction qui dessine le plancher d'un joueur aux coordonnées (x,y)"""
    l = ["-1","-1","-2","-2","-2","-3","-3"]
    for i in range(7):
        texte(joueur["pos_plancher"][0]+i*25-5 + 5,joueur["pos_plancher"][1]-20,l[i], taille=10,police="Copperplate gothic bold")
        dessin_tuile("",joueur["pos_plancher"][0]+i*25,joueur["pos_plancher"][1],id="contour")
        dessin_tuile(joueur["plancher"][i],joueur["pos_plancher"][0]+i*25,joueur["pos_plancher"][1],id="plancher")


def dessin_tuile_fabrique(x,y):
    """Dessine une tuile fabrique avec une superposition de cercles"""
    cercle(x,y,45,remplissage="Brown")
    cercle(x,y,41, remplissage="white",couleur="green")
    cercle(x,y,25, remplissage="brown")
    cercle(x,y,22, remplissage="blue")
    cercle(x,y,20,remplissage="brown")


def dessin_zone_centre(x,y,tuiles_centre):
    """
    Fonction qui déssine la zone centre en prenant en compte la liste
    des tuiles qui la compose (aux coordonnées (x,y))
    """
    max_tuile = 11
    saut_ligne = 0
    rectangle(x-5, y-5, x+25*max_tuile, y+25*4,remplissage="#5D2F25",couleur="#5D2F25")
    for j in range(len(tuiles_centre)):
        indice = j%max_tuile
        if indice == 0 and j != 0:
            saut_ligne+=1
        dessin_tuile(tuiles_centre[max_tuile*saut_ligne+indice], x+25*indice, y+25*saut_ligne,id="tuile")


def dessin_tuiles_dans_fabrique(fabrique):
    """
    Prend en argument une fabrique donc un DICTIONNAIRE et
    dessiner les tuiles contenues dans la fabrique
    """
    taille_tuile = 20
    x,y = fabrique["pos"] #Coordonnées du centre de la fabrique
    gap = 30 #espacement avec le centre de la fabrique
    #Liste des coord (x,y) des coints inferieurs gauche des 4 tuiles
    coord_tuiles = [(x-gap , y-gap) , (x+gap-taille_tuile , y-gap) , (x-gap , y+gap-taille_tuile) , (x+gap-taille_tuile , y+gap-taille_tuile)]
    if fabrique["tuiles"] != []:
        for i in range(len(coord_tuiles)):
            dessin_tuile(fabrique["tuiles"][i] , coord_tuiles[i][0] ,coord_tuiles[i][1],id="tuile")


def dessin_fabriques(fabriques):
    """Fonction qui dessines les fabriques et appelle dessin_tuiles_dans_fabrique()
    pour déssiner aussi les tuiles qui les composent
    """
    for fab in fabriques:
        dessin_tuile_fabrique(fab["pos"][0], fab["pos"][1])
    #On met une séparation pour éviter les superposition au niveau du dessin
    for fab in fabriques:
        dessin_tuiles_dans_fabrique(fab)


def dessin_gagnants(gagnants):
    rectangle(0,0,3000,3000,remplissage="#5D2F25")
    texte(200,200,"VICTOIRE !",couleur="Black",taille=64,police="Copperplate gothic bold")
    texte(202,198,"VICTOIRE !",couleur="Orange",taille=64,police="Copperplate gothic bold")
    for i in range(len(gagnants)):
        texte(400,400 + (i+1)*35," -> "+gagnants[i]["nom"],couleur="Orange",taille=30,police="Copperplate gothic bold")
    print("--------------------------------------------------------------------")
    print("Voici les gagnants : ")
    for g in gagnants:
        print("-> ",g["nom"])
        

def dessin_plateau_joueurs(joueurs):
    """
    Fonction qui déssine le plateau d'un joueur donné en argument.
    Cette fonction utilises toutes les fonctions auxiliaires de dessins liéés
    au joueurs créées jusqu'à maintenant
    """
    for j in joueurs:
        texte(j["pos_plateau"][0],j["pos_plateau"][1]-75,j["nom"],taille=41,couleur="Black",police="Copperplate gothic bold")
        texte(j["pos_plateau"][0],j["pos_plateau"][1]-75,j["nom"],taille=40,couleur="Orange",police="Copperplate gothic bold")

        texte(j["pos_score"][0],j["pos_score"][1],"Score "+str(j["score"]),couleur="Pink", taille=20, tag="score",police="Copperplate gothic bold")
        dessin_mur(j)
        dessin_lignes_motif(j)
        dessin_plancher(j)

if __name__ == "__main__":
    ...

