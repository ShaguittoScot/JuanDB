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

        /* ── HELP ICON ────────────────────────────────────────────────── */
        QPushButton#helpIconBtn {{
            color: {theme['TEXT_MUTED']};
            border: none;
            background: transparent;
            padding: 0 4px 4px 4px;
        }}
        QPushButton#helpIconBtn:hover {{
            color: {theme['TEXT_DARK']};
            background: transparent;
        }}
        QPushButton#helpIconBtn:pressed {{
            color: {theme['ACCENT']};
        }}

        /* ── USER PROFILE WIDGET ──────────────────────────────────────── */
        QFrame#userProfileWidget {{
            border-radius: 8px;
            border: 1px solid transparent;
        }}
        QFrame#userProfileWidget:hover {{
            background-color: {theme['BG_ELEVATED']};
            border-color: {theme['BORDER']};
        }}
        QLabel#userAvatar {{
            background-color: {theme['ACCENT_SOFT']};
            color: {theme['ACCENT']};
            border-radius: 14px;
            font-weight: 700;
        }}
        QMenu#userMenu {{
            background-color: {theme['BG_SURFACE']};
            border: 1px solid {theme['BORDER']};
            border-radius: 10px;
            padding: 6px;
            color: {theme['TEXT_DARK']};
            font-family: 'Segoe UI', sans-serif;
            font-size: 13px;
        }}
        QMenu#userMenu::item {{
            padding: 9px 16px;
            border-radius: 6px;
        }}
        QMenu#userMenu::item:selected {{
            background-color: {theme['BG_ELEVATED']};
        }}
        QMenu#userMenu::separator {{
            height: 1px;
            background: {theme['SEPARATOR']};
            margin: 4px 10px;
        }}
        QLabel#userLogoutItem {{
            color: {theme['ERROR']};
            padding: 9px 16px;
            border-radius: 6px;
        }}
        QLabel#userLogoutItem:hover {{
            background-color: rgba(248, 81, 73, 0.10);
        }}
    """
