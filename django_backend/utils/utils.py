def unique_article_slug_between_dbs(db_alias, slug):
    return (db_alias.replace("_", "-") + slug).replace(" ", "-").lower()


def get_settings_path(prod=False):
    """
    Determine the appropriate settings path based on the 'prod' argument.

    Parameters:
    - prod (bool): A boolean indicating if the production settings should be used.

    Returns:
    - str: Path to the appropriate settings module.
    """

    # If 'prod' is True, return the production settings path.
    if prod:
        return "core.settings.prod"

    # Default to development settings path.
    return "core.settings.dev"
