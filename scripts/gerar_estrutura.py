#!/usr/bin/env python3
"""Gera a estrutura do livro a partir de curriculo.yml.

O que faz (sempre de forma idempotente — só grava arquivos que mudaram):
  1. valida o currículo (ids únicos, pré-requisitos existentes, ausência de
     ciclos, chaves bibliográficas presentes em referencias.bib);
  2. cria o esboço de cada capítulo que ainda não existe (NUNCA sobrescreve
     texto escrito);
  3. atualiza o bloco de cabeçalho de cada capítulo (nível, status,
     pré-requisitos, leituras), delimitado pelos marcadores
     <!-- cabecalho:inicio --> … <!-- cabecalho:fim -->;
  4. gera as páginas de abertura das partes, o mapa do curso (plano.qmd),
     o PLANO.md da raiz, as listas de capítulos de cada perfil
     (_quarto-site.yml e _quarto-pdf.yml) e _capitulos.json (usado pelo
     filtro filtros/refs-pendentes.lua no PDF).

Uso:
    python scripts/gerar_estrutura.py            # gera e relata
    python scripts/gerar_estrutura.py --checar   # só valida
    python scripts/gerar_estrutura.py --silencioso
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
CURRICULO = RAIZ / "curriculo.yml"
BIB = RAIZ / "referencias.bib"
PARTES_DIR = RAIZ / "partes"

STATUS_VALIDOS = ["planejado", "rascunho", "revisao", "completo"]
STATUS_ROTULO = {"planejado": "planejado", "rascunho": "rascunho",
                 "revisao": "em revisão", "completo": "completo"}
STATUS_ICONE = {"planejado": "○", "rascunho": "◔", "revisao": "◑", "completo": "●"}
MARCA_INI = "<!-- cabecalho:inicio — gerado por scripts/gerar_estrutura.py a partir de curriculo.yml; não edite à mão -->"
MARCA_FIM = "<!-- cabecalho:fim -->"
AVISO_GERADO = "<!-- ARQUIVO GERADO por scripts/gerar_estrutura.py — edite curriculo.yml, não este arquivo -->"

APENDICES = ["apendices/notacao.qmd", "apendices/guia-de-autoria.qmd", "apendices/dados.qmd"]

# ----------------------------------------------------------------- utilitários
alterados: list[str] = []


def gravar(caminho: Path, conteudo: str) -> None:
    """Grava somente se o conteúdo mudou (evita laços no quarto preview)."""
    if caminho.exists() and caminho.read_text(encoding="utf-8") == conteudo:
        return
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(conteudo, encoding="utf-8")
    alterados.append(str(caminho.relative_to(RAIZ)))


def slug(texto: str, max_len: int = 60) -> str:
    texto = re.sub(r"\\[a-zA-Z]+", "", texto).replace("$", "")
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c)).lower()
    texto = re.sub(r"[^a-z0-9]+", "-", texto).strip("-")
    if len(texto) > max_len:
        texto = texto[:max_len].rsplit("-", 1)[0]
    return texto


def rotulo(cid: str) -> str:
    return "sec-" + cid.lower()


# -------------------------------------------------------------------- leitura
def carregar() -> dict:
    dados = yaml.safe_load(CURRICULO.read_text(encoding="utf-8"))
    for p_idx, parte in enumerate(dados["partes"], start=1):
        parte["numero"] = p_idx
        for cap in parte["capitulos"]:
            cap.setdefault("prereq", [])
            cap.setdefault("leituras", [])
            cap.setdefault("topicos", [])
            cap.setdefault("status", "planejado")
            cap["parte"] = parte
    return dados


def todos_capitulos(dados: dict) -> list[dict]:
    return [c for p in dados["partes"] for c in p["capitulos"]]


def caminho_capitulo(cap: dict) -> Path:
    pasta = PARTES_DIR / cap["parte"]["pasta"]
    existentes = sorted(pasta.glob(f"{cap['id'].lower()}-*.qmd"))
    if existentes:  # nome estável mesmo que o título mude
        return existentes[0]
    return pasta / f"{cap['id'].lower()}-{slug(cap['titulo'])}.qmd"


# ------------------------------------------------------------------ validação
def validar(dados: dict) -> list[str]:
    erros: list[str] = []
    caps = todos_capitulos(dados)
    ids = [c["id"] for c in caps]
    for cid, n in Counter(ids).items():
        if n > 1:
            erros.append(f"id duplicado: {cid}")
    conjunto = set(ids)
    chaves_bib = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", BIB.read_text(encoding="utf-8")))
    for c in caps:
        if not re.fullmatch(r"[A-Z]{3}-[GMD]\d{2}", c["id"]):
            erros.append(f"{c['id']}: id fora do padrão ÁREA-Nnn")
        elif c["id"][4] != c["nivel"]:
            erros.append(f"{c['id']}: nível '{c['nivel']}' não bate com o id")
        if c["status"] not in STATUS_VALIDOS:
            erros.append(f"{c['id']}: status inválido '{c['status']}'")
        for p in c["prereq"]:
            if p not in conjunto:
                erros.append(f"{c['id']}: pré-requisito inexistente {p}")
        for k in c["leituras"]:
            if k not in chaves_bib:
                erros.append(f"{c['id']}: chave bibliográfica ausente em referencias.bib: {k}")
    # ciclos (DFS)
    grafo = {c["id"]: c["prereq"] for c in caps}
    estado: dict[str, int] = {}

    def visita(n: str, pilha: list[str]) -> None:
        estado[n] = 1
        for m in grafo.get(n, []):
            if estado.get(m) == 1:
                erros.append("ciclo de pré-requisitos: " + " → ".join(pilha + [n, m]))
            elif m in grafo and estado.get(m) is None:
                visita(m, pilha + [n])
        estado[n] = 2

    for n in grafo:
        if estado.get(n) is None:
            visita(n, [])
    for t in dados.get("trilhas", []):
        for cid in t.get("capitulos", []):
            if cid not in conjunto:
                erros.append(f"trilha '{t['nome']}': capítulo inexistente {cid}")
    return erros


# ------------------------------------------------------ macros para o MathJax
def ler_macros(caminho: Path) -> dict[str, tuple[str, int]]:
    """Lê os \\newcommand de tex/macros.tex (com chaves balanceadas)."""
    texto = caminho.read_text(encoding="utf-8")
    macros: dict[str, tuple[str, int]] = {}
    for m in re.finditer(r"\\newcommand\{\\(\w+)\}(?:\[(\d)\])?\{", texto):
        ini, prof, j = m.end(), 1, m.end()
        while prof:
            prof += {"{": 1, "}": -1}.get(texto[j], 0)
            j += 1
        macros[m.group(1)] = (texto[ini:j - 1], int(m.group(2) or 0))
    return macros


def mathjax_macros() -> str:
    macros = ler_macros(RAIZ / "tex" / "macros.tex")
    itens = {k: (corpo if n == 0 else [corpo, n]) for k, (corpo, n) in macros.items()}
    return ("<!-- ARQUIVO GERADO por scripts/gerar_estrutura.py a partir de tex/macros.tex — não edite -->\n"
            "<script>\nwindow.MathJax = {tex: {macros: " + json.dumps(itens, ensure_ascii=False)
            + "}};\n</script>\n")


# ----------------------------------------------------------------- cabeçalhos
def no_pdf(cap: dict) -> bool:
    return cap["status"] != "planejado"


def bloco_cabecalho(cap: dict, por_id: dict) -> str:
    nivel = cap["nivel"]
    nome_nivel = {"G": "Graduação", "M": "Mestrado", "D": "Doutorado"}[nivel]
    status = STATUS_ROTULO[cap["status"]]

    def lista_prereq(para_pdf: bool) -> str:
        itens = []
        for pid in cap["prereq"]:
            alvo = por_id[pid]
            if para_pdf and not no_pdf(alvo):
                itens.append(f"*{alvo['titulo']}* ({pid})")
            else:
                itens.append(f"@{rotulo(pid)} (*{alvo['titulo']}*)")
        return "; ".join(itens) if itens else "nenhum"

    leituras = ", ".join(f"@{k}" for k in cap["leituras"]) or "—"
    linhas = [MARCA_INI, "::: {.cabecalho-capitulo}",
              f"[{nome_nivel}]{{.nivel .nivel-{nivel}}} · [{status}]{{.status}} · `{cap['id']}`", ""]
    pre_html, pre_pdf = lista_prereq(False), lista_prereq(True)
    if pre_html == pre_pdf:
        linhas += [f"**Pré-requisitos:** {pre_html}", ""]
    else:
        linhas += ["::: {.content-visible when-format=\"html\"}",
                   f"**Pré-requisitos:** {pre_html}", ":::", "",
                   "::: {.content-visible unless-format=\"html\"}",
                   f"**Pré-requisitos:** {pre_pdf}", ":::", ""]
    linhas += [f"**Leituras principais:** {leituras}", ":::", MARCA_FIM]
    return "\n".join(linhas)


def esboco(cap: dict, cab: str) -> str:
    topicos = "\n".join(f"{i}. {t}" for i, t in enumerate(cap["topicos"], 1)) or "1. (a definir)"
    return f"""# {cap['titulo']} {{#{rotulo(cap['id'])}}}

