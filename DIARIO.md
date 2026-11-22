# Diário do projeto — Formação em Economia

Registro curto de cada sessão: o que foi feito, decisões e pendências. Entradas mais recentes no topo.

## 22/11/2026 — MAT-G01 Lógica, conjuntos e métodos de demonstração

**Feito**

- Decisão: a revisão começa pela base quantitativa (trilha "Base quantitativa"), acompanhando o que David está estudando.
- ECM-G01 aprovado por David como padrão de estilo e profundidade.
- Skill `capitulo-formacao-economia` salva: roteiro fixo de cada sessão de estudo.
- Capítulo **MAT-G01** escrito (status: rascunho), com fonte principal em Morais Filho, *Um Convite à Matemática*:
  - lógica proposicional, quantificadores e técnicas de demonstração;
  - conjuntos, relações (equivalência ↔ partição; ordens; preferências racionais e dominância de Pareto) e funções (imagens e pré-imagens, inversa, utilidade ordinal);
  - indução e boa ordenação (soma geométrica e valor presente, Bernoulli, decomposição em primos);
  - cardinalidade (casa dos pombos; $\Z$, $\N\times\N$ e $\Q$ enumeráveis; teorema de Cantor; $\R$ não enumerável);
  - 3 interativos (tabelas-verdade, enumeração de $\N\times\N$, argumento diagonal), laboratório, 9 exercícios resolvidos, 15 flashcards e ficha-resumo.
- Infraestrutura:
  - novo controle `seletor` em `ojs/controles.js`;
  - no PDF, código e saídas quebram linhas longas (fvextra), a numeração ficou sem ponto final e o sumário passou a se chamar "Sumário";
  - `_freeze/` foi para o `.gitignore`;
  - convenção $\N = \{1, 2, \dots\}$ registrada na notação.

**Pendências**

- [ ] David revisar o MAT-G01 e apontar o que faltar em relação ao livro do Daniel Cordeiro.
- [ ] Próximo capítulo da trilha: definir com David (candidatos: MAT-G02 *Números reais, sequências e séries* ou MAT-G05 *Álgebra linear I*).

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
- Repositório `medeirosdavid/formacao-economia` criado e enviado; tornado **público** por David, para usar o GitHub Pages gratuito.
- CI: cada *push* gera o site, o PDF e o baralho Anki (artefato **livro** na aba *Actions*) e publica em https://medeirosdavid.github.io/formacao-economia/ quando o repositório é público.
- Interativos passaram a usar controles próprios (`ojs/controles.js`), sem depender de `@observablehq/inputs`.

**Pendências**

- [x] Pages ativado e site publicado (21/11).
- [ ] (Adiado por decisão de David) Ambiente local com Quarto.
- [x] ECM-G01 revisado e aprovado por David (22/11).
- [x] Começar pela base quantitativa (22/11).
