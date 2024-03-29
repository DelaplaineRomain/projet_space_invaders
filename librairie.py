# -*- coding : utf-8 -*-

# Header
"""
objectif : librairie pour le jeu space invaders
Fait par Gouchon Léo et Delaplaine Romain
Date de dernière modification : 17/01/2021
To do : rien
"""

# creation de la classe vaisseau
"""attribut : position , vitesse, vie"""

import tkinter

class Vaisseau() :
    def __init__(self,pType,pVitesse,pVie = 1,pPosition = [0,0]):
        self.__vie = pVie
        self.__vitesse = pVitesse
        self.__position = pPosition
        self.__type = pType

    def set_vie (self,pVie):
        self.__vie = pVie

    def set_vitesse (self,pVitesse):
        self.__vitesse = pVitesse

    def set_position (self,pPosition):
        self.__position = pPosition

    def set_type (self,pType):
        self.__type = pType

    def get_position(self):
        return self.__position[:]

    def get_vie(self):
        return self.__vie

    def get_type(self):
        return self.__type

    def deplacement_droite(self):
        if self.__position[0] < 980 :
            self.__position[0] += 10

    def deplacement_gauche(self):
        if self.__position[0] >= 10 :
            self.__position[0] -= 10

    def deplacement_bas(self):
        if self.__position[1] < 690 :
            self.__position[1] += 10

    def deplacement_haut(self):
        if self.__position[1] > 10 :
            self.__position[1] -= 10

class shoot():
    def __init__(self,pPosition,pAuteur,pType):     # Un shoot auras toujours le type 5
        self.__position_ball = pPosition
        self.__auteur = pAuteur
        self.__type = pType

    def get_position(self):
        return self.__position_ball[:]

    def get_auteur(self):
        return self.__auteur

    def get_type(self):
        return self.__type

    def deplacement_bas_shoot(self):
        if self.__position_ball[1] <= 690 :
            self.__position_ball[1] += 3

    def deplacement_haut_shoot(self):
        if self.__position_ball[1] >= 10 :
            self.__position_ball[1] -= 3

class brique():
    def __init__(self,pPosition,pType):             # Une brique auras toujours le type 6
        self.__position = pPosition
        self.__type = pType
    
    def get_position(self):
        return self.__position[:]

    def get_type(self):
        return self.__type
