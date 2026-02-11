"""Module providing the logic of the 2048 game"""

import random
import copy
from typing import List, Tuple

TAILLE:int = 4


# ==========================================================
# 🎯 FONCTION PUBLIQUE (API POUR L’INTERFACE)
# ==========================================================

def nouvelle_partie() -> Tuple[List[List[int]], int]:
    """
    Crée une nouvelle partie du jeu 2048.

    :return: Une grille TAILLExTAILLE initialisée avec deux tuiles, ainsi que le score à 0.
    :rtype: Tuple[List[List[int]], int]
    """
    plateau = _creer_plateau_vide()
    plateau1 = _ajouter_tuile(plateau)
    plateau2 = _ajouter_tuile(plateau1)
    return plateau2, 0
    

def jouer_coup(plateau: List[List[int]], direction: str) -> tuple[List[List[int]], int, bool]:
    # 1. On garde une copie pour vérifier si ça a bougé
    plateau_avant = copy.deepcopy(plateau)
    
    # 2. On appelle tes fonctions de mouvement
    if direction == 'g':
        nouveau_plateau, points = _deplacer_gauche(plateau)
    elif direction == 'd':
        nouveau_plateau, points = _deplacer_droite(plateau)
    elif direction == 'h':
        nouveau_plateau, points = _deplacer_haut(plateau)
    elif direction == 'b':
        nouveau_plateau, points = _deplacer_bas(plateau)
    else:
        return plateau, 0, _partie_terminee(plateau)

    # 3. SI le mouvement a changé quelque chose, on ajoute une tuile
    # (C'est ce que vérifie le Cas 1 et Cas 2 du test)
    if nouveau_plateau != plateau_avant:
        # Ici on appelle la fonction qui pose un 2 ou un 4 au hasard
        # Elle s'appelle souvent 'ajouter_nouvelle_tuile' ou 'apparition'
        nouveau_plateau = _ajouter_tuile(nouveau_plateau)

    # 4. On vérifie si c'est fini
    est_fini = _partie_terminee(nouveau_plateau)

    return nouveau_plateau, points, est_fini

# ==========================================================
# 🔒 FONCTIONS PRIVÉES (LOGIQUE INTERNE)
# ==========================================================

def _creer_plateau_vide() -> List[List[int]]:
    """
    Crée une grille TAILLExTAILLE remplie de zéros.
    :return: Une grille vide.
    :rtype: List[List[int]]
    """
    return [[0 for _ in range(TAILLE)] for _ in range(TAILLE)]

