# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import random


def race_initialize(nb_horses, type_race):
    """Cette fonction initialise l'état de la course."""
    horses = [] # Je crée une liste vide pour stocker les chevaux.
    for i in range(nb_horses): # Pour chaque cheval, je crée un dico.
        horses.append({
            'numero': i + 1,
            'vitesse': 0,
            'distance': 0,
            'disqualifie': False,
            'arrive': False,
            'position_arrivée': 0
        })

    # Déterminer le nombre de chevaux à afficher à l'arrivée selon le type de course.
    if type_race.lower() == 'tiercé':
        nb_a_display = 3
    elif type_race.lower() == 'quarté':
        nb_a_display = 4
    elif type_race.lower() == 'quinté':
        nb_a_display = 5
    else:
        nb_a_display = 3  # La valeur par défaut étant 3.

    return horses, nb_a_display  # Je retourne la liste des chevaux et le nombre à afficher.

def speed_evolution(current_speed, de):
    """ Elle calcule l'évolution de la vitesse basée sur la vitesse actuelle et le dé"""
    if current_speed == 0: # En me basant sur le tableau d'évolution, quand la vitesse est égale à 0.
        evolution = [0, 1, 1, 1, 2, 2] # Les index (0 - 5) correspondent aux résultats du dé [1 - 6].
    elif current_speed == 1:
        evolution = [0, 0, 1, 1, 1, 2] # Pareil pour les autres.
    elif current_speed == 2:
        evolution = [0, 0, 1, 1, 1, 2]
    elif current_speed == 3:
        evolution = [-1, 0, 0, 1, 1, 1]
    elif current_speed == 4:
        evolution = [-1, 0, 0, 0, 1, 1]
    elif current_speed == 5:
        evolution = [-2, -1, 0, 0, 0, 1]
    elif current_speed == 6:
        evolution = [-2, -1, 0, 0, 0, 'DQ']
    else:
        return current_speed  # Je retourne la vitesse actuelle par défaut.

    change = evolution[de - 1] # Je récupère le changement correspondant au résultat du dé, car les listes
                               # commencent à l'index 0.
    if change == 'DQ': # Si le changement correspond à 'DQ' le cheval est disqualifié.
        return 'DQ' # Je retourne disqualifier.

    new_speed = current_speed + change # Cette variable calcule la nouvelle vitesse.
    return max(0, min(6, new_speed))  # Je retourne la valeur de la nouvelle vitesse comprise entre 0 et 6.

def distance_traveled(speed):
    """Elle retourne la distance parcourue en fonction de la vitesse donnée selon le tableau"""
    distances = {0: 0, 1: 23, 2: 46, 3: 69, 4: 92, 5: 115, 6: 138}
    """Cette variable est un dico qui mappe la vitesse
    vers la distance correspondante"""
    return distances.get(speed, 0)
    """Je retourne la distance correspondante à la vitesse, si elle n'existe pas dans le
    dico, je retourne 0."""

def display_race_status(horses, round_):
    """Elle affiche l'état actuel de la course"""

    print(f"\n=== Tour {round_} ===") # J'affiche le nombre de tours.
    print("Cheval | Vitesse | Distance | Statut") # L'en-tête qui indique les éléments avec une ligne séparatrice.
    print("-" * 40) # Je trace ma ligne.

    for horse in horses: # Je boucle pour déterminer le statut de chaque cheval.
        if horse['disqualifie']:
            status = "DISQUALIFIÉ"
        elif horse['arrive']:
            status = f"ARRIVÉ ({horse['position_arrivée']}ème)"
        else:
            status = "En course"

        print(f"{horse['numero']:6} | {horse['vitesse']:7} | {horse['distance']:8} | {status}") # J'affiche les infos.

def play_round(horses, remaining_position):
    """Joue un tour de course pour tous les chevaux"""

    for horse in horses: # Pour chaque cheval qui n'est pas arrivé et pas disqualifié.
        if not horse['arrive'] and not horse['disqualifie']:
            # Je lance le dé
            de = random.randint(1, 6)

            # Je calcule la nouvelle vitesse
            news_speed = speed_evolution(horse['vitesse'], de) # En ajoutant la fonction.

            if news_speed == 'DQ': # Ici je gère la disqualification par rapport à un cheval.
                horse['disqualifie'] = True
                horse['vitesse'] = 0
                print(f"Cheval {horse['numero']} disqualifié !")
            else:
                horse['vitesse'] = news_speed # Sinon, je mets à jour la vitesse et calcule la distance du tour
                distance_round = distance_traveled(horse['vitesse']) # En ajoutant la fonction.

                # On vérifie si le cheval arrive à la ligne d'arrivée. Si oui, on attribue la position d'arrivée.
                if horse['distance'] + distance_round >= 2400 and not horse['arrive']:

                    horse['distance'] = 2400  # Exactement la ligne d'arrivée
                    horse['arrive'] = True
                    horse['position_arrivée'] = remaining_position[0]
                    remaining_position.pop(0)
                    print(f"Cheval {horse['numero']} arrive en position {horse['position_arrivée']} !")
                elif not horse['arrive']:
                    # Sinon, on ajoute normalement la distance parcourue.
                    horse['distance'] += distance_round

