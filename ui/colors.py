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