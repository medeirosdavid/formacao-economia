# Formação em Economia

*Macroeconomia, Finanças e Econometria — da graduação ao doutorado.*

Material de estudo e referência unificado, escrito em [Quarto](https://quarto.org). Um único texto-fonte gera:

- **site** com todos os capítulos (inclusive os esboços), busca, simulações interativas e código;
- **PDF** só com os capítulos já escritos, no estilo de caixas `tcolorbox`;
- **baralho do Anki** com os flashcards de todos os capítulos.

## Começando

```bash
# 1. Quarto (https://quarto.org/docs/get-started/) e uma distribuição TeX
quarto install tinytex          # se ainda não tiver LaTeX

# 2. Ambiente Python dos laboratórios
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Pré-visualização ao vivo do site
quarto preview
```

| Tarefa | Comando |
|:--|:--|
| validar o currículo | `python scripts/gerar_estrutura.py --checar` |
| criar esboços, atualizar cabeçalhos, listas e plano | `python scripts/gerar_estrutura.py` |
| renderizar o site | `quarto render` |
| renderizar o PDF | `quarto render --profile pdf --to pdf` |
| gerar o baralho do Anki | `python scripts/flashcards_anki.py` |
| atualizar os dados baixados | `FORMACAO_ATUALIZAR_DADOS=1 quarto render` |

## Estrutura

```
curriculo.yml            fonte única: partes, capítulos, nível, pré-requisitos, leituras, status
partes/<nn-area>/        um arquivo .qmd por capítulo (código-slug.qmd) + index.qmd da parte
apendices/               notação, guia de autoria, fontes de dados
tex/macros.tex           macros de notação (fonte única para PDF e site)
tex/preambulo.tex        caixas e estilo do PDF
estilos/tema.scss        estilo do site (mesma paleta do PDF)
_formato-html.yml        opções do site      ┐ copiadas para os perfis
_formato-pdf.yml         opções do PDF       ┘ pelo script de estrutura
formacao/                pacote Python dos laboratórios (dados do BCB/IBGE com cache, gráficos)
dados/cache/             séries baixadas (versionadas: o livro renderiza sem internet)
filtros/                 filtros Lua do PDF
scripts/                 geração da estrutura e exportação para o Anki
templates/capitulo.qmd   esqueleto-padrão de capítulo
```

Arquivos **gerados** pelo script (não edite à mão): `_quarto-site.yml`, `_quarto-pdf.yml`, `plano.qmd`, `PLANO.md`, `_capitulos.json`, `estilos/mathjax-macros.html`, `partes/*/index.qmd` e o bloco de cabeçalho de cada capítulo.

## Fluxo de trabalho

1. Escolha o capítulo em `curriculo.yml` (ou acrescente um novo tópico).
2. Redija seguindo `templates/capitulo.qmd` e o apêndice *Guia de autoria*.
3. Atualize o `status` (`planejado → rascunho → revisao → completo`) e rode o script de estrutura.
4. Faça *commit*; o GitHub Actions publica site, PDF e Anki.

## Publicação

O workflow `.github/workflows/publicar.yml` roda a cada *push*: renderiza o site, o PDF e o baralho do Anki, guarda tudo como artefato **livro** da execução (aba *Actions*) e, com o repositório público, publica no GitHub Pages:

- site: <https://medeirosdavid.github.io/formacao-economia/>
- PDF: <https://medeirosdavid.github.io/formacao-economia/pdf/formacao-economia.pdf>
- Anki: <https://medeirosdavid.github.io/formacao-economia/formacao-economia.apkg>

Pré-requisito, uma única vez: *Settings → Pages → Build and deployment → Source: GitHub Actions*. Se o repositório voltar a ser privado, a publicação para (a menos que a variável de repositório `PUBLICAR_PAGES` seja `true` e a conta tenha plano com Pages privado).

Os resultados do código ficam congelados em `_freeze/` (versione essa pasta depois da primeira renderização local) e as séries de dados em `dados/cache/`.
