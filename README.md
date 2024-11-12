# MU4RBI01 Projet Python

**Participants:** *(Groupe 5, IPS TSDM)*

- ELION GALIBA Fady (*fady2010*)
- NOCHÉ Kévin (*NKevinVI*)
- SIVATHASAN Ramya (*RamyaThasan*)

**Langage:** *Français*

---

## But du Projet

Création d'un simple jeu de tactique en 2D, dans lequel chaque joueur incarne un clan de dragons.

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
    - D'un nombre de points de vie (*health*)
    - Une statistique d'attaque (*attack_power*)
    - Une statistique de défense (*resistance*)
    - Une statistique de vitesse (*speed*)
- Les unités auront différentes compétences (au moins trois différentes par type d'unité).
- Le terrain aura au minimum trois types de cases différentes (neutre, naturel, mort). Chaque type de case peut être un "sous-type" d'une autre classe (la forêt est naturelle, un vieux champ de bataille mort).
- Le calcul des HP doit dépendre:
    - La puissance de la compétence subie (si une compétence a été utilisée)
    - Les Dmg de l'*unité* ayant lancé l'attaque
    - La DR de l'*unité* cible

Fonctionnalités supplémentaires:
- Système de ramassage d'objets et d'utilisation de ces objets.

**Date limite de fin du Projet: 13 décembre 2024**

Pour plus d'informations, voir le fichier `Sujet.pdf`.

---

## Licence

**Tous droits réservés.**

> Les outils utilisés ici sont fournis par _Sorbonne Université_ et les bibliothèques _Python_; l'univers est le produit des collaborateurs (toute ressemblance avec une marque ou un fait réel est une pure coïncidence). Le but de ce projet est en tout premier lieu éducatif.

![](SdI.png)
![](pygame_logo.png)
