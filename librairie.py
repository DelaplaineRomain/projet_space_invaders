# -*- coding : utf-8 -*-

# Header
"""
objectif : librairie pour le jeu space invaders
Fait par Gouchon Léo et Delaplaine Romain
Date de dernière modification : 18/12/2020
To do : tout
"""

# creation de la classe vaisseau
"""attribut : position , vitesse, vie"""

class Vaisseau() :
    def __init__(self,pVitesse,pVie = 1,pPosition = [0,0]):
        self.__vie = pVie
        self.__vitesse = pVitesse
        self.__position = pPosition

    def set_position(self, pPosition):
        self.__position = pPosition

    def get_position(self):
        return self.__position

    def get_vie(self):
        return self.__vie

    def deplacement_droite(self, canevas):
        if self.__position[0] < 980 :
            self.__position[0] += 10

    def deplacement_gauche(self, canevas):
        if self.__position[0] > 10 :
            self.__position[0] -= 10

    def deplacement_bas(self):
        if self.__position[1] < 690 :
            self.__position[1] += 10

    def deplacement_haut(self):
        if self.__position[1] > 10 :
            self.__position[1] -= 10

class Vaisseau_joueur(Vaisseau):
    def __init__(self,pName = "player"):
        self.__player = pName

class Vaisseau_alien(Vaisseau):
    def blabla(self):
        return "je suis trop fort"



