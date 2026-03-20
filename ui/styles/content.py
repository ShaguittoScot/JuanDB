def get_content_style(theme: dict) -> str:
    return f"""
        /* ── CONTENT AREA ────────────────────────────────────────── */
        QFrame#contentArea {{
            background-color: {theme['BG_CONTENT']};
        }}

        QPushButton#themeToggleBtn {{
            background-color: {theme['BG_CARD']};
            color: {theme['TEXT_DARK']};
            border: 1px solid {theme['BORDER']};
            border-radius: 4px;
            padding: 4px 12px;
            font-family: "Courier New";
            font-weight: bold;
        }}
        QPushButton#themeToggleBtn:hover {{
            background-color: {theme['BG_CONTENT']};
            border: 1px solid {theme['ACCENT']};
            color: {theme['ACCENT']};
        }}

        QFrame#topBar {{
            background-color: {theme['BG_CARD']};
        }}

        QFrame#topBarLine {{
            background-color: {theme['BORDER']};
        }}

        QLabel#moduleTitle {{
            color: {theme['TEXT_DARK']};
            letter-spacing: 0.5px;
        }}

        QLabel#breadcrumb {{
            color: {theme['TEXT_MUTED']};
            letter-spacing: 1px;
        }}

        QFrame#workspace {{
            background-color: {theme['BG_CONTENT']};
        }}
    """
