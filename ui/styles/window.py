def get_window_style(theme: dict) -> str:
    return f"""
        /* ── GLOBAL RESET ─────────────────────────────────────────────── */
        MainWindow, SetupView {{
            background-color: {theme['BG_BASE']};
        }}
        QWidget {{
            color: {theme['TEXT_DARK']};
            font-family: 'Segoe UI', 'Inter', 'SF Pro Text', sans-serif;
            font-size: 13px;
        }}

        /* Scroll bars */
        QScrollBar:vertical {{
            background: transparent;
            width: 8px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {theme['BORDER']};
            border-radius: 4px;
            min-height: 24px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {theme['TEXT_HINT']};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        QScrollBar:horizontal {{
            background: transparent;
            height: 8px;
        }}
        QScrollBar::handle:horizontal {{
            background: {theme['BORDER']};
            border-radius: 4px;
            min-width: 24px;
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0;
        }}
        QScrollBar::corner {{
            background: transparent;
        }}

        /* Tooltip */
        QToolTip {{
            background-color: {theme['BG_ELEVATED']};
            color: {theme['TEXT_DARK']};
            border: 1px solid {theme['BORDER']};
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 12px;
        }}
    """
