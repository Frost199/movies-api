"""
Get Movies Service
"""
from requests import get


def get_movies(url: str, page: int):
    """
    Get movies from https://www.themoviedb.org/
    Args:
        url: url to get the movies
        page: page to get movies
    Returns:

    """
    constructed_url = '{}&page={}'.format(url, str(page))
    return get(constructed_url)
