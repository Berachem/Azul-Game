# 🕹️ Jeu de plateau avec une IA 🤖 : Azul
 Jeu Azul en Python avec une IA implémentées, jouable de 1 à 4 joueurs

Par :  **Berachem MARKRIA** et **Tristan MARTINEZ** <br>
Projet réalisé grâce à  : **Carine PIVOTEAU**, **Anthony LABARRE** et **Camille COMBE**  (nous les remercions tous les 3 🙂)<br>
Nous avons implementés le jeu de plateau [Azul](https://www.fnac.com/Jeu-de-strategie-Asmodee-Azul/a14232820/w-4/) en Python.

Ce projet a débuté en Octobre 2021 et s'est terminé en début Janvier 2022. Soit une durée d'environ 3 mois.
Il a pu avoir lieu grâce à nos enseignants de l'Université Gustave Eiffel (anciennement Paris-Est, Marne-la-Vallée).

<h1>🪄 Implémentation</h1>

Création de 4 IAs différentes et un semblant d'Automat. Pour satisfaire tous les types de joueurs ;)
On pourra choisir le type des IAs qu'on souhaite affronter après avoir choisi un mode de jeu contenant au moins une IA.

Possibilité de changer le patern des tuiles dans la partie en écrivant dans un fichier `patern_tuiles.txt` la liste des couleurs que l'on souhaite
Possibilité de changer l'ordre des couleurs dans les murs en écrivant dans un fichier `config_mur.txt` l'ordre des couleurs (en liste)


### IA "difficile"

elle cherche la meilleurs option dans les tuiles proposer c'est à dire celle
qui va lui donné le meilleur score sur le coup
meilleur_coup enregistre le score, la ligne, la couleur de la tuile
le numéro de la fabrique et si elle se trouve dans une fabrique ou dans la
zone du centre (si c'est la zone du centre alors le numéro de fabrique sera 10)
 
### IA "long"
elle choisira le maximum de tuiles possibles et les placera le plus bas possible dans sa ligne motif

### IA "facile"
elle mettra les tuiles de manière aléatoire

### IA "rapide"
elle prendra le moins de tuiles possible et les placera le plus haut possible dans sa ligne motif

### ~~Automat

Il s'agit d'une IA un peu différente qui commence constamment, son plancher n'est jamais remplie, il n'y a pas de calcul de 
points final en fin de partie néanmoins le calcul des point à chaque tour reste effectif; la partie s'arrête quand un joueur 
a au moins 3 lignes pleines ET 5 tuiles de la même couleur.



<h1>💻 Tester le Code</h1>

Voici ce que cela donne lorsque qu'on lance le fichier `menu.py`
```py
python3 menu.py
```
On a implémenté un menu où l'on peut choisir parmis quelques modes de jeu proposés :

![Menu](https://i.postimg.cc/JMt8ZBhk/screen-menu.png)

Voici un exemple lorsqu'on lance le mode jeu *Regarder* : 

![Game](https://i.postimg.cc/syTyMJ3z/screen-partie.png)

Merci d'avoir feuilleté notre projet, ça nous fait chaud au ❤️ !
