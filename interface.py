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
import random


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
        global current_game_id        #permettra d'arreter les fonctions en cours d'exécution lors de la fin de partie
        current_game_id = 0
        global game_id
        game_id = 0
        global score
        score = 0
        self.score.set(str(score))
        global liste_shoot
        liste_shoot = []
        self.vaisseau_joueur()
        self.create_wall()
        self.Vaisseau_alien()
        self.tir_alien()
        self.deplacement_shoot()
        self.colision()

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
        Efface tout le canevas et affiche game over
        """
        global current_game_id
        global game_id
        global liste_shoot
        global coord_all_alien
        global coord_all_wall
        global mon_vaisseau
        self.canevas.delete("all")
        game_id = current_game_id + 1
        liste_shoot = []
        coord_all_alien = []
        coord_all_wall = []
        mon_vaisseau = None
        self.canevas.create_text( 500 , 300 , text = "Game\nOver", fill = "white" , font = ('Courier', 150, 'bold'))

    def vaisseau_joueur(self):
        global mon_vaisseau
        global mon_vaisseau_gui
        mon_vaisseau = lib.Vaisseau(0,20,3,[100,640])
        position_x = mon_vaisseau.get_position()[0]
        position_y = mon_vaisseau.get_position()[1]
        mon_vaisseau_gui = self.canevas.create_rectangle(position_x , position_y , position_x+20 , position_y+20 , fill = 'white')
        self.vie.set(str(mon_vaisseau.get_vie()))

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
        if pAuteur == 0:
            ball_gui = self.canevas.create_oval(position_x_ball , position_y_ball , position_x_ball+10 , position_y_ball+10, fill = 'blue')
        elif pAuteur == 1:
            ball_gui = self.canevas.create_oval(position_x_ball , position_y_ball , position_x_ball+10 , position_y_ball+10, fill = 'red')
        liste_shoot.append([ball,ball_gui]) 

    def deplacement_shoot(self):
        global liste_shoot
        global game_id
        global current_game_id
        if game_id == current_game_id:
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
                if position_y == 0 or position_y == 700:
                    self.canevas.delete(projectile_gui)
            self.mywindow.after(200,self.deplacement_shoot)

    # def deplacement_ball(self):
    #     global ball
    #     global ball_gui
    #     ball.deplacement_haut_shoot()
    #     position_x_ball = ball.get_position()[0]
    #     position_y_ball = ball.get_position()[1]
    #     self.canevas.coords(ball_gui , position_x_ball , position_y_ball , position_x_ball+10 , position_y_ball+10)
    #     self.mywindow.after(500,self.deplacement_ball)

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

    def tir_alien(self):
        global game_id
        global current_game_id
        if game_id == current_game_id:
            chance = random.randint(1,10)
            if chance <= 6 :
                global coord_all_alien
                num = random.randint(0,4)
                alien_tireur  = coord_all_alien[2][num][0]
                position_tireur = alien_tireur.get_position()
                type_tireur = alien_tireur.get_type()
                self.create_ball(position_tireur,type_tireur)
            self.mywindow.after(2000,self.tir_alien)

    def colision_check (self,element1,element2):
        x_element1 = element1.get_position()[0]
        y_element1 = element1.get_position()[1]
        x_element2 = element2.get_position()[0]
        y_element2 = element2.get_position()[1]
        # hit_box_1 = [x_element1,x_element1+20,y_element1,y_element1+20]
        hit_box_2 = [x_element2-25,x_element2+25,y_element2-25,y_element2+25]
        if (hit_box_2[0] <= x_element1-10 <= hit_box_2[1] and hit_box_2[2] <= y_element1-10 <= hit_box_2[3]) or (hit_box_2[0] <= x_element1+10 <= hit_box_2[1] and hit_box_2[2] <= y_element1+10 <= hit_box_2[3]) :
            return True
        else :
            return False

    def colision (self):
        global coord_all_alien
        global liste_shoot
        global mon_vaisseau
        global mon_vaisseau_gui
        global coord_all_wall
        global game_id
        global current_game_id
        if game_id == current_game_id:
            liste_tempo = liste_shoot
            for i,val1 in enumerate (liste_shoot):                #val1 représente la liste [shoot,shoot_gui]
                shoot = val1[0]
                shoot_gui = val1[1]
                auteur = shoot.get_auteur()
                if auteur == 1 or auteur == 2 or auteur == 3:
                    for mur in coord_all_wall :
                        for colonne in mur :
                            for val2 in colonne :     #val2 représente la liste [brique,brique_gui]                            
                                fragment = val2[0]
                                fragment_gui = val2[1]
                                validite_wall = self.colision_check(shoot,fragment)
                                if validite_wall :
                                    self.canevas.delete(shoot_gui,fragment_gui)
                                    liste_shoot.remove(val1)
                                    colonne.remove(val2)
                    validite_joueur = self.colision_check(shoot,mon_vaisseau)
                    if validite_joueur :
                        if mon_vaisseau.get_vie() > 1 :
                            self.canevas.delete(shoot_gui)
                        elif mon_vaisseau.get_vie() == 1 :
                            self.canevas.delete(mon_vaisseau_gui,shoot_gui)
                            self.fin_partie()
                        new_vie = mon_vaisseau.get_vie() - 1
                        mon_vaisseau.set_vie(new_vie)
                        self.vie.set(str(mon_vaisseau.get_vie()))
                        liste_shoot.remove(val1)

                elif auteur == 0 :
                    for ligne in coord_all_alien :
                        for vaisseau in ligne :
                            vaisseau_enemi = vaisseau[0]
                            vaisseau_enemi_gui = vaisseau[1]
                            validite = self.colision_check(shoot,vaisseau_enemi)
                            if validite :
                                self.add_score(vaisseau_enemi.get_type())
                                self.canevas.delete(vaisseau_enemi_gui,shoot_gui)
                                liste_shoot.remove(val1)
                                # ligne.remove(vaisseau)
                    for val3 in liste_tempo[:i]+liste_tempo[i+1:]:
                        shoot2 = val3[0]
                        shoot2_gui = val3[1]
                        validite = self.colision_check(shoot,shoot2)
                        if validite :
                            self.canevas.delete(shoot2_gui,shoot_gui)
                            liste_shoot.remove(val1)
                            liste_shoot.remove(val3)
                    for mur in coord_all_wall :
                        for colonne in mur :
                            for val4 in colonne :     #val4 représente la liste [brique,brique_gui]
                                fragment = val4[0]
                                fragment_gui = val4[1]
                                validite_wall = self.colision_check(shoot,fragment)
                                if validite_wall :
                                    self.canevas.delete(shoot_gui)
                                    liste_shoot.remove(val1)          
            self.mywindow.after(100,self.colision)

    def create_wall(self):
        """
        Fonction qui créé un mur de brique (3 briques de hauteurs et 5 de largeurs)
        """
        global coord_all_wall
        
        coord_all_wall = []
        #On créé un "tableau" de 5x3 où chaque cellule sera un rectangle
        position_mur = [random.randint(0,330), random.randint(380,590), random.randint(660,900)]
        for pos in position_mur:
            mur = []
            for colonne in range(5): 
                lst_colonne_brique = []
                for ligne in range(3):
                    brique = lib.brique([pos+25*colonne,475+25*ligne])
                    position_x = brique.get_position()[0]
                    position_y = brique.get_position()[1]
                    brique_GUI = self.canevas.create_rectangle(position_x , position_y , position_x+25 , position_y+25 , fill = 'red')
                    valren = [brique,brique_GUI]
                    lst_colonne_brique.append(valren)
                mur.append(lst_colonne_brique)
            coord_all_wall.append(mur)

    def add_score (self,pType):
        global score
        if pType == 1 :
            point = 30
        elif pType == 2 :
            point = 10
        elif pType == 3 :
            point = 150
        score += point
        self.score.set(str(score))