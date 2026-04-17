def get_views_style(theme: dict) -> str:
    return f"""
        /* ── GLOBALES DE VISTAS ─────────────────────────────────────── */
        BackupView, TransferView, SecurityView, MonitorView, SettingsView, SetupView {{
            background-color: transparent;
        }}

        /* ── INPUTS ─────────────────────────────────────────────────── */
        QComboBox, QLineEdit {{
            background-color: {theme['BG_ELEVATED']};
            border: 1px solid {theme['BORDER']};
            border-radius: 6px;
            padding: 10px 12px;
            color: {theme['TEXT_DARK']};
            font-size: 13px;
            min-height: 18px;
            selection-background-color: {theme['ACCENT']};
        }}
        QComboBox:hover, QLineEdit:hover {{
            border-color: {theme['TEXT_MUTED']};
        }}
        QComboBox:focus, QLineEdit:focus {{
            border-color: {theme['ACCENT']};
            background-color: {theme['BG_SURFACE']};
        }}
        QComboBox:disabled, QLineEdit:disabled {{
            color: {theme['TEXT_HINT']};
            border-color: {theme['SEPARATOR']};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 28px;
        }}
        QComboBox::down-arrow {{
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid {theme['TEXT_MUTED']};
            margin-right: 10px;
            width: 0px;
            height: 0px;
        }}
        QComboBox QAbstractItemView {{
            background: {theme['BG_ELEVATED']};
            background-color: {theme['BG_ELEVATED']};
            border: 1px solid {theme['BORDER']};
            border-radius: 4px;
            selection-background-color: {theme['ACCENT_SOFT']};
            selection-color: {theme['ACCENT']};
            color: {theme['TEXT_DARK']};
            outline: none;
            padding: 4px;
        }}
        QComboBox QAbstractItemView::item {{
            background-color: {theme['BG_ELEVATED']};
            padding: 6px 10px;
            border-radius: 4px;
            min-height: 18px;
        }}
        QComboBox QAbstractItemView::item:hover,
        QComboBox QAbstractItemView::item:selected {{
            background-color: {theme['ACCENT_SOFT']};
            color: {theme['ACCENT']};
        }}

        /* ── QSpinBox ────────────────────────────────────────────────── */
        QSpinBox {{
            background-color: {theme['BG_ELEVATED']};
            border: 1px solid {theme['BORDER']};
            border-radius: 6px;
            padding: 0 10px;
            color: {theme['TEXT_DARK']};
            font-size: 13px;
            min-height: 18px;
        }}
        QSpinBox:focus {{ border-color: {theme['ACCENT']}; }}
        QSpinBox::up-button, QSpinBox::down-button {{
            width: 20px;
            background: {theme['BG_ELEVATED']};
            border: none;
            border-radius: 3px;
        }}
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
            background: {theme['BG_SURFACE']};
        }}

        /* ── QSlider ─────────────────────────────────────────────────── */
        QSlider::groove:horizontal {{
            height: 4px;
            background: {theme['BORDER']};
            border-radius: 2px;
        }}
        QSlider::handle:horizontal {{
            background: {theme['ACCENT']};
            border: none;
            width: 14px; height: 14px;
            margin: -5px 0;
            border-radius: 7px;
        }}
        QSlider::sub-page:horizontal {{
            background: {theme['ACCENT']};
            border-radius: 2px;
        }}

        /* ── QListWidget ─────────────────────────────────────────────── */
        QListWidget {{
            background-color: {theme['BG_SURFACE']};
            border: 1px solid {theme['BORDER']};
            border-radius: 10px;
            padding: 8px;
            outline: none;
        }}
        QListWidget::item {{
            border-radius: 6px;
            padding: 10px 12px;
            color: {theme['TEXT_MUTED']};
            font-size: 13px;
            font-family: 'Segoe UI', sans-serif;
            font-weight: 500;
            border: none;
        }}
        QListWidget::item:selected {{
            background-color: {theme['ACCENT_SOFT']};
            color: {theme['ACCENT']};
            font-weight: 600;
        }}
        QListWidget::item:hover:!selected {{
            background-color: {theme['BG_ELEVATED']};
            color: {theme['TEXT_DARK']};
        }}


        /* ── GROUPBOX ────────────────────────────────────────────────── */
        QGroupBox {{
            border: 1px solid {theme['BORDER']};
            border-radius: 8px;
            margin-top: 16px;
            padding: 16px 12px 12px 12px;
            font-weight: 600;
            font-size: 12px;
            color: {theme['TEXT_MUTED']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 12px;
            top: -8px;
            padding: 0 6px;
            background-color: {theme['BG_SURFACE']};
            color: {theme['TEXT_MUTED']};
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1px;
        }}

        /* ── TABLAS ──────────────────────────────────────────────────── */
        QTableWidget {{
            background-color: {theme['BG_SURFACE']};
            border: 1px solid {theme['BORDER']};
            border-radius: 8px;
            color: {theme['TEXT_DARK']};
            gridline-color: {theme['SEPARATOR']};
            selection-background-color: {theme['ACCENT_SOFT']};
            selection-color: {theme['TEXT_DARK']};
            outline: none;
        }}
        QTableWidget::item {{
            padding: 6px 10px;
            border: none;
        }}
        QTableWidget::item:selected {{
            background-color: {theme['ACCENT_SOFT']};
            color: {theme['ACCENT']};
        }}
        QHeaderView::section {{
            background-color: {theme['BG_ELEVATED']};
            color: {theme['TEXT_MUTED']};
            padding: 8px 10px;
            border: none;
            border-bottom: 1px solid {theme['BORDER']};
            border-right: 1px solid {theme['SEPARATOR']};
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        QHeaderView::section:last {{
            border-right: none;
        }}

        /* ── CHECKBOX ────────────────────────────────────────────────── */
        QCheckBox {{
            color: {theme['TEXT_DARK']};
            font-size: 13px;
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 1.5px solid {theme['BORDER']};
            background-color: {theme['BG_ELEVATED']};
        }}
        QCheckBox::indicator:hover {{
            border-color: {theme['ACCENT']};
        }}
        QCheckBox::indicator:checked {{
            background-color: {theme['ACCENT']};
            border-color: {theme['ACCENT']};
        }}
        QCheckBox::indicator:checked:hover {{
            background-color: {theme['ACCENT_DARK']};
        }}

        /* ── PROGRESS BAR ────────────────────────────────────────────── */
        QProgressBar {{
            border: none;
            border-radius: 3px;
            text-align: center;
            color: transparent;
            background-color: {theme['BG_ELEVATED']};
            max-height: 6px;
        }}
        QProgressBar::chunk {{
            background-color: {theme['ACCENT']};
            border-radius: 3px;
        }}

        /* ── LOG / TERMINAL AREA ─────────────────────────────────────── */
        QTextEdit#logArea {{
            background-color: {theme['BG_BASE']};
            border: 1px solid {theme['BORDER']};
            border-radius: 8px;
            padding: 10px;
            font-family: 'Cascadia Code', 'Consolas', 'Fira Code', monospace;
            font-size: 12px;
            color: {theme['TEXT_DARK']};
        }}

        /* ── BOTÓN SECUNDARIO (objectName) ───────────────────────────── */
        QPushButton#btnSecondary {{
            background-color: transparent;
            border: 1px solid {theme['BORDER']};
            border-radius: 6px;
            color: {theme['TEXT_MUTED']};
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 500;
        }}
        QPushButton#btnSecondary:hover {{
            background-color: {theme['BG_ELEVATED']};
            border-color: {theme['TEXT_MUTED']};
            color: {theme['TEXT_DARK']};
        }}

        /* ── UTILITY CLASSES ─────────────────────────────────────────── */
        .view-title {{
            color: {theme['TEXT_DARK']};
            font-size: 22px;
            font-weight: 700;
        }}
        .view-subtitle-accent {{
            color: {theme['ACCENT']};
            font-size: 15px;
            font-weight: 600;
        }}
        .view-subtitle-muted {{
            color: {theme['TEXT_DARK']};
            font-size: 15px;
            font-weight: 600;
        }}
        .section-title {{
            color: {theme['TEXT_MUTED']};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.5px;
        }}
        .text-adaptive {{ color: {theme['TEXT_DARK']}; font-size: 13px; }}
        .text-light    {{ color: {theme['TEXT_DARK']}; }}
        .text-accent   {{ color: {theme['ACCENT']}; }}
        .text-muted    {{ color: {theme['TEXT_MUTED']}; font-size: 12px; }}
        .text-hint     {{ color: {theme['TEXT_HINT']}; font-size: 11px; }}
        .text-error    {{ color: {theme['ERROR']}; }}
        .text-success  {{ color: {theme['SUCCESS']}; }}
        .text-info     {{ color: {theme['INFO']}; }}
        .text-warning  {{ color: {theme['WARNING']}; }}
        .text-muted-11 {{ color: {theme['TEXT_MUTED']}; font-size: 11px; }}
        .text-footer   {{ color: {theme['TEXT_HINT']}; font-size: 11px; padding: 6px; }}
        .desc-muted    {{ color: {theme['TEXT_MUTED']}; font-size: 13px; }}
        .status-indicator {{ color: {theme['SUCCESS']}; font-size: 11px; }}
        .label         {{ color: {theme['TEXT_MUTED']}; font-size: 12px; font-weight: 500; }}

        /* ── CONTENEDORES AUXILIARES ─────────────────────────────────── */
        .view-container {{
            background-color: {theme['BG_ELEVATED']};
            border-radius: 8px;
            border: 1px solid {theme['SEPARATOR']};
        }}
        .view-container-small {{
            background-color: {theme['BG_ELEVATED']};
            border-radius: 6px;
            border: 1px solid {theme['SEPARATOR']};
        }}
        .options-frame {{
            background-color: {theme['BG_ELEVATED']};
            border-radius: 6px;
        }}
        .legend-container {{
            background-color: {theme['BG_ELEVATED']};
            border-radius: 6px;
            border: 1px solid {theme['SEPARATOR']};
        }}
        .h-separator {{
            background-color: {theme['SEPARATOR']};
            max-width: 1px;
        }}
        .v-gradient-divider {{
            background-color: {theme['SEPARATOR']};
            border-radius: 1px;
        }}
        .warning-box {{
            color: {theme['WARNING']};
            font-size: 12px;
            background-color: rgba(210, 153, 34, 0.08);
            padding: 10px 12px;
            border-radius: 6px;
            border: 1px solid rgba(210, 153, 34, 0.25);
        }}
        .status-panel {{
            background-color: {theme['BG_ELEVATED']};
            border-radius: 6px;
            border: 1px solid {theme['BORDER']};
        }}

        /* ── METRIC CARD ──────────────────────────────────────────────── */
        .metric-card {{
            background-color: {theme['BG_SURFACE']};
            border-radius: 8px;
            border: 1px solid {theme['BORDER']};
        }}
        .metric-card:hover {{
            border-color: {theme['ACCENT']};
        }}

        /* ── FILE SELECTOR ────────────────────────────────────────────── */
        .file-selector-input {{
            background-color: {theme['BG_ELEVATED']};
            border: 1px solid {theme['BORDER']};
            border-radius: 6px;
            padding: 7px 10px;
            color: {theme['TEXT_DARK']};
            font-size: 13px;
        }}
        .file-selector-input:focus {{
            border-color: {theme['ACCENT']};
        }}

        /* ── BOTONES GENÉRICOS ────────────────────────────────────────── */
        .btn-primary {{
            background-color: {theme['ACCENT']};
            border: none;
            border-radius: 6px;
            color: #FFFFFF;
            font-weight: 600;
            font-size: 13px;
            padding: 8px 20px;
        }}
        .btn-primary:hover {{
            background-color: {theme['ACCENT_DARK']};
        }}
        .btn-primary:disabled {{
            background-color: {theme['BORDER']};
            color: {theme['TEXT_HINT']};
        }}

        .btn-secondary-animated {{
            background-color: transparent;
            border: 1px solid {theme['BORDER']};
            border-radius: 6px;
            color: {theme['TEXT_MUTED']};
            font-weight: 500;
            font-size: 13px;
            padding: 8px 20px;
        }}
        .btn-secondary-animated:hover {{
            background-color: {theme['BG_ELEVATED']};
            border-color: {theme['TEXT_MUTED']};
            color: {theme['TEXT_DARK']};
        }}

        .btn-danger {{
            background-color: transparent;
            border: 1px solid {theme['ERROR']};
            border-radius: 6px;
            color: {theme['ERROR']};
            font-weight: 500;
            font-size: 13px;
            padding: 8px 20px;
        }}
        .btn-danger:hover:enabled {{
            background-color: {theme['ERROR']};
            color: #FFFFFF;
        }}
        .btn-danger:disabled {{
            border-color: {theme['BORDER']};
            color: {theme['TEXT_HINT']};
        }}

        .icon-14 {{ font-size: 14px; }}
        .icon-16-accent {{ font-size: 16px; color: {theme['ACCENT']}; }}
        .icon-20 {{ font-size: 20px; }}

        /* ── TAB WIDGET ─────────────────────────────────────────────── */
        QTabWidget::pane {{
            border: none;
            background-color: transparent;
        }}
        QTabWidget {{
            background-color: transparent;
        }}
        QTabBar {{
            background-color: transparent;
        }}
        QTabBar::tab {{
            background-color: transparent;
            color: {theme['TEXT_MUTED']};
            padding: 10px 20px;
            border: none;
            border-bottom: 2px solid transparent;
            font-size: 13px;
            font-family: 'Segoe UI', sans-serif;
            font-weight: 500;
            min-width: 100px;
        }}
        QTabBar::tab:selected {{
            color: {theme['ACCENT']};
            border-bottom-color: {theme['ACCENT']};
            font-weight: 600;
        }}
        QTabBar::tab:hover:!selected {{
            color: {theme['TEXT_DARK']};
            background-color: {theme['BG_ELEVATED']};
        }}

        /* ── PAGE HEADER ──────────────────────────────────────────────── */
        QFrame#pageHeader {{
            border-bottom: 1px solid {theme['SEPARATOR']};
        }}

        /* ── FORM CARD (tarjeta de formulario) ───────────────────────── */
        QFrame#formCard {{
            background-color: {theme['BG_CARD']};
            border: 1px solid {theme['BORDER']};
            border-radius: 12px;
        }}
        QFrame#terminalCard {{
            background-color: {theme['BG_BASE']};
            border: 1px solid {theme['BORDER']};
            border-radius: 10px;
        }}
        QFrame#terminalHeader {{
            background-color: {theme['BG_SURFACE']};
            border: none;
            border-bottom: 1px solid {theme['BORDER']};
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }}
        
        QStackedWidget#transferCard {{
            background-color: {theme['BG_CARD']};
            border-radius: 12px;
            border: 1px solid {theme['BORDER']};
        }}

        QFrame#modeToggleContainer {{
            background-color: {theme['BG_SURFACE']};
            border: 1px solid {theme['BORDER']};
            border-radius: 8px;
        }}

        /* ── INPUT GROUP (input + botón fusionado) ────────────────────── */
        QFrame#inputGroup {{
            background-color: {theme['BG_ELEVATED']};
            border: 1px solid {theme['BORDER']};
            border-radius: 6px;
        }}
        QFrame#inputGroup:hover {{
            border-color: {theme['TEXT_MUTED']};
        }}
        QFrame#inputGroup QComboBox,
        QFrame#inputGroup QLineEdit {{
            border: none;
            border-radius: 0;
            background: transparent;
            padding: 10px 12px;
        }}
        QFrame#inputGroup QComboBox:focus,
        QFrame#inputGroup QLineEdit:focus {{
            border: none;
            background: transparent;
        }}
        QPushButton#inputGroupBtn {{
            background-color: {theme['BG_SURFACE']};
            border: none;
            border-left: 1px solid {theme['BORDER']};
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
            border-top-left-radius: 0;
            border-bottom-left-radius: 0;
            color: {theme['TEXT_MUTED']};
            font-weight: 500;
            font-size: 12px;
            padding: 10px 16px;
            min-height: 18px;
        }}
        QPushButton#inputGroupBtn:hover {{
            background-color: {theme['BG_ELEVATED']};
            color: {theme['TEXT_DARK']};
        }}

        /* ── HERO BUTTON (acción principal destacada) ─────────────────── */
        .btn-primary-hero {{
            background-color: {theme['ACCENT']};
            border: none;
            border-radius: 8px;
            color: #FFFFFF;
            font-weight: 600;
            font-size: 14px;
            padding: 12px 28px;
            min-height: 22px;
        }}
        .btn-primary-hero:hover {{
            background-color: {theme['ACCENT_DARK']};
        }}
        .btn-primary-hero:pressed {{
            background-color: {theme['ACCENT_ALT']};
        }}
        .btn-primary-hero:disabled {{
            background-color: {theme['BORDER']};
            color: {theme['TEXT_HINT']};
        }}

        .btn-warning-hero {{
            background-color: {theme['WARNING']};
            border: none;
            border-radius: 8px;
            color: #FFFFFF;
            font-weight: 600;
            font-size: 14px;
            padding: 12px 28px;
            min-height: 22px;
        }}
        .btn-warning-hero:hover {{
            background-color: #B07D15;
        }}
        .btn-warning-hero:pressed {{
            background-color: #8C6411;
        }}
        
        .btn-success-hero {{
            background-color: {theme['SUCCESS']};
            border: none;
            border-radius: 8px;
            color: #FFFFFF;
            font-weight: 600;
            font-size: 14px;
            padding: 12px 28px;
            min-height: 22px;
        }}
        .btn-success-hero:hover {{
            background-color: #329940;
        }}
        .btn-success-hero:pressed {{
            background-color: #298235;
        }}

        .btn-info-hero {{
            background-color: {theme['INFO']};
            border: none;
            border-radius: 8px;
            color: #FFFFFF;
            font-weight: 600;
            font-size: 14px;
            padding: 12px 28px;
            min-height: 22px;
        }}
        .btn-info-hero:hover {{
            background-color: #4A8EE0;
        }}
        .btn-info-hero:pressed {{
            background-color: #3C75BA;
        }}


        /* ── BOTONES DE MODO DE TRANSFERENCIA ───────────────────────── */
        QPushButton[transferMode="active"] {{
            background-color: {theme['ACCENT']};
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 0 24px;
            font-weight: 600;
        }}
        QPushButton[transferMode="inactive"] {{
            background-color: transparent;
            color: {theme['TEXT_MUTED']};
            border: none;
            border-radius: 6px;
            padding: 0 24px;
            font-weight: 500;
        }}
        QPushButton[transferMode="inactive"]:hover {{
            color: {theme['TEXT_LIGHT']};
        }}

        /* ── FORM LABEL (labels modernos, más pequeños) ───────────────── */
        .form-label {{
            color: {theme['TEXT_MUTED']};
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.3px;
            padding-bottom: 0px;
        }}

        /* ── FORM DIVIDER ─────────────────────────────────────────────── */
        .form-divider {{
            background-color: {theme['SEPARATOR']};
            border: none;
            max-height: 1px;
        }}
    """
