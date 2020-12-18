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

#### les fonctions propres a tkinter 

#### creation des outils tkinter

"""creation de la fenetre"""
mywindow = tkinter.Tk()
mywindow.title('Space invaders')
mywindow['bg'] = 'grey'

"""section pour le score et la vie"""
frame1 = tkinter.Frame(mywindow , bg = 'grey')
frame1.grid(row = 1 , column = 1 , columnspan = 20 , padx = 10 , pady = 10)

tkinter.Label(frame1, text = 'Score :' , bg = 'grey').grid(row = 1 , column = 1 , padx = 10 , pady = 10 , sticky = 'W')
score = tkinter.StringVar()
tkinter.Label(frame1 , textvariable = score).grid(row = 1 , column = 2 , padx = 10 , pady = 10 , sticky = 'W')

tkinter.Label(frame1, text = 'Life :' , bg = 'grey').grid(row = 1 , column = 3 , padx = 10 , pady = 10 , sticky = 'E')
vie = tkinter.StringVar()
tkinter.Label(frame1 , textvariable = vie).grid(row = 1 , column = 4 , padx = 10 , pady = 10 , sticky = 'E')

"""section pour le canvas"""
frame2 = tkinter.Frame(mywindow , bg = 'grey')
frame2.grid(row = 2 , column = 1 , rowspan = 15 , columnspan = 20 , padx = 10 , pady = 10)
Largeur = 700
Hauteur = 700
canevas = tkinter.Canvas(frame2, width = Largeur , height = Hauteur, bg = 'black' )
canevas.grid(padx = 10 , pady = 10)

""""section pour les boutons quiter et lancer"""
frame3 = tkinter.Frame(mywindow , bg = 'grey')
frame3.grid(row = 1 , column = 21 , rowspan = 16 , columnspan = 5 , padx = 10 , pady = 10)
bouton_lancer = tkinter.Button(frame3 , text = 'Start')
bouton_lancer.grid(row = 1 , column = 1, padx = 10 , pady = 10)
bouton_quitter = tkinter.Button(frame3 , text = 'Exit')
bouton_quitter.grid(row = 2 , column = 1, padx = 10 , pady = 10)

"""lancement de la fenetre"""

mywindow.mainloop()