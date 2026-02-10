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
    """
    Effectuer un mouvement sur le plateau.

    :param plateau: Une grille TAILLExTAILLE du jeu.
    :type plateau: List[List[int]]
    :param direction: La direction du déplacement : 'g' (gauche), 'd' (droite), 'h' (haut), 'b' (bas).
    :type direction: str
    :return: Retourne un tuple (nouveau_plateau, points, est_fini).
    :rtype: tuple[List[List[int]], int, bool]
    """
    nouveau_plateau = [ligne[:] for ligne in plateau] # On copie pour ne pas modifier l'original
    points = 0
    est_fini = False
    
    if direction == 'g':
        nouveau_plateau = _deplacer_gauche(nouveau_plateau)
    elif direction == 'd':
        # Astuce : inverser, aller à gauche, ré-inverser
        nouveau_plateau = [_inverser_lignes(l) for l in nouveau_plateau]
        nouveau_plateau = _deplacer_gauche(nouveau_plateau)
        nouveau_plateau = [_inverser_lignes(l) for l in nouveau_plateau]
    elif direction == 'h':
        # Ici il faudra utiliser une fonction transposer
        nouveau_plateau = _transposer(nouveau_plateau)
        nouveau_plateau = _deplacer_gauche(nouveau_plateau)
        nouveau_plateau = _transposer(nouveau_plateau)
    elif direction == 'b':
        nouveau_plateau = _transposer(nouveau_plateau)
        # Bas = Droite sur une grille transposée
        nouveau_plateau = [_inverser_lignes(l) for l in nouveau_plateau]
        nouveau_plateau = _deplacer_gauche(nouveau_plateau)
        nouveau_plateau = [_inverser_lignes(l) for l in nouveau_plateau]
        nouveau_plateau = _transposer(nouveau_plateau)

    # Vérification si le mouvement a changé quelque chose
    # (Si rien ne bouge, on ne rajoute pas de tuile normalement)
    
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
            nouvelle_ligne.appends(nombre)
    return nouvelle_ligne

def _fusionner(ligne: List[int]) -> Tuple[List[int], int]:
    """
    Fusionne les valeurs identiques consécutives d'une ligne.

    :param ligne: Une ligne sans zéros.
    :type ligne: List[int]
    :return: La ligne après fusion, les points gagnés
    :rtype: Tuple[List[int], int]
    """
    liste_fusionnee = []
    point = 0
    i = 0
    while i < len(ligne):
        if i + 1 < len(ligne) and ligne[i] == ligne(i+1):
            fusion = ligne[i] + ligne[i+1]
            point += fusion
            liste_fusionnee.append(fusion)
            i += 2
        else:
            liste_fusionnee(ligne[i])
            i += 1
    return liste_fusionnee, point

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

def _transposer(plateau): # ajouter les annotations de type
    """
    DOCSTRING À ÉCRIRE
    """
    taille = len(plateau)
    nouvelle_grille = [[0] * taille for _ in range(taille)]
    for l in range(taille):
        for c in range(taille):
            nouvelle_grille[c][l] = plateau[l][c]
    return nouvelle_grille

def _deplacer_haut(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers le haut en fusionnant les valeurs identiques.

    :param plateau: La grille actuelle du jeu.
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    """
    grille_t = _transposer(plateau)
    # On imagine que _deplacer_gauche renvoie (grille, score)
    nouvelle_grille_t, points = _deplacer_gauche(grille_t)
    return _transposer(nouvelle_grille_t), points


def _deplacer_bas(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers le bas en fusionnant les valeurs identiques.

    :param plateau: La grille actuelle du jeu.
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    """
    grille_t = _transposer(plateau)
    nouvelle_grille_t, points = _deplacer_droite(grille_t)
    return _transposer(nouvelle_grille_t), points

def _partie_terminee(plateau: List[List[int]]) -> bool:
    """
    DOCSTRING À ÉCRIRE
    """
    # Partie non terminee si il y a des cases vides
    # Partie non terminee si il y a des fusions possibles (horizontale ou verticale)
    # Sinon c'est vrai

    # 1. On cherche s'il reste une case vide
    for ligne in plateau:
        if 0 in ligne:
            return False
            
    # 2. On cherche une fusion possible (voisins identiques)
    for l in range(4):
        for c in range(4):
            # Test voisin de droite
            if c < 3 and plateau[l][c] == plateau[l][c+1]:
                return False
            # Test voisin du bas
            if l < 3 and plateau[l][c] == plateau[l+1][c]:
                return False
                
    return True