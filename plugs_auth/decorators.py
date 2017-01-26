from plugs_auth.settings import plugs_auth_settings as settings

def dynamicviewset(viewset):
    """
    The activate route only makes sense if
    user activation is required, remove the
    route if activation is turned off
    """
    if not settings['REQUIRE_ACTIVATION'] and hasattr(viewset, 'activate'):
        delattr(viewset, 'activate')
    return viewset
    
