# MU4RBI01 Projet Python

**Participants:** *(Groupe 5, IPS TSDM)*

- ELION GALIBA Fady (*fady2010*)
- NOCHÉ Kévin (*NKevinVI*)
- SIVATHASAN Ramya (*RamyaThasan*)

**Langage:** *Français*

---

## Table des Matières

* [But du Projet](https://github.com/NKevinVI/Sorbonne_SdI_IPS_TSDM_MU4RBI01_Project?tab=readme-ov-file#but-du-projet)
* [Comment lancer le jeu?](https://github.com/NKevinVI/Sorbonne_SdI_IPS_TSDM_MU4RBI01_Project?tab=readme-ov-file#comment-lancer-le-jeu)
* [Comment jouer?](https://github.com/NKevinVI/Sorbonne_SdI_IPS_TSDM_MU4RBI01_Project?tab=readme-ov-file#comment-jouer)
* [Licence](https://github.com/NKevinVI/Sorbonne_SdI_IPS_TSDM_MU4RBI01_Project?tab=readme-ov-file#licence)

---

## But du Projet

Création d'un simple jeu de tactique en 2D à deux joueurs, dans lequel chaque joueur incarne un clan de dragons.

À faire:
- Un rapport de 2 pages présentant les fonctionnalités implémentées dans le Projet, et la justification des choix de conception du diagramme de classes UML.
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
- Système de ramassage de mana, améliorant la capacité d'attaque d'une unité.
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

| Touche(s) | Action effectuée. |
| --- | --- |
| Clique gauche Souris | Permet de choisir l'unité à jouer. Une fois l'unité sélectionnée, on joue sans retour en arrière! |
| Touches directionnelles | Pour déplacer l'unité que vous avez choisie. |
| Z, Q, S, D | Permettent de diriger une attaque simple. |
| Espace | Une fois l'attaque simple dirigée sur une unité, permet d'attaquer. |
| X | Action spéciale de l'unité. |
| Échap | Dans certains cas, annule le coup spéciale de l'unité. |
| Control | Rafraîchit la fenêtre (d'autres boutons peuvent fonctionner, mais on conseille à ceux allergiques à l'informatique d'utiliser celui-ci). |

À chaque tour, le joueur choisit une unité, peut **ou** la déplacer, **ou** la faire attaquer, **ou** encore lui faire faire son attaque spéciale (seul cas particulier: le _Gueux_).

Il existe trois types de classes, communes et identiques pour chaque camp:

- Le _Gueux_: Unité représentant le peuple. Il a une vitesse de 2 cases, une résistance de 11, une puissance d'attaque de 17 et une santé de 23. Il s'agit de la seule unité capable de faire toutes ses actions en un tour (se déplacer, attacker et utiliser sa capacité spéciale). Sa capacité spéciale est de se régénérer de la moitié de sa propre puissance d'attaque; comme les autres unités, elle ne peut avoir une santé supérieure à celle attribuée par défaut (c'est-à-dire ici 23).
- Le _Soldat_: Unité représentant le pouvoir politique autour des puissants. Il a une vitesse de 3 cases, une résistance de 13, une attaque de 23 et une santé de 36. Son attaque spéciale est de pouvoir attaquer une zone de 5 cases n'importe où sur le plateau, en infligeant sa puissance s'attaque moins 4, avec pour minimum 0 dégât. Il ne peut attaquer les unités protégées par les cases spéciales (voir plus bas).
- Le _Royal_: Unité représentant le chef d'état par excellence. Il a une vitesse de 2, une résistance de 16, une attaque de 32 et une santé de 60. Son attaque spéciale est une capacité berserk lui permettant d'infliger son attaque normale plus la moitié de sa puissance d'attaque à un adversaire, sans que ce dernier puisse utiliser sa résistance; cependant, l'unité royale reçoit la moitié de sa propre puissance d'attaque sans pouvoir utiliser également sa résistance, s'ingligeant du même coup des dégâts importants.

Lorsqu'une unité reçoit des dégâts, les dégâts reçues sont la puissance d'attaque de l'adversaire moins la résistance de l'unité subissant l'attaque. Comme nous l'avons vu, le _Royal_ peut échapper à cette règle avec son attaque spéciale (berserk).

Le mana (représenté par des carrés cyans), une fois récupéré, permet d'augmenter la puissance d'attaque de l'unité l'ayant ramassé de 4.

Les méchants se trouvent sur des cases rouges par défaut, qui les protègent des attaques à distance des unités _Soldat_. Idem pour les gentils, mais sur les cases vertes.

---

## Licence

**Tous droits réservés.**

### Pour la branche *main*

Les musiques proviennent de *Sergey Cheremisinov*, et sont sous licence CC BY-NC 4.0.
L'image de début de jeu vient de l'artiste *Anne Stokes*, et peut être retrouvée sur son [site](https://annestokes.com/).

> Les outils utilisés ici sont fournis par _Sorbonne Université_ et les bibliothèques _Python_; l'univers est le produit des collaborateurs (toute ressemblance avec une marque ou un fait réel est une pure coïncidence). Le but de ce projet est en tout premier lieu éducatif.

![](SdI.png)
![](pygame_logo.png)
