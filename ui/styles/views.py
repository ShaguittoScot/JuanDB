def get_views_style(theme: dict) -> str:
    return f"""
        /* ── GLOBALES DE VISTAS ─────────────────────────────────── */
        BackupView, ImportExportView, SecurityView, MonitorView {{
            background-color: transparent;
        }}
        
        QLabel.label {{
            color: {theme['TEXT_MUTED']};
            font-size: 12px;
            font-weight: 500;
            min-width: 100px;
        }}
        
        QLabel.section-title {{
            color: {theme['ACCENT']};
            font-size: 13px;
            font-weight: bold;
            margin-top: 8px;
        }}
        
        /* ── INPUTS DE VISTAS ───────────────────────────────────── */
        QComboBox, QLineEdit {{
            background-color: {theme['BG_SIDEBAR2']};
            border: 1px solid {theme['BORDER']};
            border-radius: 8px;
            padding: 8px 12px;
            color: {theme['TEXT_LIGHT']};
            font-size: 12px;
            min-height: 20px;
        }}
        
        QComboBox:hover, QLineEdit:hover {{
            border-color: {theme['ACCENT']};
        }}
        
        QComboBox:focus, QLineEdit:focus {{
            border-color: {theme['ACCENT']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 24px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {theme['TEXT_LIGHT']};
            margin-right: 8px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {theme['BG_SIDEBAR2']};
            border: 1px solid {theme['BORDER']};
            selection-background-color: {theme['ACCENT']};
            color: {theme['TEXT_LIGHT']};
        }}
        
        /* ── AGRUPACIONES (Groupbox) ────────────────────────────── */
        QGroupBox {{
            border: 1px solid {theme['BORDER']};
            border-radius: 12px;
            margin-top: 12px;
            padding-top: 12px;
            font-weight: bold;
            color: {theme['TEXT_LIGHT']};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px;
        }}
        
        /* ── TABLAS ─────────────────────────────────────────────── */
        QTableWidget {{
            background-color: {theme['BG_SIDEBAR2']};
            border: 1px solid {theme['BORDER']};
            border-radius: 12px;
            color: {theme['TEXT_LIGHT']};
            gridline-color: {theme['BORDER']};
        }}
        
        QHeaderView::section {{
            background-color: {theme['BORDER']};
            color: {theme['TEXT_MUTED']};
            padding: 8px;
            border: none;
            font-weight: bold;
        }}
        
        /* ── CHECKBOX ───────────────────────────────────────────── */
        QCheckBox {{
            color: {theme['TEXT_MUTED']};
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 2px solid {theme['BORDER']};
            background-color: {theme['BG_SIDEBAR2']};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {theme['ACCENT']};
            border-color: {theme['ACCENT']};
        }}
        
        /* ── PROGRESS BAR ───────────────────────────────────────── */
        QProgressBar {{
            border: 1px solid {theme['BORDER']};
            border-radius: 6px;
            text-align: center;
            color: {theme['TEXT_LIGHT']};
            background-color: {theme['BG_SIDEBAR2']};
        }}
        
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {theme['ACCENT']}, stop:1 {theme['TEXT_MUTED']});
            border-radius: 5px;
        }}
        
        /* ── LOG AREA (QTextEdit#logArea) ───────────────────────── */
        QTextEdit#logArea {{
            background-color: {theme['BG_SIDEBAR']};
            border: 1px solid {theme['BORDER']};
            border-radius: 12px;
            padding: 12px;
            font-family: 'Consolas', monospace;
            font-size: 11px;
        }}
        
        /* ── BOTONES SECUNDARIOS ────────────────────────────────── */
        QPushButton#btnSecondary {{
            background-color: transparent;
            border: 1px solid {theme['BORDER']};
            border-radius: 8px;
            color: {theme['TEXT_MUTED']};
            padding: 8px 16px;
            font-size: 12px;
        }}
        
        QPushButton#btnSecondary:hover {{
            background-color: {theme['BORDER']};
            border-color: {theme['ACCENT']};
        }}
        
        /* ── UTILITY CLASSES PARA VISTAS ──────────────────────────── */
        .view-title {{
            color: {theme['TEXT_DARK']};
        }}
        .view-subtitle-accent {{
            color: {theme['ACCENT']};
        }}
        .view-subtitle-muted {{
            color: {theme['TEXT_MUTED']};
        }}
        .text-adaptive {{ color: {theme['TEXT_DARK']}; }}
        .text-light {{ color: {theme['TEXT_LIGHT']}; }}
        .text-accent {{ color: {theme['ACCENT']}; }}
        .text-muted {{ color: {theme['TEXT_MUTED']}; }}
        .text-error {{ color: {theme['ERROR']}; }}
        .text-success {{ color: {theme['SUCCESS']}; }}
        .text-warning {{ color: {theme['WARNING']}; }}
        .text-muted-11 {{ color: {theme['TEXT_MUTED']}; font-size: 11px; }}
        .text-hint {{ color: {theme['TEXT_DARK']}; font-size: 10px; margin-top: 8px; }}
        .text-footer {{ color: {theme['TEXT_DARK']}; padding: 8px; }}
        .desc-muted {{ color: {theme['TEXT_MUTED']}; font-size: 11px; margin-bottom: 8px; }}
        .status-indicator {{ color: {theme['ACCENT']}; font-size: 12px; }}
        
        .icon-20 {{ font-size: 20px; }}
        
        .view-container {{
            background-color: {theme['BG_SIDEBAR2']};
            border-radius: 16px;
        }}
        .view-container-small {{
            background-color: {theme['BG_SIDEBAR2']};
            border-radius: 12px;
        }}
        .options-frame {{
            background-color: {theme['BG_SIDEBAR']};
            border-radius: 8px;
            padding: 8px;
        }}
        .legend-container {{
            background-color: {theme['BG_SIDEBAR']};
            border-radius: 6px;
        }}
        .h-separator {{
            background-color: {theme['BORDER']};
            max-width: 1px;
        }}
        .v-gradient-divider {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {theme['ACCENT']}, stop:0.5 {theme['TEXT_MUTED']}, stop:1 {theme['ACCENT']});
            border-radius: 1px;
        }}
        .warning-box {{
            color: {theme['WARNING']};
            font-size: 10px;
            margin-top: 8px;
            background-color: {theme['BG_SIDEBAR']};
            padding: 8px;
            border-radius: 6px;
        }}
        
        
        .metric-card {{
            background-color: {theme['BG_SIDEBAR']};
            border-radius: 12px;
            border: 1px solid transparent;
        }}
        .metric-card:hover {{
            border-color: {theme['ACCENT']};
            background-color: {theme['BG_SIDEBAR2']};
        }}
        .icon-16-accent {{ font-size: 16px; color: {theme['ACCENT']}; }}
        
        .file-selector-input {{
            background-color: transparent;
            border: 1px solid {theme['BORDER']};
            border-radius: 8px;
            padding: 8px 12px;
            color: {theme['TEXT_LIGHT']};
            font-size: 12px;
        }}
        .file-selector-input:focus {{
            border-color: {theme['ACCENT']};
        }}
    
        /* BOTONES GENERICOS PRIMARIOS Y SECUNDARIOS */
        .btn-danger {{
            background-color: transparent;
            border: 1px solid {theme['ERROR']};
            color: {theme['ERROR']};
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 12px;
        }}
        .btn-danger:hover:enabled {{
            background-color: {theme['ERROR']};
            color: white;
        }}
        .btn-danger:disabled {{
            border-color: {theme['BORDER']};
            color: {theme['BORDER']};
        }}
        
        .status-panel {{
            background-color: {theme['BG_SIDEBAR2']};
            border-radius: 12px;
            border: 1px solid {theme['BORDER']};
        }}
        
        .icon-14 {{ font-size: 14px; }}

        .btn-primary {{
            background-color: {theme['ACCENT']};
            border: none;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            font-size: 14px;
            padding: 10px 24px;
        }}
        .btn-primary:hover {{
            background-color: {theme['ACCENT']}dd; /* Slightly transparent via hex? Better handled by opacity */
        }}
        .btn-primary:disabled {{
            background-color: {theme['BORDER']};
            color: {theme['TEXT_DARK']};
        }}
        
        .btn-secondary-animated {{
            background-color: transparent;
            border: 1px solid {theme['BORDER']};
            border-radius: 10px;
            color: {theme['TEXT_MUTED']};
            font-weight: bold;
            font-size: 14px;
            padding: 10px 24px;
        }}
        .btn-secondary-animated:hover {{
            border-color: {theme['ACCENT']};
            color: {theme['ACCENT']};
        }}
    """
