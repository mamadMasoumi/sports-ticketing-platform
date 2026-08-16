def is_support_or_admin(user):
    """
    Return True if the user has role 'support' or 'admin'.
    Works with the custom AuthenticatedUser class (has `role` attribute).
    """
    return getattr(user, 'role', None) in ('support', 'admin')