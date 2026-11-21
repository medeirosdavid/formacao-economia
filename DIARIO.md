# Diário do projeto — Formação em Economia

Registro curto de cada sessão: o que foi feito, decisões e pendências. Entradas mais recentes no topo.

## 21/11/2026 — Fundação do projeto

**Feito**

- Arquitetura definida: Quarto + GitHub, com três saídas (site, PDF e Anki).
- Currículo de 144 capítulos, da graduação ao doutorado, em 7 partes (`curriculo.yml`), com 5 trilhas de leitura.
- Esqueleto completo do livro:
  - perfis `site`/`pdf`;
  - macros de notação únicas para HTML e PDF;
  - caixas `tcolorbox` sóbrias no PDF e paleta equivalente no site;
  - filtros Lua para o PDF (referências a capítulos não escritos, caixas da ficha e do cabeçalho);
  - pacote `formacao` (dados do BCB/IBGE com cache e estilo gráfico);
  - exportação para o Anki;
  - workflow de publicação no GitHub Pages.
- Apêndices: *Notação e convenções*, *Guia de autoria*, *Fontes de dados brasileiros*.
- Capítulo-piloto **ECM-G01 Regressão linear simples** (status: rascunho):
  - teoria com 4 teoremas, 9 proposições/lemas e demonstrações completas;
  - 2 interativos em OJS (ajuste manual da reta; distribuição amostral de β̂₁);
  - laboratório (MQO do zero vs. `statsmodels`, Monte Carlo, Gauss–Markov na prática);
  - aplicação da lei de Okun com o SGS (24369, 22109);
  - 7 exercícios resolvidos, 11 flashcards, ficha-resumo.
- Verificação: site e PDF renderizados sem avisos; MathJax sem erros; interativos funcionando; o caminho dos dados foi testado com respostas simuladas da API.
- Repositório `medeirosdavid/formacao-economia` criado (**privado**, por decisão de David) e enviado.
- CI ajustada: cada *push* gera o site, o PDF e o baralho Anki como artefato **livro** da execução (aba *Actions*). O deploy no GitHub Pages fica desligado até existir a variável `PUBLICAR_PAGES = true`.

**Pendências**

- [ ] Conferir a primeira execução do GitHub Actions: o build deve passar e o artefato **livro** deve trazer os números reais da lei de Okun.
- [ ] Primeira renderização local com internet, para preencher `dados/cache/` e `_freeze/` e versioná-los.
- [ ] Revisar o ECM-G01: estilo, profundidade e exercícios. O resultado calibra todos os capítulos seguintes.
- [ ] Decidir por onde a revisão começa: base quantitativa (MAT/EST) ou econometria de graduação em sequência.