{cab}

::: {{.callout-note title="Capítulo em construção"}}
Roteiro planejado:

{topicos}
:::
"""


ESBOCO_CORPO = re.compile(
    r'\A\s*::: \{\.callout-note title="Capítulo em construção"\}\nRoteiro planejado:\n\n'
    r'(?:\d+\. [^\n]*\n)+:::\s*\Z')


def eh_esboco_intocado(texto: str) -> bool:
    """Verdadeiro se o arquivo é só o esboço gerado (título, cabeçalho e roteiro)."""
    if not texto.startswith("# ") or MARCA_FIM not in texto:
        return False
    return bool(ESBOCO_CORPO.match(texto.split(MARCA_FIM, 1)[1]))


def atualizar_capitulo(cap: dict, por_id: dict) -> Path:
    caminho = caminho_capitulo(cap)
    cab = bloco_cabecalho(cap, por_id)
    if not caminho.exists():
        gravar(caminho, esboco(cap, cab))
        return caminho
    texto = caminho.read_text(encoding="utf-8")
    if eh_esboco_intocado(texto):  # esboço sem texto próprio: título e roteiro seguem o currículo
        gravar(caminho, esboco(cap, cab))
        return caminho
    padrao = re.compile(re.escape(MARCA_INI.split(" — ")[0]) + r".*?" + re.escape(MARCA_FIM), re.S)
    if padrao.search(texto):
        novo = padrao.sub(lambda _: cab, texto, count=1)
    else:
        print(f"aviso: {caminho.relative_to(RAIZ)} não tem marcadores de cabeçalho; nada alterado.",
              file=sys.stderr)
        novo = texto
    gravar(caminho, novo)
    return caminho


# -------------------------------------------------------- páginas das partes
def pagina_parte(parte: dict, caminhos: dict) -> str:
    linhas = [f"# {parte['titulo']} {{.unnumbered}}", "", AVISO_GERADO, "",
              parte["descricao"], "",
              "::: {.content-visible when-format=\"html\"}",
              "| Código | Nível | Capítulo | Status |", "|:--|:--|:--|:--|"]
    for cap in parte["capitulos"]:
        arq = caminhos[cap["id"]].name
        linhas.append(f"| {cap['id']} | {cap['nivel']} | [{cap['titulo']}]({arq}) | "
                      f"{STATUS_ICONE[cap['status']]} {STATUS_ROTULO[cap['status']]} |")
    linhas += [":::", ""]
    return "\n".join(linhas)


# ------------------------------------------------------------- mapa do curso
def resumo_progresso(dados: dict) -> list[str]:
    linhas = ["| Parte | Capítulos | G | M | D | Escritos | Completos |",
              "|:--|--:|--:|--:|--:|--:|--:|"]
    tot = Counter()
    for p in dados["partes"]:
        caps = p["capitulos"]
        c = Counter(x["nivel"] for x in caps)
        escritos = sum(no_pdf(x) for x in caps)
        completos = sum(x["status"] == "completo" for x in caps)
        tot.update({"n": len(caps), "G": c["G"], "M": c["M"], "D": c["D"],
                    "e": escritos, "c": completos})
        linhas.append(f"| {p['titulo']} | {len(caps)} | {c['G']} | {c['M']} | {c['D']} | {escritos} | {completos} |")
    linhas.append(f"| **Total** | **{tot['n']}** | {tot['G']} | {tot['M']} | {tot['D']} | {tot['e']} | {tot['c']} |")
    return linhas


def trilhas(dados: dict, por_id: dict, link) -> list[str]:
    linhas = []
    for t in dados.get("trilhas", []):
        linhas += [f"### {t['nome']}", "", t["descricao"], ""]
        if "filtro_nivel" in t:
            ids = [c["id"] for c in todos_capitulos(dados) if c["nivel"] == t["filtro_nivel"]]
            linhas.append(f"{len(ids)} capítulos — ver as tabelas abaixo (nível {t['filtro_nivel']}).")
        else:
            for i, cid in enumerate(t["capitulos"], 1):
                c = por_id[cid]
                linhas.append(f"{i}. {STATUS_ICONE[c['status']]} {link(c)} `{cid}`")
        linhas.append("")
    return linhas


def plano(dados: dict, por_id: dict, caminhos: dict, para_quarto: bool) -> str:
    def link(c: dict) -> str:
        rel = caminhos[c["id"]].relative_to(RAIZ).as_posix()
        return f"[{c['titulo']}]({rel})"

    if para_quarto:
        cab = ["# Mapa do curso {.unnumbered}", "", AVISO_GERADO, "", "::: {.plano}"]
    else:
        cab = [AVISO_GERADO, "", f"# Plano mestre — {dados['titulo']}", "",
               f"*{dados['subtitulo']}*", ""]
    linhas = cab + [
        "Legenda de status: ○ planejado · ◔ rascunho · ◑ em revisão · ● completo. "
        "Níveis: **G** graduação · **M** mestrado · **D** doutorado.", "",
        "## Progresso", ""] + resumo_progresso(dados) + ["", "## Trilhas de leitura", ""]
    linhas += trilhas(dados, por_id, link)
    linhas += ["## Capítulos por parte", ""]
    for p in dados["partes"]:
        linhas += [f"### Parte {p['numero']} — {p['titulo']}", "", p["descricao"], "",
                   "| Código | Nível | Capítulo | Pré-requisitos | Status |",
                   "|:--|:--|:--|:--|:--|"]
        for c in p["capitulos"]:
            pre = ", ".join(c["prereq"]) or "—"
            linhas.append(f"| {c['id']} | {c['nivel']} | {link(c)} | {pre} | "
                          f"{STATUS_ICONE[c['status']]} {STATUS_ROTULO[c['status']]} |")
        linhas.append("")
    if para_quarto:
        linhas.append(":::")
    return "\n".join(linhas) + "\n"


# ------------------------------------------------------------ perfis do Quarto
def perfil(dados: dict, caminhos: dict, so_escritos: bool) -> str:
    cab = ["# " + AVISO_GERADO.strip("<!- >"),
           f"# Perfil {'pdf' if so_escritos else 'site'}: "
           + ("apenas capítulos com status diferente de 'planejado'." if so_escritos
              else "todos os capítulos, inclusive esboços."), ""]
    cfg: dict = {"book": {"chapters": ["index.qmd"]}}
    if not so_escritos:
        cfg["book"]["chapters"].append("plano.qmd")
    for p in dados["partes"]:
        caps = [c for c in p["capitulos"] if (no_pdf(c) or not so_escritos)]
        if not caps:
            continue
        cfg["book"]["chapters"].append({
            "part": f"partes/{p['pasta']}/index.qmd",
            "chapters": [caminhos[c["id"]].relative_to(RAIZ).as_posix() for c in caps]})
    cfg["book"]["chapters"].append("referencias.qmd")
    cfg["book"]["appendices"] = APENDICES
    if not so_escritos:
        cfg["book"]["sidebar"] = {"tools": [
            {"icon": "file-earmark-pdf", "href": "pdf/formacao-economia.pdf", "text": "PDF"},
            {"icon": "stack", "href": "formacao-economia.apkg", "text": "Baralho Anki"}]}
    else:
        cfg["project"] = {"output-dir": "_pdf"}
        cfg["book"]["output-file"] = "formacao-economia"
    # O bloco `format:` vem de _formato-html.yml / _formato-pdf.yml (edite lá).
    formato = (RAIZ / ("_formato-pdf.yml" if so_escritos else "_formato-html.yml")).read_text(encoding="utf-8")
    return ("\n".join(cab) + yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False, width=200)
            + "\n# ---- formato (copiado de " + ("_formato-pdf.yml" if so_escritos else "_formato-html.yml")
            + ")\n" + formato)


# ------------------------------------------------------------------- principal
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checar", action="store_true", help="apenas valida o currículo")
    ap.add_argument("--silencioso", action="store_true", help="só imprime erros")
    args = ap.parse_args()

    dados = carregar()
    erros = validar(dados)
    if erros:
        print("Erros no currículo:", *erros, sep="\n  ", file=sys.stderr)
        return 1
    if args.checar:
        print("Currículo válido.")
        return 0

    por_id = {c["id"]: c for c in todos_capitulos(dados)}
    caminhos = {c["id"]: atualizar_capitulo(c, por_id) for c in todos_capitulos(dados)}
    for p in dados["partes"]:
        gravar(PARTES_DIR / p["pasta"] / "index.qmd", pagina_parte(p, caminhos))
    gravar(RAIZ / "plano.qmd", plano(dados, por_id, caminhos, para_quarto=True))
    gravar(RAIZ / "PLANO.md", plano(dados, por_id, caminhos, para_quarto=False))
    gravar(RAIZ / "estilos" / "mathjax-macros.html", mathjax_macros())
    gravar(RAIZ / "_capitulos.json", json.dumps(
        {c["id"]: {"titulo": c["titulo"], "nivel": c["nivel"], "status": c["status"],
                   "no_pdf": no_pdf(c)} for c in por_id.values()},
        ensure_ascii=False, indent=1) + "\n")
    gravar(RAIZ / "_quarto-site.yml", perfil(dados, caminhos, so_escritos=False))
    gravar(RAIZ / "_quarto-pdf.yml", perfil(dados, caminhos, so_escritos=True))

    if not args.silencioso:
        n = len(por_id)
        escritos = sum(no_pdf(c) for c in por_id.values())
        print(f"{n} capítulos no currículo; {escritos} com texto (entram no PDF).")
        print(f"{len(alterados)} arquivo(s) criado(s) ou atualizado(s).")
        for a in alterados[:15]:
            print("  ·", a)
        if len(alterados) > 15:
            print(f"  · … e mais {len(alterados) - 15}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
