from . import views

def includeme(config):
    # General views
    config.add_route('ultimate_ox.menu', '/menu')
    config.add_route('ultimate_ox.stats', '/stats')
    config.add_route('ultimate_ox.preferences', '/preferences')
    
    config.add_view(views.menu, route_name='ultimate_ox.menu', renderer='templates/general/menu.pt', permission='loggedin')
    config.add_view(views.stats, route_name='ultimate_ox.stats', renderer='templates/general/stats.pt', permission='loggedin')
    config.add_view(views.preferences, route_name='ultimate_ox.preferences', renderer='templates/general/preferences.pt', permission='loggedin')
    
    # Game views
    config.add_route('ultimate_ox.new_game', '/new_game')
    config.add_route('ultimate_ox.view_game', '/game/{game_id}')
    config.add_route('ultimate_ox.check_turn', '/check_turn/{game_id}')
    config.add_route('ultimate_ox.make_move', '/make_move')
    
    config.add_view(views.new_game, route_name='ultimate_ox.new_game', renderer='templates/game/new_game.pt', permission='loggedin')
    config.add_view(views.view_game, route_name='ultimate_ox.view_game', renderer='templates/game/view_game.pt', permission='loggedin')
    
    return config
