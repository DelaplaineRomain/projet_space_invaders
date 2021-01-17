# -*- coding : utf-8 -*-

# Header
"""
objectif : créer le jeu space invaders 
Fait par Gouchon Léo et Delaplaine Romain
Date de dernière modification : 17/01/2020
To do : remplacer les rectangles par des images
        faire une fonction qui fait réaparraitre des aliens quand il n'y en a plus
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
        self.canevas.grid(padx = 10 , pady = 10)

        """"section pour les boutons quiter et lancer"""
        self.frame3 = tkinter.Frame(self.mywindow , bg = 'grey')
        self.frame3.grid(row = 1 , column = 21 , rowspan = 16 , columnspan = 5 , padx = 10 , pady = 10)
        self.bouton_lancer = tkinter.Button(self.frame3 , text = 'Start' , command = self.game_start)
        self.bouton_lancer.grid(row = 1 , column = 1, padx = 10 , pady = 10)
        self.bouton_quitter = tkinter.Button(self.frame3 , text = 'Stop' , command = self.fonction_stop)
        self.bouton_quitter.grid(row = 2 , column = 1, padx = 10 , pady = 10)

        """lancement de la fenetre"""

        self.mywindow.mainloop()

    def game_start(self):
        """
        fonction qui permet d'initialiser une partie
        elle se lance quand on appuie sur le bouton "bouton_lancer"
        """
        global game_id                  #permettra d'arreter les fonctions en cours d'exécution lors de la fin de partie   
        global current_game_id          #permettra d'arreter les fonctions en cours d'exécution lors de la fin de partie
        global list_shoot
        global score
        global speed
        global dictionnaire_image
        
        self.canevas.delete("all")
        dictionnaire_image = {}
        current_game_id = 0
        game_id = 0
        score = 0
        speed = 8
        self.create_background()
        self.score.set(str(score))
        list_shoot = []
        self.create_player_ship()
        self.create_wall()
        self.create_alien_ship()
        self.alien_shoot()
        self.deplacement_shoot()
        self.collision()
        
    def create_background(self):
        """
        fonction qui génère le fond du jeu
        """
        global dictionnaire_image

        image_background = tkinter.PhotoImage(file = "background.gif")
        dictionnaire_image["background.gif"] = image_background

        self.canevas.create_image(0, 0, anchor="nw" ,image = image_background)

    def create_alien_ship(self):
        """
        génère les vaisseaux ennemis
        
        stockage des vaisseaux_aliens : 
        coord_all_alien contient les listes coord_ligne_alien qui contiennent des sous-listes [vaisseau, vaisseau_gui]
        coord_all_alien = [[ligne 1],[ligne 2],[[vaisseau1, vaisseau1_gui],[vaisseau2, vaisseau2_gui], [etc]]] 
        """
        global alien_ship
        global alien_ship_gui      
        global dx
        global dy
        global position_x
        global position_y
        global coord_all_alien
        global dictionnaire_image

        image_alien1 = tkinter.PhotoImage(file = "alien1.gif")
        dictionnaire_image["alien1.gif"] = image_alien1

        image_alien2 = tkinter.PhotoImage(file = "alien2.gif")
        dictionnaire_image["alien2.gif"] = image_alien2
        
        image_alien3 = tkinter.PhotoImage(file = "alien3.gif")
        dictionnaire_image["alien3.gif"] = image_alien3

        all_alien_image = [image_alien1, image_alien2, image_alien3]
        dx = 1
        dy = 40
        coord_all_alien = [] 
        #On créé 5 vaisseaux à la suite sur une même ligne 3 fois
        #On aura alors un "tableau" de vaisseau de 3x5 (3 lignes, 5 colonnes)
        for ligne in range(3):
            coord_ligne_alien = [] #Liste vide qui sera remplie par les vaisseaux d'une même ligne
            for colonne in range(5):
                alien_ship = lib.Vaisseau(ligne+1,20,1,[20+100*colonne,20+100*ligne])
                position_x = alien_ship.get_position()[0]
                position_y = alien_ship.get_position()[1]
                alien_ship_gui = self.canevas.create_image(position_x, position_y, anchor = "center", image = all_alien_image[ligne])
                coord_ligne_alien.append([alien_ship, alien_ship_gui])
            coord_all_alien.append(coord_ligne_alien)
        self.alien_movement() #Lance la fonction qui permet de déplacer continuellement les vaisseaux ennemis                                                 

    def alien_movement(self):
        """
        déplacement automatique des aliens
        le vaisseau bouge toujours en premier vers la droite
        S'il atteint le bord droit, il bougera alors vers la gauche
        S'il atteint le bord gauche, il bougera alors vers la droite ET si on peut, on fait descendre les vaisseaux
        """
        global alien_ship
        global alien_ship_gui
        global dx
        global dy
        global coord_all_alien
        global speed
        global game_id
        global current_game_id
        if game_id == current_game_id:
            #Si un des vaisseaux de la colonne de droite atteint le bord de l'écran, on inverse dx afin que les vaisseaux bougent vers la gauche
            if coord_all_alien[0][-1][0].get_position()[0]+50+dx > 1000 or coord_all_alien[1][-1][0].get_position()[0]+50+dx > 1000 or coord_all_alien[2][-1][0].get_position()[0]+50+dx > 1000: 
                dx = -dx
            #Si un des vaisseaux de la colonne de gauche atteint le bord de l'écran, on inverse dx afin que les vaisseaux bougent vers la droite
            if coord_all_alien[0][0][0].get_position()[0]-10+dx < 0 or coord_all_alien[1][0][0].get_position()[0]-10+dx < 0 or coord_all_alien[2][0][0].get_position()[0]-10+dx < 0 :
                dx = -dx
                #Quand les vaisseaux atteignent le bord gauche de l'écran, on augmente la cadence de tir des vaisseaux ennemis
                if speed < 15:
                    speed += 1
                #Si les aliens n'ont pas encore atteint les ilots, ils descendent de dy
                if coord_all_alien[0][0][0].get_position()[1] - 10 + dy < 220 : 
                    for ligne in coord_all_alien:
                        for vaisseau in ligne:
                            vaisseau[0].set_position([vaisseau[0].get_position()[0],vaisseau[0].get_position()[1]+dy])
                #Si ils ont atteints les ilots MAIS qu'ils sont tous détruits, alors les vaisseaux continuent à descendre
                elif len(coord_all_wall) == 0 : 
                    for ligne in coord_all_alien:
                        for vaisseau in ligne:
                            vaisseau[0].set_position([vaisseau[0].get_position()[0],vaisseau[0].get_position()[1]+dy])

            #Dans les conditions d'avant, on actualisait la position du vaisseau, dans cette boucle, on met à jour la position graphique des vaisseaux
            for ligne in coord_all_alien:
                    for vaisseau in ligne:
                        vaisseau[0].set_position([vaisseau[0].get_position()[0] + dx,vaisseau[0].get_position()[1]])
                        #Si le vaisseau est tjr affiché à l'écran, on met à jour sa position graphique
                        try : 
                            self.canevas.coords(vaisseau[1], vaisseau[0].get_position()[0], vaisseau[0].get_position()[1])
                        #S'il n'est plus affiché, on traite l'erreur qui indique qu'il ne trouve pas le "vaisseau_gui" en ne faisant rien 
                        #Le vaisseau n'est plus affiché <=> on a supprimé la variable vaisseau_gui de ce vaisseau
                        except IndexError: 
                            pass
            #Si les aliens n'ont pas encore atteint la ligne du vaisseau du joueur, on relance cette fonction
            if coord_all_alien[-1][0][0].get_position()[1] < 620 : 
                #self.mywindow.after(200,self.alien_movement)
                self.mywindow.after(5,self.alien_movement)
            #Si des aliens ont atteint la ligne du vaisseau joueur, on arrête la partie
            else : 
                self.game_end()

        
    def game_end(self):
        """
        Fonction qui se lance quand la partie est terminé (soit le joueur n'a plus de vie, soit des vaisseaux ennemis ont atteint la ligne du vaisseau joueur)
        Efface toutes les entités du canevas et affiche à la place "Game Over"
        """
        global game_id
        global list_shoot
        global coord_all_alien
        global coord_all_wall
        global my_ship
        self.canevas.delete("all")
        game_id = 1
        list_shoot = []
        coord_all_alien = []
        coord_all_wall = []
        my_ship = None
        self.canevas.create_text( 500 , 300 , text = "Game\nOver", fill = "white" , font = ('Courier', 150, 'bold'))
        
    def fonction_stop (self):
        """
        Fonction qui se lance quand on appuie sur le bouton restart
        Efface toutes les entités du canevas et affiche à la place "Restart"
        """
        global game_id
        global list_shoot
        global coord_all_alien
        global coord_all_wall
        global my_ship
        self.canevas.delete("all")
        game_id = 1
        list_shoot = []
        coord_all_alien = []
        coord_all_wall = []
        my_ship = None
        self.canevas.create_text( 500 , 300 , text = "Restart", fill = "white" , font = ('Courier', 150, 'bold'))

    def create_player_ship(self):
        """
        Fonction qui créer un vaisseau joueur
        """
        global my_ship
        global my_ship_gui
        global dictionnaire_image

        image_vaisseau = tkinter.PhotoImage(file = "vaisseau.gif")
        dictionnaire_image["vaisseau.gif"] = image_vaisseau

        my_ship = lib.Vaisseau(0,20,3,[100,640])
        position_x = my_ship.get_position()[0]
        position_y = my_ship.get_position()[1]
        my_ship_gui = self.canevas.create_image(position_x , position_y , anchor = "center", image = image_vaisseau)
        self.vie.set(str(my_ship.get_vie()))

    def deplacement_joueur(self,pTouche):
        """
        fonction qui déplace le vaisseau allié
        Input : 
            pTouche : touche sur laquelle le joueur appuie
        """
        global my_ship
        global my_ship_gui
        if not (my_ship == None):
            touche = pTouche
            if touche == 'q' or touche == 'Left':
                my_ship.deplacement_gauche()
            if touche == 'd' or touche == 'Right':
                my_ship.deplacement_droite()
            position_x = my_ship.get_position()[0]
            position_y = my_ship.get_position()[1]
            self.canevas.coords(my_ship_gui , position_x , position_y)

    def create_ball(self, pPosition , pAuteur):
        """
        Fonction qui génère une balle
        Input : 
            pPosition : position sous forme de liste [x,y] à laquelle la balle seras créée
            pAuteur : indice entier 0 ou 1 qui indique qui est l'auteur du tir (le joueur ou un ennemi)
        """
        global ball
        global ball_gui
        global list_shoot
        ball = lib.shoot(pPosition , pAuteur , 5)
        position_x_ball = ball.get_position()[0]
        position_y_ball = ball.get_position()[1]
        if pAuteur == 0:
            ball_gui = self.canevas.create_oval(position_x_ball , position_y_ball , position_x_ball+10 , position_y_ball+10, fill = 'blue')
        elif pAuteur == 1:
            ball_gui = self.canevas.create_oval(position_x_ball , position_y_ball , position_x_ball+10 , position_y_ball+10, fill = 'red')
        list_shoot.append([ball,ball_gui]) 

    def deplacement_shoot(self):
        """
        Fonction qui s'occupe du déplacement de tout les projectiles présents sur le canevas 
        """
        global list_shoot      # liste contenant tout les projectiles présents sous la forme [[proj1,proj_gui1], etc]
        global game_id
        global current_game_id
        if game_id == current_game_id:
            for val in list_shoot:
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
                if position_y == 0 or position_y == 690:
                    self.canevas.delete(projectile_gui)
            self.mywindow.after(20,self.deplacement_shoot)

    def player_shoot(self):
        """
        fonction qui lance un tir alié depuis les coordonnés du vaisseau alié
        """
        global my_ship
        position_initial = my_ship.get_position()
        type_initial = my_ship.get_type()
        self.create_ball(position_initial,type_initial)
        
    def gestion_keyEvent(self,event):
        """
        fonction qui vérifie si le joueur appuie sur une touche autorisée et active la fonction en conséquence
        """
        touche = event.keysym
        liste = ['q','d','Right','Left']
        if touche in liste :
            self.deplacement_joueur(touche)
        if touche == 'space' :
            self.player_shoot()

    def alien_shoot(self):
        """
        Fonction qui gère les tirs aliens
        Seul les aliens se trouvant en position la plus basse peuvent tirer, les aliens ont une certaine chance aléatoire 
        de tirer, plus les aliens se rapprochent du joueur et plus les tirs seront fréquents
        """
        global game_id
        global current_game_id
        global speed
        if game_id == current_game_id:
            chance = random.randint(1,15)
            if chance <= speed :
                global coord_all_alien
                if speed < 13 : 
                    num1 = random.randint(0,4)
                    if len(coord_all_alien[2][num1]) == 2 : #Si le vaisseau qui est censé tiré est tjr affiché
                        alien_tireur  = coord_all_alien[2][num1][0]
                    elif len(coord_all_alien[1][num1]) == 2 : #Sinon on fait tirer le vaisseau du dessus
                        alien_tireur  = coord_all_alien[1][num1][0]
                    elif len(coord_all_alien[0][num1]) == 2 : #Sinon on fait tirer le vaisseau du dessus
                        alien_tireur  = coord_all_alien[0][num1][0]
                    #Si un des if ou elif a fonctionné, le try marchera
                    try :
                        position_tireur = alien_tireur.get_position()
                        type_tireur = alien_tireur.get_type()
                        self.create_ball(position_tireur,type_tireur)
                    #Sinon, on ne fait rien
                    except UnboundLocalError :
                        pass
                else :
                    num1 = random.randint(0,2) #On choisis une colonne au hasard et on fera tirer cet alien
                    if len(coord_all_alien[2][num1]) == 2 : #Si le vaisseau qui est censé tiré est tjr affiché
                        alien_tireur  = coord_all_alien[2][num1][0]
                    elif len(coord_all_alien[1][num1]) == 2 : #Sinon on fait tirer le vaisseau du dessus
                        alien_tireur  = coord_all_alien[1][num1][0]
                    elif len(coord_all_alien[0][num1]) == 2 : #Sinon on fait tirer le vaisseau du dessus
                        alien_tireur  = coord_all_alien[0][num1][0]
                    #Si un des if ou elif a fonctionné, le try marchera
                    try :
                        position_tireur = alien_tireur.get_position()
                        type_tireur = alien_tireur.get_type()
                        self.create_ball(position_tireur,type_tireur)
                    #Sinon, on ne fait rien
                    except UnboundLocalError :
                        pass
                                
                    num2 = random.randint(3,4) #On choisis une colonne au hasard et on fera tirer cet alien
                    if len(coord_all_alien[2][num2]) == 2 : #Si le vaisseau qui est censé tiré est tjr affiché
                        alien_tireur  = coord_all_alien[2][num2][0]
                    elif len(coord_all_alien[1][num2]) == 2 : #Sinon on fait tirer le vaisseau du dessus
                        alien_tireur  = coord_all_alien[1][num2][0]
                    elif len(coord_all_alien[0][num2]) == 2 : #Sinon on fait tirer le vaisseau du dessus
                        alien_tireur  = coord_all_alien[0][num2][0]
                    #Si un des if ou elif a fonctionné, le try marchera
                    try :
                        position_tireur = alien_tireur.get_position()
                        type_tireur = alien_tireur.get_type()
                        self.create_ball(position_tireur,type_tireur)
                    #Sinon, on ne fait rien
                    except UnboundLocalError :
                        pass

            self.mywindow.after(1000,self.alien_shoot)


    def collision_check (self,pElement1,pElement2):
        """
        Fonction qui test le chevauchement de deux éléments
        Input : 
            pElement1 : premier élément
            pElement2 : deuxième élément avec lequel on regardera s'il y a chevauchement
        Output :
            True s'il y a chevauchement
            False s'il n'y a pas de chevauchement
        """
        x_element1 = pElement1.get_position()[0]
        y_element1 = pElement1.get_position()[1]
        x_element2 = pElement2.get_position()[0]
        y_element2 = pElement2.get_position()[1]
        elt_type = pElement2.get_type()     # On regarde le type de l'élément deux afin de définir la hitbox correspondante
        if elt_type != 5 :
            if elt_type == 6 or elt_type == 0:
                hit_box_2 = [x_element2,x_element2+25,y_element2,y_element2+25]
            elif elt_type == 1 or elt_type == 2 or elt_type == 3 or elt_type == 4:
                hit_box_2 = [x_element2,x_element2+50,y_element2,y_element2+50]
        else :
            hit_box_2 = [x_element2,x_element2+20,y_element2,y_element2+20]
        if (hit_box_2[0] < x_element1 < hit_box_2[1] and hit_box_2[2] < y_element1 < hit_box_2[3]) or (hit_box_2[0] < x_element1+10 < hit_box_2[1] and hit_box_2[2] < y_element1+10 < hit_box_2[3]) :
            return True
        else :
            return False

    def collision (self):
        """
        Fonction qui gère les collisions entre tout les projectiles présent
        On parcourt la liste de tout les projectiles et en fonction de qui émet le tir on parcourt
        les listes d'objets avec lesquels il peut y avoir collision et regarde avec la fonciton
        collision_check si c'est le cas
        """
        global coord_all_alien
        global list_shoot
        global my_ship
        global my_ship_gui
        global coord_all_wall
        global game_id
        global current_game_id
        if game_id == current_game_id :
            if not (my_ship == None):
                liste_tempo = list_shoot
                for i,val1 in enumerate (list_shoot):                  #val1 représente la liste [shoot,shoot_gui]
                    shoot = val1[0]
                    shoot_gui = val1[1]
                    auteur = shoot.get_auteur()
                    if auteur == 1 or auteur == 2 or auteur == 3:       #le shoot vient d'un alien
                        try : #S'il reste des briques à détruire
                            for mur in coord_all_wall :
                                for colonne in mur :
                                    for val2 in colonne :               #val2 représente la liste [brique,brique_gui]                            
                                        fragment = val2[0]
                                        fragment_gui = val2[1]
                                        validite_wall = self.collision_check(shoot,fragment)
                                        if validite_wall :
                                            self.canevas.delete(shoot_gui,fragment_gui)
                                            if val1 in list_shoot : 
                                                list_shoot.remove(val1)
                                            if val2 in colonne :
                                                colonne.remove(val2)
                                    if colonne in mur :
                                        if len(colonne) == 0 :
                                            mur.remove(colonne) 
                            if mur in coord_all_wall :
                                if len(mur) == 0 :
                                    coord_all_wall.remove(mur)
                        except UnboundLocalError : #Sinon on passe
                            pass

                        if not (my_ship == None):
                            validite_joueur = self.collision_check(shoot,my_ship)
                            if validite_joueur :
                                if my_ship.get_vie() > 1 :
                                    self.canevas.delete(shoot_gui)
                                    new_vie = my_ship.get_vie() - 1
                                    my_ship.set_vie(new_vie)
                                elif my_ship.get_vie() == 1 :
                                    self.canevas.delete(my_ship_gui,shoot_gui)
                                    new_vie = my_ship.get_vie() - 1
                                    my_ship.set_vie(new_vie)
                                    self.game_end()
                                self.vie.set(str(new_vie))
                                if val1 in list_shoot:
                                    list_shoot.remove(val1)

                    elif auteur == 0 :                          #le shoot vient du joueur
                        for ligne in coord_all_alien :
                            for vaisseau in ligne :
                                if len(vaisseau) == 2 :
                                    vaisseau_ennemi = vaisseau[0]
                                    vaisseau_ennemi_gui = vaisseau[1]
                                    validite = self.collision_check(shoot,vaisseau_ennemi)
                                    if validite :
                                        self.add_score(vaisseau_ennemi.get_type())       
                                        self.canevas.delete(vaisseau_ennemi_gui,shoot_gui)
                                        if val1 in list_shoot :
                                            list_shoot.remove(val1)
                                        if vaisseau_ennemi_gui in vaisseau :
                                            vaisseau.remove(vaisseau_ennemi_gui)
                        for val3 in liste_tempo[:i]+liste_tempo[i+1:]:
                            shoot2 = val3[0]
                            shoot2_gui = val3[1]
                            validite = self.collision_check(shoot,shoot2)
                            if validite :
                                self.canevas.delete(shoot2_gui,shoot_gui)
                                if val1 in list_shoot :
                                    list_shoot.remove(val1)
                                if val3 in list_shoot :
                                    list_shoot.remove(val3)
                        for mur in coord_all_wall :
                            for colonne in mur :
                                for val4 in colonne :     #val4 représente la liste [brique,brique_gui]
                                    fragment = val4[0]
                                    fragment_gui = val4[1]
                                    validite_wall = self.collision_check(shoot,fragment)
                                    if validite_wall :
                                        self.canevas.delete(shoot_gui)
                                        if val1 in list_shoot:
                                            list_shoot.remove(val1)          
                self.mywindow.after(100,self.collision)

    def create_wall(self):
        """
        Fonction qui créé 3 murs de brique (3 briques de hauteurs et 5 de largeurs)
        On a décidé de rendre la position horizontale des murs aléatoires afin de rendre chaque partie un peu différente

        coord_all_wall : contient les informations des 3 murs
        mur : contient les informations de chaque colonne de brique de ce mur
        lst_colonne_brique : contient les informations de chaque brique de cette colonne du mur
        Chaque brique est représenté par un objet de la classe brique ainsi qu'un élement graphique appelé "brique_GUI"
        """
        global coord_all_wall
        global dictionnaire_image

        image_brique = tkinter.PhotoImage(file = "brique.gif")
        dictionnaire_image["brique.gif"] = image_brique

        coord_all_wall = []
        position_mur = [random.randint(200,275), random.randint(400,575), random.randint(700,775)]
        for pos in position_mur:
            mur = []
            for colonne in range(5): 
                lst_colonne_brique = []
                for ligne in range(3):
                    brique = lib.brique([pos+25*colonne,475+25*ligne],6)
                    position_x = brique.get_position()[0]
                    position_y = brique.get_position()[1]
                    brique_GUI = self.canevas.create_image(position_x , position_y, anchor = "center", image = image_brique)
                    valren = [brique,brique_GUI]
                    lst_colonne_brique.append(valren)
                mur.append(lst_colonne_brique)
            coord_all_wall.append(mur)

    def add_score (self,pType):
        """
        Fonction qui modifie le score en fonction de la cible touché
        Input : 
            pType : indice entier de la cible touché 
        """
        global score
        if pType == 1 :
            point = 30
        elif pType == 2 :
            point = 10
        elif pType == 3 :
            point = 150
        score += point
        self.score.set(str(score))