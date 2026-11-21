"""Acesso a dados públicos brasileiros com cache local.

Toda série baixada é gravada em ``dados/cache/`` (versionado no Git). Assim:

* o livro renderiza de forma reprodutível mesmo sem internet;
* os números do texto só mudam quando você decide atualizar os dados
  (``atualizar=True`` ou variável de ambiente ``FORMACAO_ATUALIZAR_DADOS=1``).

Exemplos
--------
>>> from formacao import dados
>>> ipca = dados.sgs(433, inicio="2010-01-01")          # IPCA, variação % mensal
>>> u = dados.sgs(dados.SERIES["desocupacao"])           # PNAD Contínua
>>> tab = dados.sidra("t/1737/n1/all/v/63/p/last%2012")  # IPCA via SIDRA
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
import warnings
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
CACHE = RAIZ / "dados" / "cache"

URL_SGS = ("https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
           "?formato=json&dataInicial={ini}&dataFinal={fim}")
URL_SIDRA = "https://apisidra.ibge.gov.br/values/{caminho}"

#: Catálogo de séries do SGS usadas no livro (código → descrição no SGS).
#: Ao acrescentar uma série, confira o código em https://www3.bcb.gov.br/sgspub
SERIES: dict[str, int] = {
    "ipca": 433,             # IPCA — variação % mensal
    "selic_meta": 432,       # Meta Selic definida pelo Copom (% a.a.)
    "selic": 11,             # Taxa Selic diária (% a.d.)
    "desocupacao": 24369,    # Taxa de desocupação — PNAD Contínua (%), trimestre móvel
    "pib_dessaz": 22109,     # PIB trimestral, dessazonalizado, índice (média 1995 = 100)
    "pib_mensal": 4380,      # PIB mensal, valores correntes (R$ milhões)
    "ibcbr": 24363,          # IBC-Br, sem ajuste sazonal
    "ibcbr_dessaz": 24364,   # IBC-Br, com ajuste sazonal
}

JANELA_MAX_ANOS = 9  # a API do SGS recusa consultas com mais de 10 anos de intervalo


class DadosIndisponiveis(RuntimeError):
    """Não foi possível baixar a série e não há cópia em cache."""


# ------------------------------------------------------------------ utilidades
def _forcar_atualizacao(atualizar: bool) -> bool:
    return atualizar or os.environ.get("FORMACAO_ATUALIZAR_DADOS") == "1"


def _baixar_json(url: str, tentativas: int = 3, espera: float = 2.0):
    ultimo_erro: Exception | None = None
    for i in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json",
                                                       "User-Agent": "formacao-economia/1.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:          # janela sem observações
                return []
            ultimo_erro = e
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            ultimo_erro = e
        time.sleep(espera * (i + 1))
    raise DadosIndisponiveis(f"falha ao acessar {url}: {ultimo_erro}")


def _janelas(inicio: date, fim: date):
    atual = inicio
    while atual <= fim:
        prox = min(date(atual.year + JANELA_MAX_ANOS, atual.month, 1) - timedelta(days=1), fim)
        yield atual, prox
        atual = prox + timedelta(days=1)


# ------------------------------------------------------------------------ SGS
def _baixar_sgs(codigo: int, inicio: date, fim: date) -> pd.Series:
    registros = []
    for ini, fim_j in _janelas(inicio, fim):
        url = URL_SGS.format(codigo=codigo, ini=ini.strftime("%d/%m/%Y"),
                             fim=fim_j.strftime("%d/%m/%Y"))
        registros += _baixar_json(url)
    if not registros:
        raise DadosIndisponiveis(f"SGS {codigo}: nenhuma observação entre {inicio} e {fim}")
    df = pd.DataFrame(registros)
    s = pd.Series(pd.to_numeric(df["valor"], errors="coerce").values,
                  index=pd.to_datetime(df["data"], format="%d/%m/%Y"), name=f"sgs_{codigo}")
    return s[~s.index.duplicated()].sort_index()


def sgs(codigo: int | str, inicio: str = "1980-01-01", fim: str | None = None,
        atualizar: bool = False) -> pd.Series:
    """Série temporal do SGS/BCB, indexada por data.

    Parâmetros
    ----------
    codigo    código numérico do SGS ou chave de :data:`SERIES`
    inicio    primeira data desejada (AAAA-MM-DD)
    fim       última data desejada (padrão: hoje)
    atualizar ignora o cache e baixa de novo
    """
    if isinstance(codigo, str):
        codigo = SERIES[codigo]
    ini = pd.Timestamp(inicio).date()
    fim_d = pd.Timestamp(fim).date() if fim else date.today()
    arquivo = CACHE / f"sgs-{codigo}.csv"

    if arquivo.exists() and not _forcar_atualizacao(atualizar):
        s = pd.read_csv(arquivo, index_col=0, parse_dates=True).iloc[:, 0]
    else:
        try:
            s = _baixar_sgs(codigo, date(1980, 1, 1), date.today())
            CACHE.mkdir(parents=True, exist_ok=True)
            s.to_frame().to_csv(arquivo)
        except DadosIndisponiveis:
            if not arquivo.exists():
                raise
            warnings.warn(f"SGS {codigo}: sem acesso à API; usando a cópia em cache.")
            s = pd.read_csv(arquivo, index_col=0, parse_dates=True).iloc[:, 0]
    s.name = f"sgs_{codigo}"
    return s.loc[str(ini):str(fim_d)]


# ---------------------------------------------------------------------- SIDRA
def sidra(caminho: str, atualizar: bool = False) -> pd.DataFrame:
    """Consulta à API do SIDRA/IBGE.

    ``caminho`` é a parte da URL depois de ``/values/``, como montada na
    página de cada tabela em https://sidra.ibge.gov.br (aba "Links de
    compartilhamento" → "Parâmetros da API"). A primeira linha da resposta
    (cabeçalho) vira o nome das colunas.
    """
    chave = hashlib.sha1(caminho.encode()).hexdigest()[:12]
    arquivo = CACHE / f"sidra-{chave}.json"
    if arquivo.exists() and not _forcar_atualizacao(atualizar):
        bruto = json.loads(arquivo.read_text(encoding="utf-8"))
    else:
        try:
            bruto = _baixar_json(URL_SIDRA.format(caminho=caminho))
            CACHE.mkdir(parents=True, exist_ok=True)
            arquivo.write_text(json.dumps(bruto, ensure_ascii=False), encoding="utf-8")
        except DadosIndisponiveis:
            if not arquivo.exists():
                raise
            warnings.warn("SIDRA: sem acesso à API; usando a cópia em cache.")
            bruto = json.loads(arquivo.read_text(encoding="utf-8"))
    cabecalho, *linhas = bruto
    df = pd.DataFrame(linhas).rename(columns=cabecalho)
    if "Valor" in df:
        df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
    return df


# ------------------------------------------------------------ transformações
def trimestral(s: pd.Series, como: str = "ultimo") -> pd.Series:
    """Converte uma série mensal em trimestral (``ultimo`` ou ``media``)."""
    r = s.resample("QE")
    out = r.last() if como == "ultimo" else r.mean()
    out.index = out.index.to_period("Q")
    return out
