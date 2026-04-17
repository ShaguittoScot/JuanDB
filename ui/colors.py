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
    "ACCENT_SECONDARY": "#3B82F6", # Mismo que ACCENT para mantener color sólido

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

# Tema claro — Tailwind "Slate", sin contraste extremo
LIGHT_THEME = {
    "BG_BASE":      "#F1F5F9",  # Fondo principal más neutro (Slate 100)
    "BG_SIDEBAR":   "#F8FAFC",  # Sidebar suave (Slate 50)
    "BG_SIDEBAR2":  "#E2E8F0",  # Hover sidebar (Slate 200)
    "BG_CONTENT":   "#F1F5F9",
    "BG_SURFACE":   "#FFFFFF",  # Tarjetas y paneles en blanco limpio
    "BG_ELEVATED":  "#E2E8F0",  # Inputs y hover states
    "BG_CARD":      "#FFFFFF",

    "ACCENT":       "#2563EB",  # Azul moderno (Blue 600)
    "ACCENT_DARK":  "#1D4ED8",  # Hover (Blue 700)
    "ACCENT_ALT":   "#1E40AF",  # Pressed (Blue 800)
    "ACCENT_SOFT":  "#DBEAFE",  # Selectores / highlight list (Blue 100)
    "ACCENT_SECONDARY": "#2563EB", # Mismo que ACCENT

    "TEXT_LIGHT":   "#FFFFFF",  # Botones primarios
    "TEXT_DARK":    "#334155",  # Texto principal oscuro sin negro fuerte (Slate 700)
    "TEXT_MUTED":   "#64748B",  # Texto secundario (Slate 500)
    "TEXT_HINT":    "#94A3B8",  # Texto deshabilitado (Slate 400)

    "BORDER":       "#E2E8F0",  # Bordes sutiles (Slate 200)
    "SEPARATOR":    "#CBD5E1",  # Separadores (Slate 300)
    "BORDER_FOCUS": "#3B82F6",

    "ERROR":        "#EF4444",
    "SUCCESS":      "#10B981",
    "WARNING":      "#F59E0B",
    "INFO":         "#3B82F6",
}

# Tema Cyberpunk — Morados profundos y rosa neón
CYBERPUNK_THEME = {
    "BG_BASE":      "#0B0813",  # Fondo base ultra oscuro
    "BG_SIDEBAR":   "#0B0813",
    "BG_SIDEBAR2":  "#1A0B2E",  # Hover sidebar con tinte morado
    "BG_CONTENT":   "#0B0813",
    "BG_SURFACE":   "#140B24",  # Tarjetas y paneles (morado profundo)
    "BG_ELEVATED":  "#1F1433",  # Inputs y hover states
    "BG_CARD":      "#140B24",

    "ACCENT":       "#FF007C",  # Rosa neón vibrante
    "ACCENT_DARK":  "#D40068",  # Rosa oscuro (hover)
    "ACCENT_ALT":   "#BD005C",  # Rosa fuerte (pressed)
    "ACCENT_SOFT":  "#330022",  # Fondo rosa muy sutil
    "ACCENT_SECONDARY": "#7A1BAF", # Púrpura eléctrico (para gradientes)

    "TEXT_LIGHT":   "#FFFFFF",
    "TEXT_DARK":    "#FFFFFF",  # Texto blanco puro para alto contraste
    "TEXT_MUTED":   "#A0A0C0",  # Lavanda grisáceo
    "TEXT_HINT":    "#6A6A8C",

    "BORDER":       "#332244",  # Bordes morados suaves
    "SEPARATOR":    "#221133",
    "BORDER_FOCUS": "#FF007C",  # Rosa neón al foco

    "ERROR":        "#FF0033",  # Rojo neón
    "SUCCESS":      "#00FF9F",  # Verde aqua / Spring Green
    "WARNING":      "#FFBF00",  # Ámbar neón
    "INFO":         "#00D1FF",  # Cyan neón
}