def _get_cases_vides(plateau: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Retourne les coordonnées des cases vides sous forme d'une liste de coordonnées

    :param plateau: La grille actuelle.
    :type plateau: List[List[int]]
    :return: Une liste de coordonnées
    :rtype: List[Tuple[int, int]]
    """
    cases_vides = []
    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if plateau[i][j] == 0:
                cases_vides.append((i,j))
    return cases_vides

def _ajouter_tuile(plateau: List[List[int]]) -> List[List[int]]:
    """
    Ajoute une tuile de valeur 2 sur une case vide.

    :param plateau: La grille actuelle.
    :type plateau: List[List[int]]
    :return: Une nouvelle grille avec une tuile ajoutée.
    :rtype: List[List[int]]
    """
    n_plateau = copy.deepcopy(plateau)
    mes_cases_vides = _get_cases_vides(plateau)
    (i, j) = random.choice(mes_cases_vides)
    n_plateau[i][j] = 2
    return n_plateau

def _supprimer_zeros(ligne: List[int]) -> List[int]:
    """
    Supprime les zéros d'une ligne.

    :param ligne: Une ligne de la grille.
    :type ligne: List[int]
    :return: La ligne sans zéros.
    :rtype: List[int]
    """
    nouvelle_ligne = []
    for nombre in ligne:
        if nombre != 0:
            nouvelle_ligne.append(nombre)
    return nouvelle_ligne

def _fusionner(ligne: List[int]) -> Tuple[List[int], int]:
    """
    Fusionne les valeurs identiques consécutives d'une ligne.

    :param ligne: Une ligne sans zéros.
    :type ligne: List[int]
    :return: La ligne après fusion, les points gagnés
    :rtype: Tuple[List[int], int]
    """
    liste_fusionee = []
    point = 0
    i = 0
    while i < len(ligne):
        if i + 1 < len(ligne) and ligne[i] == ligne[i+1]:
            fusion = ligne[i] + ligne[i + 1]
            point = point + fusion
            liste_fusionee.append(fusion)
            i += 2
        else:
            liste_fusionee.append(ligne[i])
            i += 1
    return liste_fusionee, point

def _completer_zeros(ligne): # ajouter les annotations de type
    """
    DOCSTRING À ECIRE
    """
    while len(ligne) < 4:
        ligne.append(0)
    return ligne
        

def _deplacer_gauche(plateau) : # ajouter les annotations de type
    """
    DOCSTRING À ÉCRIRE
    """
    new_plateau = []
    new_score = 0
    for ligne in plateau:
        ligne_sans_zero = _supprimer_zeros(ligne)
        ligne_fusionnee, point = _fusionner(ligne_sans_zero)
        new_score = new_score + point
        ligne_finale = _completer_zeros(ligne_fusionnee)
        new_plateau.append(ligne_finale)
    return new_plateau, new_score

def _inverser_lignes(plateau): # ajouter les annotations de type
    """
    DOCSTRING À ÉCRIRE
    """
    result =[]
    for ligne in plateau:
        result.append(ligne[::-1])
    return result

def _deplacer_droite(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers la droite en fusionnant les valeurs identiques.

    :param plateau: La grille actuelle du jeu.
    :type plateau: List[List[int]]
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    :rtype: Tuple[List[List[int]], int]
    """
    plateau_inverse = _inverser_lignes(plateau)
    plateau_jouer_g, score = _deplacer_gauche(plateau_inverse)
    plateau_final = _inverser_lignes(plateau_jouer_g)
    return plateau_final, score

def _transposer(plateau: list[list[int]]) -> list[list[int]]:
    """
    Retourne une nouvelle grille où les lignes du plateau deviennent des colonnes.
    """
    TAILLE = len(plateau)
    # 1. On crée d'abord une grille remplie de 0
    nouvelle_grille = [[0] * TAILLE for _ in range(TAILLE)]
    
    # 2. On remplit avec les valeurs du plateau d'origine
    for l in range(TAILLE):
        for c in range(TAILLE):
            # La ligne 'l' devient la colonne 'l'
            nouvelle_grille[c][l] = plateau[l][c]
            
    return nouvelle_grille

def _deplacer_haut(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers le haut en fusionnant les valeurs identiques.

    :param plateau: La grille actuelle du jeu.
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    """
    plateau_h = _transposer(plateau)
    #on imagine que _deplacer_gauche renvoie (plateau, score)
    nouveau_plateau_h, score = _deplacer_gauche(plateau_h)
    return _transposer(nouveau_plateau_h), score


def _deplacer_bas(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers le bas en fusionnant les valeurs identiques.

    :param plateau: La grille actuelle du jeu.
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    """
    plateau_b = _transposer(plateau)
    #on imagine que _deplacer_gauche renvoie (plateau, score)
    nouveau_plateau_b, score = _deplacer_droite(plateau_b)
    return _transposer(nouveau_plateau_b), score


def _partie_terminee(plateau: List[List[int]]) -> bool:
    """
    Retourne True si aucune case n'est vide et aucune fusion n'est possible.
    """
    TAILLE = len(plateau)

    # 1. On cherche une case vide (0)
    for l in range(TAILLE):
        for c in range(TAILLE):
            if plateau[l][c] == 0:
                return False

    # 2. On cherche une fusion horizontale possible
    for l in range(TAILLE):
        for c in range(TAILLE - 1): # -1 pour ne pas sortir de la grille
            if plateau[l][c] == plateau[l][c + 1]:
                return False

    # 3. On cherche une fusion verticale possible
    for l in range(TAILLE - 1):
        for c in range(TAILLE):
            if plateau[l][c] == plateau[l + 1][c]:
                return False

    # Si on arrive ici, c'est que tout est bloqué
    return True