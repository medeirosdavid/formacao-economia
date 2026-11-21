"""Pacote de apoio aos laboratórios do livro *Formação em Economia*.

Módulos
-------
dados     acesso às APIs públicas brasileiras (BCB/SGS, IBGE/SIDRA) com cache local
graficos  estilo gráfico comum a todos os capítulos
"""
from . import dados, graficos  # noqa: F401

__all__ = ["dados", "graficos"]
