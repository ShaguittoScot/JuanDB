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

        /* Dialog */
        QDialog, QDialog#formCard {{
            background-color: {theme['BG_CARD']};
            color: {theme['TEXT_DARK']};
        }}

        /* GroupBox dentro de diálogos */
        QDialog QGroupBox {{
            background-color: transparent;
            color: {theme['TEXT_MUTED']};
            border: 1px solid {theme['BORDER']};
            border-radius: 8px;
            margin-top: 20px;
            padding: 18px 12px 12px 12px;
            font-weight: 600;
            font-size: 12px;
        }}
        QDialog QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 12px;
            top: -10px;
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 6px;
            padding-right: 6px;
            margin: 2px;
            background-color: {theme['BG_CARD']};
            color: {theme['TEXT_MUTED']};
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1px;
        }}

        /* Labels dentro de diálogos */
        QDialog QLabel {{
            color: {theme['TEXT_DARK']};
            margin: 2px;
        }}
        QDialog QLabel[class="text-light"] {{
            color: {theme['TEXT_LIGHT']};
            margin: 2px;
        }}
        QDialog QLabel[class="text-muted"] {{
            color: {theme['TEXT_MUTED']};
            margin: 2px;
        }}

        /* ComboBox dentro de diálogos */
        QDialog QComboBox {{
            background-color: {theme['BG_ELEVATED']};
            border: 1px solid {theme['BORDER']};
            border-radius: 6px;
            padding: 10px 12px;
            color: {theme['TEXT_DARK']};
        }}
        QDialog QComboBox:hover {{
            border-color: {theme['TEXT_MUTED']};
        }}
        QDialog QComboBox:focus {{
            border: 2px solid {theme['ACCENT']};
            background-color: {theme['BG_SURFACE']};
        }}

        /* CheckBox dentro de diálogos */
        QDialog QCheckBox {{
            color: {theme['TEXT_DARK']};
        }}
        QDialog QCheckBox::indicator {{
            border: 1.5px solid {theme['BORDER']};
            background-color: {theme['BG_ELEVATED']};
        }}
        QDialog QCheckBox::indicator:checked {{
            background-color: {theme['ACCENT']};
            border-color: {theme['ACCENT']};
        }}
    """