def race_ends(horses):
    """Elle vérifie s'il reste des chevaux en course et retourne True seulement si tous les chevaux non disqualifiés
    sont arrivés"""
    for horse in horses:
        if not horse['disqualifie'] and not horse['arrive']:
            return False  # Il reste au moins un cheval non disqualifié qui n'est pas arrivé
    return True  # Tous les chevaux non disqualifiés sont arrivés.

def display_results(horses, nb_a_display, type_race):
    """Elle affiche les résultats finaux de la course"""
    print(f"\n{'='*50}")
    print(f"RÉSULTATS FINAUX - {type_race.upper()}") # J'affiche l'en-tête des résultats.
    print(f"{'='*50}")

    # Je filtre et trie les chevaux arrivés par position
    horses_arrives = [c for c in horses if c['arrive']]
    horses_arrives_sort = sorted(horses_arrives, key=lambda x: x['position_arrivée'])

    # Je sépare les disqualifiés et les non-arrivés
    horses_disqualifies = [c for c in horses if c['disqualifie']]
    horses_no_arrives = [c for c in horses if not c['arrive'] and not c['disqualifie']]

    print(f"\n--- Classement final ---")
    if horses_arrives_sort:
        for horse in horses_arrives_sort:
            print(f"{horse['position_arrivée']:2}ème : Cheval {horse['numero']:2} - Distance: {horse['distance']}m")
    else:
        print("Aucun cheval n'est arrivé !")

    print(f"\n--- Résultats pour le {type_race.upper()} ---")

    # J'affiche les premiers chevaux arrivés selon le type de course.
    if len(horses_arrives_sort) >= nb_a_display:
        for i in range(nb_a_display):
            horse = horses_arrives_sort[i]
            print(f"{i+1} : Cheval {horse['numero']}")
    else:
        print(f"Pas assez de chevaux arrivés pour former un {type_race} complet")
        for i, horse in enumerate(horses_arrives_sort):
            print(f"{i+1} : Cheval {horse['numero']}")

    if horses_no_arrives:
        print(f"\n--- Chevaux non arrivés ---")
        for horse in horses_no_arrives:
            print(f"Cheval {horse['numero']} - Distance: {horse['distance']}m")

    if horses_disqualifies:
        print(f"\n--- Chevaux disqualifiés ---")
        for horse in horses_disqualifies:
            print(f"Cheval {horse['numero']}")

def main():
    """Fonction principale du programme"""
    print("=== SIMULATEUR DE COURSE DE TROT ATTELÉ ===")

    # Je boucle pour la saisie d'un nombre de chevaux.
    while True:
        try:
            nb_horses = int(input("Nombre de chevaux (12-20): "))
            if 12 <= nb_horses <= 20:
                break
            else:
                print("Veuillez entrer un nombre entre 12 et 20.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    type_race = input("Type de course (tiercé/quarté/quinté): ").strip()

    # J'initialise la course et la liste des positions disponibles.
    horses, nb_a_display = race_initialize(nb_horses, type_race)
    remaining_position = list(range(1, nb_horses + 1))
    tour = 0

    print(f"\nDébut de la course avec {nb_horses} chevaux - {type_race.upper()}")
    print("Longueur de la course: 2400 m")
    print("Appuyez sur Entrée pour faire avancer la course tour par tour...")

    # Déroulement de la course
    while not race_ends(horses):
        input()  # Attendre que l'utilisateur appuie sur Entrée
        tour += 1
        play_round(horses, remaining_position)
        display_race_status(horses, tour)

        # Afficher une barre de progression
        race_horses = [c for c in horses if not c['disqualifie'] and not c['arrive']]
        print(f"\nChevaux encore en course: {len(race_horses)}")

    # Affichage des résultats finaux
    display_results(horses, nb_a_display, type_race)

if __name__ == "__main__":
    main()
