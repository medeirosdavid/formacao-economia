#!/usr/bin/env python3
"""Exporta os flashcards do livro para um baralho do Anki (.apkg).

Um flashcard é um callout com a classe ``.flashcard``:

    ::: {.callout-note .flashcard collapse="true"}
    ## Pergunta (pode ter $\\LaTeX$)
    Resposta em Markdown, com matemática e macros do livro.
    :::

O script percorre ``partes/**/*.qmd``, converte cada cartão com o Pandoc
(expandindo as macros de ``tex/macros.tex``, que o Anki não conhece) e grava
``_anki/formacao-economia.apkg`` com um sub-baralho por capítulo:

    Formação em Economia::<Parte>::<código> <título>

Os identificadores são estáveis: reimportar o arquivo no Anki atualiza os
cartões existentes sem perder o histórico de revisões.

Uso:
    python scripts/flashcards_anki.py            # todos os capítulos
    python scripts/flashcards_anki.py ECM-G01    # só os capítulos indicados
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

import genanki
import yaml

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "_anki" / "formacao-economia.apkg"
ABRE = re.compile(r"^(:{3,})\s*\{(?P<attrs>[^}]*)\}\s*$")
FECHA = re.compile(r"^:{3,}\s*$")

MODELO = genanki.Model(
    1607392319,  # id fixo: não altere, ou o Anki criará um novo tipo de nota
    "Formação em Economia — Pergunta/Resposta",
    fields=[{"name": "Frente"}, {"name": "Verso"}, {"name": "Capitulo"}],
    templates=[{
        "name": "Cartão",
        "qfmt": '<div class="cap">{{Capitulo}}</div><div class="frente">{{Frente}}</div>',
        "afmt": '{{FrontSide}}<hr id="answer"><div class="verso">{{Verso}}</div>',
    }],
    css="""
.card { font-family: "Source Serif 4", Georgia, serif; font-size: 19px; line-height: 1.5;
        text-align: left; color: #1f2933; background: #fbfbfa; padding: 0 1em; }
.cap { font-family: sans-serif; font-size: 12px; color: #8a94a3; margin-bottom: .8em; }
.frente { font-weight: 600; }
.verso { margin-top: .6em; }
""",
)


def id_estavel(texto: str) -> int:
    return int(hashlib.sha1(texto.encode()).hexdigest()[:8], 16)


def extrair_cartoes(qmd: Path) -> list[tuple[str, str]]:
    """Devolve [(frente, verso)] em Markdown, na ordem do arquivo."""
    linhas = qmd.read_text(encoding="utf-8").splitlines()
    cartoes, i = [], 0
    while i < len(linhas):
        m = ABRE.match(linhas[i])
        if m and ".flashcard" in m.group("attrs"):
            prof, j, corpo = 1, i + 1, []
            while j < len(linhas) and prof > 0:
                if ABRE.match(linhas[j]):
                    prof += 1
                elif FECHA.match(linhas[j]):
                    prof -= 1
                    if prof == 0:
                        break
                corpo.append(linhas[j])
                j += 1
            titulo = re.search(r'title="([^"]*)"', m.group("attrs"))
            if titulo:
                frente, verso = titulo.group(1), corpo
            else:
                k = next((n for n, l in enumerate(corpo) if l.strip()), 0)
                frente, verso = re.sub(r"^#+\s*", "", corpo[k]).strip(), corpo[k + 1:]
            cartoes.append((frente, "\n".join(verso).strip()))
            i = j + 1
        else:
            i += 1
    return cartoes


def markdown_para_html(segmentos: list[str]) -> list[str]:
    """Converte vários trechos de Markdown numa única chamada ao Pandoc."""
    macros = (RAIZ / "tex" / "macros.tex").read_text(encoding="utf-8")
    macros = "\n".join(l for l in macros.splitlines() if l.startswith("\\newcommand"))
    marcador = "<!--CARTAO-{}-->"
    doc = macros + "\n\n" + "\n\n".join(f"{marcador.format(n)}\n\n{s}" for n, s in enumerate(segmentos))
    html = subprocess.run(["quarto", "pandoc", "-f", "markdown", "-t", "html", "--mathjax", "--wrap=none"],
                          input=doc, capture_output=True, text=True, check=True).stdout
    partes = re.split(r"<!--CARTAO-\d+-->", html)[1:]
    return [p.strip() for p in partes]


def main(filtro: list[str]) -> int:
    curriculo = yaml.safe_load((RAIZ / "curriculo.yml").read_text(encoding="utf-8"))
    titulo_livro = curriculo["titulo"]
    baralhos, total = [], 0
    for parte in curriculo["partes"]:
        for cap in parte["capitulos"]:
            if filtro and cap["id"] not in filtro:
                continue
            arquivos = sorted((RAIZ / "partes" / parte["pasta"]).glob(f"{cap['id'].lower()}-*.qmd"))
            if not arquivos:
                continue
            cartoes = extrair_cartoes(arquivos[0])
            if not cartoes:
                continue
            nome = f"{titulo_livro}::{parte['titulo']}::{cap['id']} {re.sub(r'[$]', '', cap['titulo'])}"
            baralho = genanki.Deck(id_estavel(nome), nome)
            html = markdown_para_html([s for par in cartoes for s in par])
            for n, (frente_md, _) in enumerate(cartoes):
                frente, verso = html[2 * n], html[2 * n + 1]
                baralho.add_note(genanki.Note(
                    model=MODELO, fields=[frente, verso, f"{cap['id']} · {cap['titulo']}"],
                    guid=genanki.guid_for(cap["id"], frente_md),
                    tags=[cap["id"], f"nivel-{cap['nivel']}", parte["id"]]))
            baralhos.append(baralho)
            total += len(cartoes)
            print(f"  {cap['id']}: {len(cartoes)} cartões")
    if not baralhos:
        print("Nenhum flashcard encontrado.")
        return 0
    SAIDA.parent.mkdir(exist_ok=True)
    genanki.Package(baralhos).write_to_file(SAIDA)
    print(f"{total} cartões em {len(baralhos)} baralho(s) → {SAIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
