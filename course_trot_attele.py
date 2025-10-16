# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import random


def race_initialize(nb_horses, type_race):
    """Initialise l'état de la course"""
    horses = []
    for i in range(nb_horses):
        horses.append({
            'numero': i + 1,
            'vitesse': 0,
            'distance': 0,
            'disqualifie': False,
            'arrive': False,
            'position_arrivee': 0
        })

    # Déterminer le nombre de chevaux à afficher à l'arrivée
    if type_race.lower() == 'tierce':
        nb_a_display = 3
    elif type_race.lower() == 'quarte':
        nb_a_display = 4
    elif type_race.lower() == 'quinte':
        nb_a_display = 5
    else:
        nb_a_display = 3  # Par défaut

    return horses, nb_a_display

def speed_evolution(current_speed, de):
    """Calcule la nouvelle vitesse selon le tableau 1"""
    if current_speed == 0:
        evolution = [0, 0, 1, 1, 1, 2, 2]
    elif current_speed == 1:
        evolution = [0, 0, 1, 1, 1, 2]
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
        return current_speed  # Cas par défaut

    change = evolution[de - 1]

    if change == 'DQ':
        return 'DQ'

    new_speed = current_speed + change
    return max(0, min(6, new_speed))  # Vitesse entre 0 et 6

def distance_traveled(speed):
    """Retourne la distance parcourue selon le tableau 2"""
    distances = {0: 0, 1: 23, 2: 46, 3: 69, 4: 92, 5: 115, 6: 138}
    return distances.get(speed, 0)

def display_race_status(horses, round):
    """Affiche l'état actuel de la course"""
    print(f"\n=== Tour {round} ===")
    print("Cheval | Vitesse | Distance | Statut")
    print("-" * 40)

    for horse in horses:
        if horse['disqualifie']:
            status = "DISQUALIFIÉ"
        elif horse['arrive']:
            status = f"ARRIVÉ ({horse['position_arrivee']}ème)"
        else:
            status = "En course"

        print(f"{horse['numero']:6} | {horse['vitesse']:7} | {horse['distance']:8} | {status}")

def play_round(horses, remaining_position):
    """Joue un tour de course pour tous les chevaux"""
    for horse in horses:
        if not horse['arrive'] and not horse['disqualifie']:
            # Lancer le dé
            de = random.randint(1, 6)

            # Calculer la nouvelle vitesse
            news_speed = speed_evolution(horse['vitesse'], de)

            if news_speed == 'DQ':
                horse['disqualifie'] = True
                horse['vitesse'] = 0
                print(f"Cheval {horse['numero']} disqualifié !")
            else:
                horse['vitesse'] = news_speed
                distance_round = distance_traveled(horse['vitesse'])

                # Vérifier si le cheval arrive pendant ce tour
                if horse['distance'] + distance_round >= 2400 and not horse['arrive']:
                    # Le cheval arrive pendant ce tour
                    horse['distance'] = 2400  # Exactement la ligne d'arrivée
                    horse['arrive'] = True
                    horse['position_arrivee'] = remaining_position[0]
                    remaining_position.pop(0)
                    print(f"Cheval {horse['numero']} arrive en position {horse['position_arrivee']} !")
                elif not horse['arrive']:
                    # Le cheval n'arrive pas encore, on ajoute la distance normalement
                    horse['distance'] += distance_round

def race_ends(horses):
    """Vérifie si la course est terminée (tous les chevaux non disqualifiés sont arrivés)"""
    for horses in horses:
        if not horses['disqualifie'] and not horses['arrive']:
            return False  # Il reste au moins un cheval non disqualifié qui n'est pas arrivé
    return True  # Tous les chevaux non disqualifiés sont arrivés

def display_results(horses, nb_a_display, type_race):
    """Affiche les résultats finaux de la course"""
    print(f"\n{'='*50}")
    print(f"RÉSULTATS FINAUX - {type_race.upper()}")
    print(f"{'='*50}")

    # Trier les chevaux par position d'arrivée (du 1er au dernier)
    horses_arrives = [c for c in horses if c['arrive']]
    horses_arrives_sort = sorted(horses_arrives, key=lambda x: x['position_arrivee'])

    horses_disqualifies = [c for c in horses if c['disqualifie']]
    horses_no_arrives = [c for c in horses if not c['arrive'] and not c['disqualifie']]

    print(f"\n--- Classement final ---")
    if horses_arrives_sort:
        for horse in horses_arrives_sort:
            print(f"{horse['position_arrivee']}ème : Cheval {horse['numero']} - Distance: {horse['distance']}m")
    else:
        print("Aucun cheval n'est arrivé !")

    print(f"\n--- Résultats pour le {type_race.upper()} ---")

    # CORRECTION : Afficher les PREMIERS chevaux arrivés selon le type de course
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

    # Saisie des paramètres
    while True:
        try:
            nb_horses = int(input("Nombre de chevaux (12-20): "))
            if 12 <= nb_horses <= 20:
                break
            else:
                print("Veuillez entrer un nombre entre 12 et 20.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    type_race = input("Type de course (tierce/quarte/quinte): ").strip()

    # Initialisation
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
