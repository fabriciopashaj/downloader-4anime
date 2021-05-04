# TODO: Make doc
def format_source(name: str, ep: int = None) -> str:
    """
    """
    return f'https://v5.4animu.me/{name}/{name}-Episode-{ep}-1080p.mp4' if ep is not None\
            else f'https://v5.4animu.me/{name}/'
def format_name(name: str) -> str:
    return '-'join(map(str.capitalize, name.replace(' ', '-').split('-')))
def format_url(name: str, ep: int = None) -> str:
    return f'https://4anime.to/{name}/{name}-Episode-{ep}-1080p.mp4' if ep is not None\
            else f'https//4anime.to/{name}/'
