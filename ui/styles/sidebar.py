def get_sidebar_style(theme: dict) -> str:
    return f"""
        /* ── SIDEBAR ─────────────────────────────────────────────────── */
        QFrame#sidebar {{
            background-color: {theme['BG_SIDEBAR']};
            border-right: 1px solid {theme['SEPARATOR']};
        }}

        QFrame#sidebarHeader {{
            background-color: {theme['BG_SIDEBAR']};
        }}

        /* Logo */
        QLabel#logoMark {{
            color: {theme['ACCENT']};
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 1px;
        }}

        QLabel#appTitle {{
            color: {theme['TEXT_DARK']};
            font-size: 14px;
            font-weight: 600;
        }}

        /* Botón colapsar */
        QPushButton#toggleBtn {{
            background-color: transparent;
            color: {theme['TEXT_MUTED']};
            border: 1px solid {theme['SEPARATOR']};
            border-radius: 5px;
            font-size: 13px;
            font-weight: bold;
        }}
        QPushButton#toggleBtn:hover {{
            color: {theme['TEXT_DARK']};
            border-color: {theme['BORDER']};
            background-color: {theme['BG_ELEVATED']};
        }}

        /* Separadores internos */
        QFrame#topLine, QFrame#divider {{
            background-color: {theme['SEPARATOR']};
        }}

        /* Etiqueta de sección */
        QLabel#sectionLabel {{
            color: {theme['TEXT_HINT']};
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
            padding-left: 8px;
        }}

        /* ── NAV BUTTONS ──────────────────────────────────────────────── */
        QPushButton#navBtn {{
            background-color: transparent;
            color: {theme['TEXT_MUTED']};
            text-align: left;
            padding: 0 12px 0 16px;
            border: none;
            border-left: 3px solid transparent;
            border-radius: 0px;
            font-size: 13px;
            font-weight: 400;
        }}
        QPushButton#navBtn:hover {{
            background-color: {theme['BG_SIDEBAR2']};
            color: {theme['TEXT_DARK']};
            border-left-color: {theme['BORDER']};
        }}
        QPushButton#navBtn:checked {{
            background-color: {theme['ACCENT_SOFT']};
            color: {theme['ACCENT']};
            border-left-color: {theme['ACCENT']};
            font-weight: 600;
        }}

        /* ── SIDEBAR FOOTER ───────────────────────────────────────────── */
        QFrame#sidebarFooter {{
            background-color: {theme['BG_SIDEBAR']};
            border-top: 1px solid {theme['SEPARATOR']};
        }}

        QLabel#avatar {{
            background-color: {theme['ACCENT_SOFT']};
            color: {theme['ACCENT']};
            border-radius: 14px;
            font-size: 12px;
            font-weight: 700;
            border: 1px solid {theme['ACCENT']};
        }}

        QLabel#userName {{
            color: {theme['TEXT_DARK']};
            font-size: 13px;
            font-weight: 600;
        }}

        QLabel#userRole {{
            color: {theme['TEXT_MUTED']};
            font-size: 11px;
        }}
    """
