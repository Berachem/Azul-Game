# 🕹️ Jeu de plateau avec une IA 🤖 : Azul
 Jeu Azul en Python avec une IA implémentées, jouable de 1 à 4 joueurs


<video width="740" height="480" controls>
  <source src="https://igadvisory.fr/opendata/azul_demo.mp4" type="video/mp4">
</video>

https://user-images.githubusercontent.com/61350744/169663102-18e8eef0-efd1-486c-a09f-67baa2d1b9f7.mp4


Par :  **Berachem MARKRIA** et **Tristan MARTINEZ** <br>
Projet réalisé grâce à  : **Carine PIVOTEAU**, **Anthony LABARRE** et **Camille COMBE**  (nous les remercions tous les 3 🙂)<br>
Nous avons implementés le jeu de plateau [Azul](https://www.fnac.com/Jeu-de-strategie-Asmodee-Azul/a14232820/w-4/) en Python.

Ce projet a débuté en Octobre 2021 et s'est terminé en début Janvier 2022. Soit une durée d'environ 3 mois.
Il a pu avoir lieu grâce à nos enseignants de l'Université Gustave Eiffel (anciennement Paris-Est, Marne-la-Vallée).

<h1>🪄 Implémentation</h1>

Mise en place de 4 IAs distinctes et d'une simulation automatisée. Pour satisfaire toutes les catégories de joueurs ;)
Vous pouvez choisir le type d'IAs que vous souhaitez affronter après avoir sélectionné un mode de jeu incluant au moins une IA.

La possibilité de personnaliser le motif des tuiles dans le jeu en éditant le fichier `patern_tuiles.txt` avec la liste des couleurs souhaitées.
De même, vous pouvez ajuster l'ordre des couleurs dans les murs en modifiant le fichier `config_mur.txt` avec l'ordre désiré (sous forme de liste).


### IA "difficile" 💪

> Cette IA cherche la meilleure option parmi les tuiles proposées, c'est-à-dire celle qui maximisera son score immédiatement. 
L'attribut "meilleur_coup" enregistre le score, la ligne, la couleur de la tuile, le numéro de la fabrique, et si elle se trouve dans une fabrique ou dans la zone centrale (le numéro de la fabrique sera 10 pour la zone centrale).

### IA "long" 🕰️

> Elle choisira le maximum de tuiles possible et les placera le plus bas possible dans sa ligne motif.

### IA "facile" 🎲

> Cette IA dispose les tuiles de manière aléatoire.

### IA "rapide" 🚄💨

> Elle prendra le moins de tuiles possible et les placera le plus haut possible dans sa ligne motif.

### ~~Automat

> Il s'agit d'une IA un peu différente qui commence constamment, son plancher n'est jamais rempli, et il n'y a pas de calcul de points finaux en fin de partie. Néanmoins, le calcul des points à chaque tour reste effectif ; la partie s'arrête quand un joueur a au moins 3 lignes pleines ET 5 tuiles de la même couleur.


<h1>💻 Tester le Code</h1>

Voici ce que cela donne lorsque qu'on lance le fichier `menu.py`
```py
python menu.py
```





Merci d'avoir feuilleté notre projet, ça nous fait chaud au ❤️ !
