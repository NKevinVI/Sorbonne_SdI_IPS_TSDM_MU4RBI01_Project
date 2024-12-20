from graphviz import Digraph

"""
    Dans ce fichier réside le diagramme UML du projet. Pour le visualiser, exécuter ce fichier.
"""

# Création du diagramme UML
uml = Digraph(format='pdf')
uml.attr(rankdir='BT', size='10,10')

# Définition des classes principales
uml.node("Game", '''{
{Game} |
{+ screen: pygame.surface.Surface\\l+ good_units: list[Unit]\\l+ evil_units: list[Unit]\\l+ PauperNumTot: int\\l+ mana_src: list[Mana]\\l+ no_death: int\\l+ music_file: str\\l} |
{+ __init__(screen)\\l+ play_music(music_file:str)\\l+ team(unit:Unit): int\\l+ handle_turn(unit_set:list[Unit])\\l+ rmv_dead(unit_set:list[Unit]): list[Unit]\\l+ flip_display()\\l+ GameOver(): bool\\l}
}''', shape='record')

uml.node("Main", '''{
{Main} |
{+ reset: bool\\l} |
{+ __init__()\\l+ restart()\\l}
}''', shape='record')

uml.node("Mana", '''{
{Mana} |
{+ x: int\\l+ y: int\\l+ here: bool\\l+ rect: pygame.rect.Rect\\l} |
{+ __init__(x:int, y:int)\\l+ absorbed(owner:Unit)\\l+ draw(screen:pygame.surface.Surface)\\l}
}''', shape='record')

uml.node("Menu", '''{
{Menu} |
{+ screen: pygame.surface.Surface\\l+ font_title: pygame.font.Font\\l+ font_option: pygame.font.Font\\l+ selected_option: str\\l+ background: pygame.surface.Surface\\l} |
{+ __init__(screen:pygame.surface.Surface)\\l+ display()\\l}
}''', shape='record')

uml.node("Unit", '''{
{Unit \{abstract\}} |
{+ x: int\\l+ y: int\\l+ rect: pygame.rect.Rect\\l+ team: str\\l+ is_selected: bool\\l+ move_count: int\\l+ is_alive: bool\\l+ protected: bool\\l} |
{+ __init__(x:int, y:int, team:str)\\l+ move(dx:int, dy:int, game:Game)\\l+ dmg(dmg:int)\\l+ attack_simple(evils:list[Unit], goods:list[Unit],\\lAttaque:bool, Deplacer:bool, event:pygame.event.Event,\\ltarget:Unit, game:Game): bool\\l+ attack_show(target:list[int], Attaque:bool,\\lDeplacer:bool, event:pygame.event.Event): list[int]\\l+ draw(screen:pygame.surface.Surface) \{abstract\}\\l}
}''', shape='record')

uml.node("Royal", '''{
{Royal} |
{+ health: int\\l+ attack_power: int\\l+ resistance: int\\l+ speed: int\\l} |
{+ __init__(x:int, y:int, team:str)\\l+ attack_berserk(evils:list[Unit],\\lgoods:list[Unit], Attaque:bool,\\lDeplacer:bool, event:pygame.event.Event,\\ltarget:Unit, game:Game): bool\\l+ draw(screen:pygame.surface.Surface)\\l}
}''', shape='record')

uml.node("Soldier", '''{
{Soldier} |
{+ health: int\\l+ attack_power: int\\l+ resistance: int\\l+ speed: int\\l} |
{+ __init__(x:int, y:int, team:str)\\l+ attack_special(area:list[int], foe:Unit)\\l+ draw(screen:pygame.surface.Surface)\\l}
}''', shape='record')

uml.node("Pauper", '''{
{Pauper} |
{+ health: int\\l+ attack_power: int\\l+ resistance: int\\l+ speed: int\\l} |
{+ __init__(x:int, y:int, team:str)\\l+ heal(heal:bool, event:pygame.event.Event,\\lgame:Game): bool\\l+ attack_simple(evils:list[Unit], goods:list[Unit],\\lAttaque:bool, Deplacer:bool,\\levent:pygame.event.Event, target:Unit,\\lgame:Game): bool\\l+ attack_show(target:list[int], Attaque:bool,\\lDeplacer:bool, event:pygame.event.Event): list[int]\\l+ draw(screen:pygame.surface.Surface)\\l}
}''', shape='record')

uml.node("VictoryDisplay", '''{
{VictoryDisplay} |
{+ screen: pygame.surface.Surface\\l+ font: pygame.font.Font\\l+ font_title: pygame.font.Font\\l+ font_option: pygame.font.Font\\l} |
{+ __init__(screen:pygame.surface.Surface)\\l+ play_music(music_file:str)\\l+ show_good_won()\\l+ show_evil_won()\\l+ show_tie()\\l+ show_no_war()\\l+ show_easter()\\l}
}''', shape='record')


# Relations entre les classes
uml.edge('Royal', 'Unit', label='Héritage', arrowhead='empty')
uml.edge('Soldier', 'Unit', label='Héritage', arrowhead='empty')
uml.edge('Pauper', 'Unit', label='Héritage', arrowhead='empty')

uml.edge('Unit', 'Game', label='Composition', arrowhead='diamond')
uml.edge('Mana', 'Game', label='Composition', arrowhead='diamond')
uml.edge('VictoryDisplay', 'Game', label='Composition', arrowhead='diamond')

uml.edge('Menu', 'Main', label='Composition', arrowhead='diamond')
uml.edge('Game', 'Main', label='Composition', arrowhead='diamond')

# Génération du fichier et ouverture
uml.render("UML")
