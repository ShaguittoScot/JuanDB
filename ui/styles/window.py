def get_window_style(theme: dict) -> str:
    return f"""
        /* ── WINDOW ─────────────────────────────────────────────── */
        QWidget {{
            background-color: {theme['BG_CONTENT']};
            color: {theme['TEXT_DARK']};
        }}
    """
