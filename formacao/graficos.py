"""Estilo gráfico comum a todos os capítulos (mesma paleta do livro)."""
from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt

PALETA = {
    "azul": "#2F5D8A",      # definições / série principal
    "vinho": "#8C2F39",     # resultados / destaque
    "verde": "#2E7D5B",
    "ambar": "#B7791F",
    "ardosia": "#4A5568",
    "cinza": "#9AA5B1",
}


def estilo() -> None:
    """Aplica o estilo do livro ao matplotlib."""
    mpl.rcParams.update({
        "figure.figsize": (7.0, 4.0),
        "figure.dpi": 110,
        "axes.prop_cycle": mpl.cycler(color=list(PALETA.values())),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#e3e7ec",
        "grid.linewidth": 0.8,
        "axes.titlesize": 11,
        "axes.titleweight": "semibold",
        "axes.labelsize": 10,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "axes.formatter.use_locale": False,
        "savefig.bbox": "tight",
    })


def fonte(ax: plt.Axes, texto: str) -> None:
    """Escreve a nota de fonte no canto inferior esquerdo do gráfico."""
    ax.annotate(f"Fonte: {texto}", xy=(0, -0.16), xycoords="axes fraction",
                fontsize=8, color=PALETA["ardosia"], ha="left", va="top")
