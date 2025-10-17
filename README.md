# Simulateur de Course de Trot Attelé  
## 1- Description 
Ce programme simule une course de trot attelé selon les règles officielles du turf. Il permet de simuler des courses de type tiercé, quarté ou quinté avec un nombre variable de chevaux (12 à 20).

## 2- Fonctionnalités 
- Configuration flexible : Choix du nombre de chevaux (12-20) et type de course (tiercé, quarté, quinté)

- Simulation réaliste : Implémentation fidèle des règles d'évolution de vitesse

- Gestion des disqualifications : Respect des conditions de disqualification

- Affichage détaillé : Statut en temps réel et résultats finaux complets

- Interface interactive : Contrôle tour par tour de la progression

## 3- Règles du jeu 
### Évolution de la vitesse 
La vitesse des chevaux évolue selon un tableau prédéfini basé sur des lancers de dé.

### Distance parcourue 
La distance parcourue par tour dépend de la vitesse.

### Conditions de victoire 
- Longueur de course : 2400 mètres

- Arrivée : Un cheval arrive quand sa distance cumulée ≥ 2400m

- Fin de course : Quand tous les chevaux non-disqualifiés sont arrivés

## 4- Architecture du code 
### Fonctions principales 
**race_initialize(nb_horses, type_race)** 
- Initialise l'état de la course et retourne la liste des chevaux et le nombre à afficher.

**speed_evolution(current_speed, de)** 
- Calcule la nouvelle vitesse basée sur la vitesse actuelle et le résultat du dé.

**distance_traveled(speed)** 
- Retourne la distance parcourue en fonction de la vitesse.

**play_round(horses, remaining_position)** 
- Exécute un tour de course pour tous les chevaux encore en course.

**race_ends(horses)** 
- Vérifie si la course est terminée.

**display_results(horses, nb_a_display, type_race)**
- Affiche les résultats finaux de la course.

**main()**
- C'est le point d'entrée du programme et assure : 
1. **Initialisation** : Accueil et configuration de la course
2. **Saisie utilisateur** : Validation des paramètres (nombre de chevaux, type de course)
3. **Boucle principale** : Gère le déroulement tour par tour de la course
4. **Contrôle de flux** : Appel séquentiel des autres fonctions
5. **Fin de jeu** : Affichage des résultats et terminaison du programme

```python```
```
def main():
    """Fonction principale du programme"""
    print("=== SIMULATEUR DE COURSE DE TROT ATTELE ===")
    
    # Configuration initiale
    # Boucle de simulation
    # Affichage des résultats
```

### Structure des données 
Chaque cheval est représenté par un dictionnaire :

```python```
```
{ 
'numero': int,             # Numéro du cheval (1 à nb_horses) 
'vitesse': int,            # Vitesse actuelle (0-6) 
'distance': int,           # Distance parcourue cumulée 
'disqualifie': bool,       # Statut de disqualification 
'arrive': bool,            # Statut d'arrivée 
'position_arrivée': int    # Position d'arrivée (0 si pas arrivé) 
}
```

## 5- Utilisation 
### Exécution du programme 
```bash``` 
```
python course_trot_attele.py
``` 
### Déroulement d'une partie 
1. **Configuration** : Saisie du nombre de chevaux et type de course

2. **Simulation** : Appui sur Entrée pour avancer tour par tour

3. **Affichage** : Statut mis à jour après chaque tour

4. **Résultats** : Classement final et résultats pour le type de course choisi

## 6- Types de courses supportées 
- **Tiercé** : Les 3 premiers chevaux

- **Quarté** : Les 4 premiers chevaux

- **Quinté** : Les 5 premiers chevaux

