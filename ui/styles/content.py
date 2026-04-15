def get_content_style(theme: dict) -> str:
    return f"""
        /* ── CONTENT AREA ─────────────────────────────────────────────── */
        QFrame#contentArea {{
            background-color: {theme['BG_CONTENT']};
        }}

        /* ── TOP BAR ──────────────────────────────────────────────────── */
        QFrame#topBar {{
            background-color: {theme['BG_SIDEBAR']};
            border-bottom: 1px solid {theme['SEPARATOR']};
        }}

        QFrame#topBarLine {{
            background-color: {theme['SEPARATOR']};
        }}

        QLabel#moduleTitle {{
            color: {theme['TEXT_DARK']};
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 0.2px;
        }}

        QLabel#breadcrumb {{
            color: {theme['TEXT_MUTED']};
            font-size: 12px;
        }}

        /* Botón de tema — estilo chip compacto */
        QPushButton#themeToggleBtn {{
            background-color: {theme['BG_ELEVATED']};
            color: {theme['TEXT_MUTED']};
            border: 1px solid {theme['BORDER']};
            border-radius: 6px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: 500;
        }}
        QPushButton#themeToggleBtn:hover {{
            background-color: {theme['BG_SURFACE']};
            color: {theme['TEXT_DARK']};
            border-color: {theme['ACCENT']};
        }}

        /* ── WORKSPACE ────────────────────────────────────────────────── */
        QFrame#workspace {{
            background-color: {theme['BG_CONTENT']};
        }}
    """
