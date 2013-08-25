def ox_notifications():
    try:
        from ...communique import register, send
    except ImportError:
        try:
            from ..communique import register, send
        except ImportError:
            return
    
    from .lib.notifications import forward_to_game, forward_to_profile
    
    register('ultimate_ox.new_game', 'New game', 'http://localhost:6543/static/images/communique/ox.png', forward_to_game)
    register('ultimate_ox.new_move', 'New move', 'http://localhost:6543/static/images/communique/ox.png', forward_to_game)
    register('ultimate_ox.end_game', 'Game over', 'http://localhost:6543/static/images/communique/ox.png', forward_to_game)
    register('ultimate_ox.win_game', 'Victory!', 'http://localhost:6543/static/images/communique/ox.png', forward_to_game)

def includeme(config):
    ox_notifications()
    
    from . import views
    
    # General views
    config.add_route('ultimate_ox.menu', '/menu')
    config.add_route('ultimate_ox.stats', '/stats')
    config.add_route('ultimate_ox.head_to_head_stats', '/head_to_head_stats')
    config.add_route('ultimate_ox.preferences', '/preferences')
    config.add_route('ultimate_ox.documentation', '/documentation')
    
    config.add_view(views.menu, route_name='ultimate_ox.menu', renderer='templates/general/menu.pt', permission='loggedin')
    config.add_view(views.stats, route_name='ultimate_ox.stats', renderer='templates/general/stats.pt', permission='loggedin')
    config.add_view(views.preferences, route_name='ultimate_ox.preferences', renderer='templates/general/preferences.pt', permission='loggedin')
    config.add_view(views.head_to_head_stats, route_name='ultimate_ox.head_to_head_stats', renderer='templates/general/head_to_head_stats.pt', permission='loggedin')
    config.add_view(views.documentation, route_name='ultimate_ox.documentation', renderer='templates/general/documentation.pt', permission='loggedin')
    
    # Game views
    config.add_route('ultimate_ox.new_game', '/new_game')
    config.add_route('ultimate_ox.rematch', '/rematch/{game_id}')
    
    config.add_route('ultimate_ox.view_game', '/game/{game_id}')
    config.add_route('ultimate_ox.check_turn', '/check_turn/{game_id}')
    config.add_route('ultimate_ox.make_move', '/make_move')
    
    config.add_view(views.new_game, route_name='ultimate_ox.new_game', renderer='templates/game/new_game.pt', permission='loggedin')
    config.add_view(views.view_game, route_name='ultimate_ox.view_game', renderer='templates/game/view_game.pt', permission='loggedin')
    
    config.add_view(views.make_move, route_name='ultimate_ox.make_move', renderer='templates/game/make_move.pt', permission='loggedin')
    config.add_view(views.rematch, route_name='ultimate_ox.rematch', renderer='string', permission='loggedin')
    config.add_view(views.check_turn, route_name='ultimate_ox.check_turn', renderer='string', permission='loggedin')
    
    return config
