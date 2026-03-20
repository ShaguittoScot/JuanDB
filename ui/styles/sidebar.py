def get_sidebar_style(theme: dict) -> str:
    return f"""
        /* ── SIDEBAR ─────────────────────────────────────────────── */
        QFrame#sidebar {{
            background-color: {theme['BG_SIDEBAR']};
            border: none;
        }}

        QFrame#sidebarHeader {{
            background-color: {theme['BG_SIDEBAR']};
        }}

        QLabel#logoMark {{
            color: {theme['ACCENT']};
            letter-spacing: 2px;
        }}

        QLabel#appTitle {{
            color: {theme['TEXT_LIGHT']};
            letter-spacing: 1px;
        }}

        QPushButton#toggleBtn {{
            background-color: {theme['BORDER']};
            color: {theme['TEXT_MUTED']};
            border: none;
            border-radius: 4px;
            font-size: 16px;
            font-weight: bold;
            padding-bottom: 2px;
        }}
        QPushButton#toggleBtn:hover {{
            background-color: {theme['SEPARATOR']};
            color: {theme['ACCENT']};
        }}

        QFrame#topLine {{
            background-color: {theme['SEPARATOR']};
        }}

        QLabel#sectionLabel {{
            color: {theme['TEXT_MUTED']};
            letter-spacing: 3px;
            padding-left: 4px;
        }}

        /* ── NAV BUTTONS ─────────────────────────────────────────── */
        QPushButton#navBtn {{
            background-color: transparent;
            color: {theme['TEXT_MUTED']};
            text-align: left;
            padding: 0 12px;
            border: none;
            border-radius: 6px;
            letter-spacing: 0.5px;
        }}
        QPushButton#navBtn:hover {{
            background-color: {theme['BG_SIDEBAR2']};
            color: {theme['TEXT_LIGHT']};
        }}
        QPushButton#navBtn:checked {{
            background-color: {theme['ACCENT']};
            color: {theme['BG_SIDEBAR']};
            font-weight: bold;
        }}

        /* ── SIDEBAR FOOTER ──────────────────────────────────────── */
        QFrame#divider {{
            background-color: {theme['SEPARATOR']};
        }}

        QFrame#sidebarFooter {{
            background-color: {theme['BG_SIDEBAR']};
        }}

        QLabel#avatar {{
            background-color: {theme['ACCENT']};
            color: {theme['BG_SIDEBAR']};
            border-radius: 16px;
            font-weight: bold;
        }}

        QLabel#userName {{
            color: {theme['TEXT_LIGHT']};
        }}

        QLabel#userRole {{
            color: {theme['TEXT_MUTED']};
            letter-spacing: 1px;
        }}
    """
