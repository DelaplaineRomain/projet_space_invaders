# -*- coding : utf-8 -*-

# Header
"""
objectif : créer le jeu space invaders 
Fait par Gouchon Léo et Delaplaine Romain
Date de dernière modification : 18/12/2020
To do : 
"""

#### les imports

import tkinter
from time import sleep

import librairie as lib
#### classe interface

class Interface_game ():
    def __init__ (self):
        # creation des outils tkinter

        """creation de la fenetre"""
        self.mywindow = tkinter.Tk()
        self.mywindow.title('Space invaders')
        self.mywindow['bg'] = 'grey'

        """section pour le score et la vie"""
        self.frame1 = tkinter.Frame(self.mywindow , bg = 'grey')
        self.frame1.grid(row = 1 , column = 1 , columnspan = 20 , padx = 10 , pady = 10)

        tkinter.Label(self.frame1, text = 'Score :' , bg = 'grey').grid(row = 1 , column = 1 , padx = 10 , pady = 10 , sticky = 'W')
        self.score = tkinter.StringVar()
        tkinter.Label(self.frame1 , textvariable = self.score).grid(row = 1 , column = 2 , padx = 10 , pady = 10 , sticky = 'W')

        tkinter.Label(self.frame1, text = 'Life :' , bg = 'grey').grid(row = 1 , column = 3 , padx = 10 , pady = 10 , sticky = 'E')
        self.vie = tkinter.StringVar()
        tkinter.Label(self.frame1 , textvariable = self.vie).grid(row = 1 , column = 4 , padx = 10 , pady = 10 , sticky = 'E')

        """section pour le canvas"""
        self.frame2 = tkinter.Frame(self.mywindow , bg = 'grey')
        self.frame2.grid(row = 2 , column = 1 , rowspan = 15 , columnspan = 20 , padx = 10 , pady = 10)
        self.Largeur = 700
        self.Hauteur = 700
        self.canevas = tkinter.Canvas(self.frame2, width = self.Largeur , height = self.Hauteur, bg = 'black' )
        self.canevas.grid(padx = 10 , pady = 10)

        """"section pour les boutons quiter et lancer"""
        self.frame3 = tkinter.Frame(self.mywindow , bg = 'grey')
        self.frame3.grid(row = 1 , column = 21 , rowspan = 16 , columnspan = 5 , padx = 10 , pady = 10)
        self.bouton_lancer = tkinter.Button(self.frame3 , text = 'Start' , command = self.Vaisseau_alien)
        self.bouton_lancer.grid(row = 1 , column = 1, padx = 10 , pady = 10)
        self.bouton_quitter = tkinter.Button(self.frame3 , text = 'Exit')
        self.bouton_quitter.grid(row = 2 , column = 1, padx = 10 , pady = 10)

        """lancement de la fenetre"""

        self.mywindow.mainloop()

    def Vaisseau_alien(self):
        """
        génère une ligne de 5 vaisseau_alien
        """
        global vaisseau_alien
        global vaisseau_alien_gui      
        global dx
        global dy
        global position_x
        global position_y
        global coord_all_alien
        dx = 40
        dy = 40
        coord_all_alien = [] #coordonné de toutes les lignes des aliens : [[ligne 1],[ligne 2],[ligne 3]]
        #On créé 5 vaisseaux à la suite sur une même ligne 3 fois
        for ligne in range(3):
            coord_ligne_alien = [] #Liste vide qui sera remplie par les vaisseaux d'une même ligne
            for colonne in range(5):
                vaisseau_alien = lib.Vaisseau_alien(1,1,[20+100*colonne,20+100*ligne])
                position_x = vaisseau_alien.get_position()[0]
                position_y = vaisseau_alien.get_position()[1]
                vaisseau_alien_gui = self.canevas.create_rectangle(position_x-10, position_y-10, position_x+10, position_y+10, fill='blue')
                coord_ligne_alien.append([vaisseau_alien, vaisseau_alien_gui])
            coord_all_alien.append(coord_ligne_alien)
        self.deplacement_alien()    

    def deplacement_alien(self):  
        """
        déplacement automatique les aliens
        le vaisseau bouge toujours en premier vers la droite
        S'il atteint le bord droit, il bougera alors vers la gauche
        S'il atteint le bord gauche, il descend d'un cran vers le bas
        """
        global vaisseau_alien
        global vaisseau_alien_gui
        global dx
        global dy
        global coord_all_alien
        
        if coord_all_alien[-1][-1][0].get_position()[0]+10+dx > 700 : #On prend l'alien le plus en bas à droite de l'écran
            dx = -dx
            print ("gauche")
        if coord_all_alien[-1][0][0].get_position()[0]-10+dx < 0 : #l'alien qui est le plus en bas à gauche de l'écran
            dx = -dx
        
            for ligne in coord_all_alien:
                for vaisseau in ligne:
                   vaisseau[0].get_position()[1] += dy
            print("droite")
        for ligne in coord_all_alien:
                for vaisseau in ligne:   
                    vaisseau[0].get_position()[0] += dx
                    self.canevas.coords(vaisseau[1],vaisseau[0].get_position()[0]-10,vaisseau[0].get_position()[1]-10,vaisseau[0].get_position()[0]+10,vaisseau[0].get_position()[1]+10)
        if coord_all_alien[-1][0][0].get_position()[1] < 500 : 
            self.mywindow.after(200,self.deplacement_alien)
        else : #Si les aliens les plus en bas sont sur la même ligne que le vaisseau
            self.fin_partie()
        
    def fin_partie(self):
        """
        Affiche un message de game over
        Pour l'instant sur la console
        """
        print("game over")
        return

        