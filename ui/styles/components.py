def get_components_style(theme: dict) -> str:
    return f"""
        /* ── CARD ────────────────────────────────────────────────── */
        QFrame#card {{
            background-color: {theme['BG_CARD']};
            border-radius: 12px;
            border: 1px solid {theme['BORDER']};
        }}

        QLabel#cardTag {{
            color: {theme['ACCENT']};
            letter-spacing: 3px;
        }}

        QFrame#accentLine {{
            background-color: {theme['ACCENT']};
            border-radius: 2px;
        }}

        QLabel#cardDesc {{
            color: {theme['TEXT_MUTED']};
            line-height: 1.6;
        }}

        /* ── PLACEHOLDER ─────────────────────────────────────────── */
        QFrame#placeholder {{
            background-color: {theme['BG_CONTENT']};
            border-radius: 8px;
            border: 1px dashed {theme['BORDER']};
        }}

        QLabel#phLabel {{
            color: {theme['TEXT_MUTED']};
            letter-spacing: 2px;
        }}

        /* ── STACK ───────────────────────────────────────────────── */
        QStackedWidget#stack {{
            background-color: transparent;
        }}
    """
