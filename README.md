# MU4RBI01 Projet Python

**Participants:** *(Groupe 5, IPS TSDM)*

- ELION GALIBA Fady (*fady2010*)
- NOCHÉ Kévin (*NKevinVI*)
- SIVATHASAN Ramya (*RamyaThasan*)

**Langage:** *Français*

---

## But du Projet

Création d'un simple jeu de tactique en 2D à deux joueurs, dans lequel chaque joueur incarne un clan de dragons.

À faire:
- Un rapport de 2 pages présentant les fonctionnalités implémentées dans le Projet, et la justifications des choix de conception du diagramme de classes UML.
- Un diagramme des classes UML modélisant le Projet.

Fonctionnalités du jeu:
- Le jeu se joue à au moins deux joueurs.
- Un joueur dispose de plusieurs *unités*.
- Le joueur peut décider de déplacer l'*unité*, utiliser sa compétence ou la laisser ne rien faire.
- Il y aura quatre types d'*unités*.
- Lorsqu'un joueur n'a plus d'*unité*, il a perdu.
- Une *unité* doit disposer:
    - D'un nombre de points de vie (`health`)
    - Une statistique d'attaque (`attack_power`)
    - Une statistique de défense (`resistance`)
    - Une statistique de vitesse (`speed`)
- Les unités auront différentes compétences (au moins trois différentes).
- Le terrain aura au minimum trois types de cases différentes (neutre, naturel, mort). Chaque type de case peut être un "sous-type" d'une autre classe (la forêt est naturelle, un vieux champ de bataille mort).
- Le calcul des HP doit dépendre:
    - La puissance de la compétence subie (si une compétence a été utilisée)
    - La puissance d'attaque (`attack_power`) de l'*unité* ayant lancé l'attaque
    - La résistance (`resistance`) de l'*unité* cible

Fonctionnalités supplémentaires:
- Système de ramassage d'objets et d'utilisation de ces objets.
- Easter Egg (seul cas où les 2 joueurs gagnent)

**Date limite de fin du Projet: 13 décembre 2024**

Pour plus d'informations, voir le fichier `Sujet.pdf`.

---

## Comment lancer le jeu?

Aller dans le dossier `SourceCode` et lancer le fichier `game.py`.
Une autre possibilité est de taper `python3 game.py` ou `python game.py` dans un terminal *Bash*, dans le dossier `SourceCode/`.

Il est également possible de lancer `exec(open("game.py").read())` dans un shell *Python*, depuis le dossier `SourceCode`.

---

## Comment jouer?

Le jeu n'est effectivement pas simple si on a pas les touches basiques avec lesquelles jouer.
Voici donc son mode d'emploi:

| Touche(s) | Action effectué. |
| --- | --- |
| Clique droit Souris | Permet de choisir l'unité à jouer. Une fois l'unité sélectionnée, on joue sans retour en arrière! |
| Touches directionnelles | Pour déplacer l'unité que vous avez choisie. |
| Z, Q, S, D | Permettent de diriger une attaque simple. |
| Espace | Une fois l'attaque simple dirigée sur une unité, permet d'attaquer. |
| X | Action spéciale de l'unité. |
| Échap | Dans certains cas, annule le coup spéciale de l'unité. |

À chaque tour, le joueur choisit une unité, peut **ou** la déplacer, **ou** la faire attaquer, **ou** encore lui faire faire son attaque spéciale.

Il existe trois types de classes, communes et identiques pour chaque camp:

- Le _Gueux_: Son attaque spéciale est simplement sa régénération de points de vie. Il se déplace de 2 cases.
- Le _Soldat_: Son attaque spéciale est une attaque de zone à distance. Il se déplace de 4 cases.
- Le _Royal_: Son attaque spéciale est une attaque berserk, qui multiplie les dégâts mais engendre des dommages à celui qui les donnent. Il se déplace d'une seule case.

---

## Licence

**Tous droits réservés.**

> Les outils utilisés ici sont fournis par _Sorbonne Université_ et les bibliothèques _Python_; l'univers est le produit des collaborateurs (toute ressemblance avec une marque ou un fait réel est une pure coïncidence). Le but de ce projet est en tout premier lieu éducatif.

![](SdI.png)
![](pygame_logo.png)
