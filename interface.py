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
import librairie as lib
from random import randint 

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
        self.Largeur = 1000
        self.Hauteur = 700
        self.canevas = tkinter.Canvas(self.frame2, width = self.Largeur , height = self.Hauteur, bg = 'black' )
        self.canevas.focus_set()
        self.canevas.bind('<Key>',self.gestion_keyEvent)
        # self.canevas.bind('<Key>',self.deplacement_joueur)
        # self.canevas.bind('<KeyPress-space>',self.tir_joueur)
        self.canevas.grid(padx = 10 , pady = 10)

        """"section pour les boutons quiter et lancer"""
        self.frame3 = tkinter.Frame(self.mywindow , bg = 'grey')
        self.frame3.grid(row = 1 , column = 21 , rowspan = 16 , columnspan = 5 , padx = 10 , pady = 10)
        self.bouton_lancer = tkinter.Button(self.frame3 , text = 'Start' , command = self.game_start)
        self.bouton_lancer.grid(row = 1 , column = 1, padx = 10 , pady = 10)
        self.bouton_quitter = tkinter.Button(self.frame3 , text = 'Exit')
        self.bouton_quitter.grid(row = 2 , column = 1, padx = 10 , pady = 10)

        """lancement de la fenetre"""

        self.mywindow.mainloop()

    def game_start(self):
        global liste_shoot
        liste_shoot = []
        self.vaisseau_joueur()
        self.create_wall()
        self.Vaisseau_alien()
        

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
                vaisseau_alien = lib.Vaisseau(1,20,1,[20+100*colonne,20+100*ligne])
                position_x = vaisseau_alien.get_position()[0]
                position_y = vaisseau_alien.get_position()[1]
                vaisseau_alien_gui = self.canevas.create_rectangle(position_x-25, position_y-25, position_x+25, position_y+25, fill = "blue")
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
        if coord_all_alien[-1][-1][0].get_position()[0]+10+dx > 1000 : #On prend l'alien le plus en bas à droite de l'écran
            dx = -dx
        if coord_all_alien[-1][0][0].get_position()[0]-10+dx < 0 : #l'alien qui est le plus en bas à gauche de l'écran
            dx = -dx
        
            for ligne in coord_all_alien:
                for vaisseau in ligne:
                   vaisseau[0].set_position([vaisseau[0].get_position()[0],vaisseau[0].get_position()[1]+dy])
        for ligne in coord_all_alien:
                for vaisseau in ligne:
                    vaisseau[0].set_position([vaisseau[0].get_position()[0] + dx,vaisseau[0].get_position()[1]])
                    self.canevas.coords(vaisseau[1],vaisseau[0].get_position()[0]-25,vaisseau[0].get_position()[1]-25,vaisseau[0].get_position()[0]+25,vaisseau[0].get_position()[1]+25)
        if coord_all_alien[-1][0][0].get_position()[1] < 640 : 
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

    def vaisseau_joueur(self):
        global mon_vaisseau
        global mon_vaisseau_gui
        mon_vaisseau = lib.Vaisseau(0,20,3,[100,640])
        position_x = mon_vaisseau.get_position()[0]
        position_y = mon_vaisseau.get_position()[1]
        mon_vaisseau_gui = self.canevas.create_rectangle(position_x , position_y , position_x+20 , position_y+20 , fill = 'white')
    
    def deplacement_joueur(self,pTouche):
        global mon_vaisseau
        global mon_vaisseau_gui
        touche = pTouche
        # touche = event.keysym
        if touche == 'q' or touche == 'Left':
            mon_vaisseau.deplacement_gauche()
        if touche == 'd' or touche == 'Right':
            mon_vaisseau.deplacement_droite()
        position_x = mon_vaisseau.get_position()[0]
        position_y = mon_vaisseau.get_position()[1]
        self.canevas.coords(mon_vaisseau_gui , position_x , position_y , position_x+20 , position_y+20)

    def create_ball(self, pPosition , pAuteur):
        global ball
        global ball_gui
        global liste_shoot
        ball = lib.shoot(pPosition , pAuteur)
        position_x_ball = ball.get_position()[0]
        position_y_ball = ball.get_position()[1]
        ball_gui = self.canevas.create_oval(position_x_ball , position_y_ball , position_x_ball+10 , position_y_ball+10, fill = 'red')
        liste_shoot.append([ball,ball_gui])
        # self.deplacement_ball()
        self.deplacement_shoot()

    def deplacement_shoot(self):
        global liste_shoot
        for val in liste_shoot:
            projectile = val[0]
            projectile_gui = val[1]
            if projectile.get_auteur() == 0 :
                projectile.deplacement_haut_shoot()
                position_x = projectile.get_position()[0]
                position_y = projectile.get_position()[1]
            elif projectile.get_auteur() == 1 :
                projectile.deplacement_bas_shoot()
                position_x = projectile.get_position()[0]
                position_y = projectile.get_position()[1]
            self.canevas.coords(projectile_gui , position_x , position_y , position_x+10 , position_y+10)
            if position_y == 0 :
                self.canevas.delete(projectile_gui)
        self.mywindow.after(500,self.deplacement_shoot)

    def deplacement_ball(self):
        global ball
        global ball_gui
        ball.deplacement_haut_shoot()
        position_x_ball = ball.get_position()[0]
        position_y_ball = ball.get_position()[1]
        self.canevas.coords(ball_gui , position_x_ball , position_y_ball , position_x_ball+10 , position_y_ball+10)
        self.mywindow.after(500,self.deplacement_ball)

    def tir_joueur(self):
        global mon_vaisseau
        position_initial = mon_vaisseau.get_position()
        type_initial = mon_vaisseau.get_type()
        self.create_ball(position_initial,type_initial)
        
    def gestion_keyEvent(self,event):
        touche = event.keysym
        liste = ['q','d','Right','Left']
        if touche in liste :
            self.deplacement_joueur(touche)
        if touche == 'space' :
            self.tir_joueur()

    def create_wall(self):
        """
        Fonction qui créé un mur de brique (3 briques de hauteurs et 5 de largeurs)
        """
        global coord_all_wall
        
        coord_all_wall = []
        #On créé un "tableau" de 5x3 où chaque cellule sera un rectangle
        position_mur = [randint(0,3), randint(380,590), randint(660,900)]
        
        for pos in position_mur:
            for ligne in range(5): 
                lst_ligne_brique = []
                for colonne in range(3):
                    brique = lib.brique([pos+25*ligne,475+25*colonne])
                    position_x = brique.get_position()[0]
                    position_y = brique.get_position()[1]
                    brique_GUI = self.canevas.create_rectangle(position_x , position_y , position_x+25 , position_y+25 , fill = 'red')
                    lst_ligne_brique.append([brique,brique_GUI])
                coord_all_wall.append(lst_ligne_brique)