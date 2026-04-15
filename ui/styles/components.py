def get_components_style(theme: dict) -> str:
    return f"""
        /* ── CARD PRINCIPAL ───────────────────────────────────────────── */
        QFrame#card {{
            background-color: {theme['BG_SURFACE']};
            border-radius: 10px;
            border: 1px solid {theme['BORDER']};
        }}

        QLabel#cardTag {{
            color: {theme['ACCENT']};
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
        }}

        QFrame#accentLine {{
            background-color: {theme['ACCENT']};
            border-radius: 1px;
        }}

        QLabel#cardDesc {{
            color: {theme['TEXT_MUTED']};
            font-size: 13px;
            line-height: 1.5;
        }}

        /* ── PLACEHOLDER ──────────────────────────────────────────────── */
        QFrame#placeholder {{
            background-color: {theme['BG_CONTENT']};
            border-radius: 8px;
            border: 1px dashed {theme['BORDER']};
        }}

        QLabel#phLabel {{
            color: {theme['TEXT_HINT']};
            letter-spacing: 1px;
            font-size: 12px;
        }}

        /* ── STACK ────────────────────────────────────────────────────── */
        QStackedWidget#stack {{
            background-color: transparent;
        }}
    """
