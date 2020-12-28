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
        génère un vaisseau_alien
        """
        global vaisseau_alien
        global vaisseau_alien_gui      #modif
        global dx
        global dy
        global position_x
        global position_y
        dx = 20
        dy = 0
        vaisseau_alien = lib.Vaisseau_alien(2121,2121,[10,200])
        position_x = vaisseau_alien.get_position()[0]
        position_y = vaisseau_alien.get_position()[1]
        vaisseau_alien_gui = self.canevas.create_rectangle(position_x-10, position_y-10, position_x+10, position_y+10, fill='blue')
        self.deplacement_alien()    #modif

    def deplacement_alien(self):  #modif
        """
        déplacement automatique des aliens
        le vaisseau bouge toujours vers la droite
        S'il atteint le bord droit, il bougera alors vers la gauche
        """
        # print("fonction deplacement_alien")
        # self.canevas.move(vaisseau_alien_gui, 20, 0)
        # while vaisseau_alien.deplacement_droite() == True:
        #     print("déplace vers la droite")
        #     position_x = vaisseau_alien.get_position()[0]
        #     position_y = vaisseau_alien.get_position()[1]
        #     print(position_x)      
        #     self.canevas.coords(vaisseau_alien_gui, position_x-10, position_y-10, position_x+10, position_y+10)
    
        # while vaisseau_alien.deplacement_gauche() == True:
        #     print("déplace vers l gauche")
        #     vaisseau_alien.deplacement_gauche()
        #     position_x = vaisseau_alien.get_position()[0]
        #     position_y = vaisseau_alien.get_position()[1]
        #     print(position_x)    
        #     self.canevas.coords(vaisseau_alien_gui, position_x-10, position_y-10, position_x+10, position_y+10)
        global vaisseau_alien
        global vaisseau_alien_gui
        global dx
        global dy
        global position_x
        global position_y
        if position_x+10+dx > 700 :
            dx = -dx
            print ("gauche")
        if position_x-10+dx < 0 :
            dx = -dx
            print("droit")
        position_x = position_x + dx
        position_y = position_y + dy
        print("position_x : ",position_x)
        self.canevas.coords(vaisseau_alien_gui,position_x-10,position_y-10,position_x+10,position_y+10)
        self.mywindow.after(200,self.deplacement_alien)
    