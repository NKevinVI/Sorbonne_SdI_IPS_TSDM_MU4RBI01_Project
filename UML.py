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
{+ screen: pygame.Surface\\l+ good_units: list[Unit]\\l+ evil_units: list[Unit]\\l+ PauperNumTot: int\\l+ mana_src: list[Mana]\\l+ no_death: int\\l+ music_file: str\\l} |
{+ __init__(screen)\\l+ play_music(music_file:str)\\l+ team(unit:Unit)\\l+ handle_turn(unit_set:list[Unit])\\l+ rmv_dead(unit_set:list[Unit])\\l+ flip_display()\\l+ GameOver()\\l}
}''', shape='record')

uml.node("Main", '''{
{Main} |
{+ reset: bool\\l} |
{+ __init__()\\l+ restart()\\l}
}''', shape='record')

uml.node("Mana", '''{
{Mana} |
{+ x: int\\l+ y: int\\l+ here: bool\\l+ rect: pygame.Rect\\l} |
{+ __init__(x:int, y:int)\\l+ absorbed(owner:Unit)\\l+ draw(screen:pygame.Surface)\\l}
}''', shape='record')

uml.node("Menu", '''{
{Menu} |
{+ screen: pygame.Surface\\l+ font_title: pygame.font.Font\\l+ font_option: pygame.font.Font\\l+ selected_option: str\\l+ background: pygame.Surface\\l} |
{+ __init__(screen:pygame.Surface)\\l+ display()\\l}
}''', shape='record')

uml.node("Unit", '''{
{Unit} |
{+ x: int\\l+ y: int\\l+ rect: pygame.Rect\\l+ team: str\\l+ is_selected: bool\\l+ move_count: int\\l+ is_alive: bool\\l+ protected: bool\\l} |
{+ __init__(x:int, y:int, team:str)\\l+ move(dx:int, dy:int, game:Game)\\l+ dmg(dmg:int)\\l+ attack_simple(evils:list[Unit], goods:list[Unit], Attaque:bool, Deplacer:bool,\\levent:pygame.event.Event, target:Unit, game:Game)\\l+ attack_show(target:list[int], Attaque:bool, Deplacer:bool, event:pygame.event.Event)\\l+ draw(screen:pygame.Surface)\\l}
}''', shape='record')

uml.node("Royal", '''{
{Royal} |
{+ health: int\\l+ attack_power: int\\l+ resistance: int\\l+ speed: int\\l} |
{+ __init__(x:int, y:int, team:str)\\l+ attack_berserk(evils:list[Unit],\\lgoods:list[Unit], Attaque:bool,\\lDeplacer:bool, event:pygame.event.Event,\\ltarget:Unit, game:Game)\\l+ draw(screen:pygame.Surface)\\l}
}''', shape='record')

uml.node("Soldier", '''{
{Soldier} |
{+ health: int\\l+ attack_power: int\\l+ resistance: int\\l+ speed: int\\l} |
{+ __init__(x:int, y:int, team:str)\\l+ attack_special(area:list[int], foe:Unit)\\l+ draw(screen:pygame.Surface)\\l}
}''', shape='record')

uml.node("Pauper", '''{
{Pauper} |
{+ health: int\\l+ attack_power: int\\l+ resistance: int\\l+ speed: int\\l} |
{+ __init__(x:int, y:int, team:str)\\l+ heal(heal:bool, event:pygame.event.Event,\\lgame:Game)\\l+ attack_simple(evils:list[Unit], goods:list[Unit],\\lAttaque:bool, Deplacer:bool,\\levent:pygame.event.Event, target:Unit,\\lgame:Game)\\l+ draw(screen:pygame.Surface)\\l}
}''', shape='record')

uml.node("VictoryDisplay", '''{
{VictoryDisplay} |
{+ screen: pygame.Surface\\l+ font: pygame.font.Font\\l+ font_title: pygame.font.Font\\l+ font_option: pygame.font.Font\\l} |
{+ __init__(screen:pygame.Surface)\\l+ play_music(music_file:str)\\l+ show_good_won()\\l+ show_evil_won()\\l+ show_tie\\l+ show_no_war()\\l+ show_easter\\l}
}''', shape='record')


# Relations entre les classes
uml.edge('Royal', 'Unit', label='Héritage', arrowhead='empty')
uml.edge('Soldier', 'Unit', label='Héritage', arrowhead='empty')
uml.edge('Pauper', 'Unit', label='Héritage', arrowhead='empty')

uml.edge('Game', 'Unit', label='Agrégation', arrowhead='odiamond')
uml.edge('Game', 'Mana', label='Composition', arrowhead='diamond')
uml.edge('Game', 'Menu', label='Composition', arrowhead='diamond')
uml.edge('Game', 'VictoryDisplay', label='Composition', arrowhead='diamond')
uml.edge('Main', 'Game', label='Composition', arrowhead='diamond')

# Génération du fichier et ouverture
uml.render("UML")
