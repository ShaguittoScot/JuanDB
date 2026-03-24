from .window import get_window_style
from .sidebar import get_sidebar_style
from .content import get_content_style
from .components import get_components_style
from .views import get_views_style

def get_stylesheet(theme: dict) -> str:
    """
    Combina y devuelve todos los estilos definidos en los submódulos.
    """
    styles = [
        get_window_style(theme),
        get_sidebar_style(theme),
        get_content_style(theme),
        get_components_style(theme),
        get_views_style(theme)
    ]
    
    return "".join(styles)
