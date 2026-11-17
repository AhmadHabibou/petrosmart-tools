"""Formatage des nombres a la francaise : espace insecable des milliers, virgule decimale."""
NBSP = " "


def nombre(x: float, decimales: int = 0) -> str:
    s = f"{x:,.{decimales}f}"
    return s.replace(",", NBSP).replace(".", ",")


def fcfa(x: float) -> str:
    return f"{nombre(x)}{NBSP}FCFA"


def m_fcfa(x: float, decimales: int = 2) -> str:
    """Montant exprime en millions de FCFA, sans l'unite (a mettre en en-tete)."""
    return nombre(x / 1e6, decimales)


def pct(x: float, decimales: int = 0) -> str:
    return f"{nombre(100 * x, decimales)}{NBSP}%"
