# ── JuanDB Design System — Professional Dark Theme ───────────────────────────
# Inspirado en: DataGrip, Beekeeper Studio, Linear App
# Paleta base: GitHub Dark + Blue accent

DARK_THEME = {
    # Fondos
    "BG_BASE":      "#0D1117",  # Fondo base de toda la ventana
    "BG_SIDEBAR":   "#0D1117",  # Sidebar igual al base
    "BG_SIDEBAR2":  "#161B22",  # Hover y elementos en sidebar
    "BG_CONTENT":   "#0D1117",  # Área de contenido
    "BG_SURFACE":   "#161B22",  # Cards, panels
    "BG_ELEVATED":  "#1C2333",  # Inputs, dropdowns, hover
    "BG_CARD":      "#161B22",

    # Acento principal — Azul profesional
    "ACCENT":       "#3B82F6",  # Azul primario
    "ACCENT_DARK":  "#2563EB",  # Hover del acento
    "ACCENT_ALT":   "#1D4ED8",  # Pressed
    "ACCENT_SOFT":  "#1E3A5F",  # Fondo suave con tinte azul

    # Texto
    "TEXT_LIGHT":   "#F0F6FC",  # Texto principal
    "TEXT_DARK":    "#F0F6FC",  # Alias (compatibilidad)
    "TEXT_MUTED":   "#7D8590",  # Texto secundario / labels
    "TEXT_HINT":    "#484F58",  # Texto deshabilitado / hints

    # Bordes
    "BORDER":       "#30363D",  # Borde estándar
    "SEPARATOR":    "#21262D",  # Separadores finos
    "BORDER_FOCUS": "#3B82F6",  # Borde en foco (= ACCENT)

    # Estado
    "ERROR":        "#F85149",
    "SUCCESS":      "#3FB950",
    "WARNING":      "#D29922",
    "INFO":         "#58A6FF",
}

# Tema claro — mismo sistema, colores invertidos
LIGHT_THEME = {
    "BG_BASE":      "#F6F8FA",
    "BG_SIDEBAR":   "#FFFFFF",
    "BG_SIDEBAR2":  "#F0F2F4",
    "BG_CONTENT":   "#F6F8FA",
    "BG_SURFACE":   "#FFFFFF",
    "BG_ELEVATED":  "#F0F2F4",
    "BG_CARD":      "#FFFFFF",

    "ACCENT":       "#0969DA",
    "ACCENT_DARK":  "#0550AE",
    "ACCENT_ALT":   "#033D8B",
    "ACCENT_SOFT":  "#DDF4FF",

    "TEXT_LIGHT":   "#FFFFFF",
    "TEXT_DARK":    "#1F2328",
    "TEXT_MUTED":   "#656D76",
    "TEXT_HINT":    "#9198A1",

    "BORDER":       "#D0D7DE",
    "SEPARATOR":    "#E8EAED",
    "BORDER_FOCUS": "#0969DA",

    "ERROR":        "#D1242F",
    "SUCCESS":      "#1A7F37",
    "WARNING":      "#9A6700",
    "INFO":         "#0969DA",
}