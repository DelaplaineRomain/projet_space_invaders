# -*- coding : utf-8 -*-

# Header
"""
objectif : tester le fonctionnement des foncitons de la librairie 
Fait par Gouchon Léo et Delaplaine Romain
Date de dernière modification : 18/12/2020
To do : d'autres test plus spécifiques 
"""

import librairie as lib

# Test pour la classe Vaisseau
print("\n### Test classe Vaisseau")

my_ship = lib.Vaisseau(0,20,3,[50,50])

print("\nLes getteurs")

test1 = my_ship.get_type()
print ("\nResultat attendu: 0 , Resulat:",test1)

test2 = my_ship.get_vie()
print ("Resultat attendu: 3 , Resulat:",test2)

test3 = my_ship.get_position()
print ("Resultat attendu: [50,50] , Resulat:",test3)

my_ship.set_position([100,100])
my_ship.set_type(1)
my_ship.set_vie(1)

print("\nLes setteurs")

test4 = my_ship.get_type()
print ("\nResultat attendu: 1 , Resulat:",test4)

test5 = my_ship.get_vie()
print ("Resultat attendu: 1 , Resulat:",test5)

test6 = my_ship.get_position()
print ("Resultat attendu: [100,100] , Resulat:",test6)

my_ship.deplacement_bas()
my_ship.deplacement_haut()
my_ship.deplacement_gauche()
my_ship.deplacement_droite()

print("\nLes déplacements")

test7 = my_ship.get_position()
print ("\nResultat attendu: [100,100] , Resulat:",test7)

# Test pour la classe shoot
print("\n### Test classe shoot")

my_shoot = lib.shoot([50,50],0,5)

print("\nLes getteurs")

test8 = my_shoot.get_auteur()
print ("\nResultat attendu: 0 , Resulat:",test8)

test9 = my_shoot.get_position()
print ("Resultat attendu: [50,50] , Resulat:",test9)

test10 = my_shoot.get_type()
print ("Resultat attendu: 5 , Resulat:",test10)

my_shoot.deplacement_bas_shoot()
my_shoot.deplacement_haut_shoot()

print("\nLes déplacements")

test11 = my_shoot.get_position()
print ("\nResultat attendu: [50,50] , Resulat:",test11)

# Test pour la classe shoot
print("\n### Test classe brique")

my_rock = lib.brique([50,50],6)

print("\nLes getteurs")

test12 = my_rock.get_position()
print ("\nResultat attendu: [50,50] , Resulat:",test12)

test13 = my_rock.get_type()
print ("Resultat attendu: 6 , Resulat:",test13)