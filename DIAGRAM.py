from graphviz import Digraph

# Création du diagramme UML
uml = Digraph(format='pdf')
uml.attr(rankdir='BT', size='8,10')

# Ajout des classes principales avec le constructeur
uml.node("Game", '''{
{Game} |
{+ screen: Surface\\l+ good_units: list[Unit]\\l+ evil_units: list[Unit]\\l+ mana_src: list[Mana]\\l+ no_death: int\\l+ PauperNumTot: int\\l} |
{+ __init__(screen)\\l+ team(unit)\\l+ handle_turn(unit_set)\\l+ rmv_dead(unit_set)\\l+ flip_display()\\l+ GameOver()\\l}
}''', shape='record')

uml.node("Mana", '''{
{Mana} |
{+ x: int\\l+ y: int\\l+ here: bool\\l} |
{+ __init__(x, y)\\l+ absorbed(owner)\\l+ draw(screen)\\l}
}''', shape='record')

uml.node("Menu", '''{
{Menu} |
{+ screen: Surface\\l+ font_title: Font\\l+ font_option: Font\\l+ selected_option: str\\l+ background: Surface\\l} |
{+ __init__(screen)\\l+ display()\\l}
}''', shape='record')

uml.node("VictoryDisplay", '''{
{VictoryDisplay} |
{+ screen: Surface\\l+ font: Font\\l} |
{+ __init__(screen)\\l+ display_message(message, color)\\l+ play_music(music_file)\\l+ stop_music()\\l+ show_good_won()\\l+ show_evil_won()\\l+ show_tie()\\l+ show_easter()\\l}
}''', shape='record')

uml.node("Unit", '''{
{Unit} |
{+ x: int\\l+ y: int\\l+ health: int\\l+ attack_power: int\\l+ team: str\\l+ is_selected: bool\\l+ move_count: int\\l+ is_alive: bool\\l+ protected: bool\\l} |
{+ __init__(x, y, team)\\l+ move(dx, dy, game)\\l+ dmg(dmg)\\l+ attack_simple(evils, goods, Attaque, Deplacer, event, target, game)\\l+ attack_show(target, Attaque, Deplacer, event)\\l+ draw(screen)\\l}
}''', shape='record')

uml.node("Royal", '''{
{Royal} |
{+ health: int\\l+ attack_power: int\\l+ resistance: int\\l+ speed: int\\l} |
{+ __init__(x, y, team)\\l+ attack_berserk(evils, goods, Attaque, Deplacer, event, target, game)\\l+ draw(screen)\\l}
}''', shape='record')

uml.node("Soldier", '''{
{Soldier} |
{+ health: int\\l+ attack_power: int\\l+ resistance: int\\l+ speed: int\\l} |
{+ __init__(x, y, team)\\l+ attack_special(area, foe)\\l+ draw(screen)\\l}
}''', shape='record')

uml.node("Pauper", '''{
{Pauper} |
{+ health: int\\l+ attack_power: int\\l+ resistance: int\\l+ speed: int\\l} |
{+ __init__(x, y, team)\\l+ heal(heal, event, game)\\l+ draw(screen)\\l}
}''', shape='record')

# Relations entre les classes
uml.edge('Royal', 'Unit', label='héritage', arrowhead='empty')
uml.edge('Soldier', 'Unit', label='héritage', arrowhead='empty')
uml.edge('Pauper', 'Unit', label='héritage', arrowhead='empty')

uml.edge('Game', 'Unit', label='agrégation', arrowhead='vee')
uml.edge('Game', 'Mana', label='association', arrowhead='vee')
uml.edge('Game', 'Menu', label='composition', arrowhead='diamond')
uml.edge('Game', 'VictoryDisplay', label='composition', arrowhead='diamond')

# Générez le fichier et ouvrez-le
uml.render("test-output", view=True)
