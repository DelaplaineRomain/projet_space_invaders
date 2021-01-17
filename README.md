# projet_space_invaders
jeu space invaders 

# Objectif: 
recréer le jeu space invaders

# Fonctionnement du jeu :

Le programme à éxécuter est main.py

Lorsque la fenêtre s'ouvre, on peut lancer une partie en appuyant sur 'Start' , on peut arrêter la partie en appuyant sur 'Stop' et ainsi relancer une partie. Le bouton 'Exit' fermera la fenêtre.

# Première piste de travail (ce dont on aura besoin, à affiner par la suite) :

-programer en orienté objet
    -classe vaisseau   
        position x,y
        vitesse
        vie
        -sous classe joueur
            attribut de joueur
        -sous classe alien
            attribut d'alien
            -sous classe type d'alien
                type d'alien
            
    -classe ilot
        position
        vie

    -classe balle
        position initial
        auteur

-fonction qui créer la grille de jeu

-fonction qui gère le deplacement du joueur (droite, gauche)

-fonction qui gère le déplacement automatiques des vaisseaux aliens

-fonction qui gère les tirs (déplacement de la balle)
    parametre : position initiale et l'auteur du tir

-fonction qui regarde si un tir touche un vaisseau

-fonction qui regarde si la partie est finis (victoire ou defaite)

-fonction qui lance la partie 

-fonction qui arrête la partie

-fonction qui quitte le programme proprement

-fonction qui calcule le score en cours

-fonction qui enregistre le score de la dernière partie et la meilleur score (fichier texte)

