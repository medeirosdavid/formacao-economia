# Diário do projeto — Formação em Economia

Registro curto de cada sessão: o que foi feito, decisões e pendências. Entradas mais recentes no topo.

## 22/11/2026 — MAT-G02 e MAT-G03

**Feito**

- Capítulo **MAT-G02** *Números reais, sequências e séries* (status: rascunho), seguindo Lima (*Análise Real*, caps. 2–4) e Rudin (caps. 1 e 3):
  - axioma do supremo, propriedade arquimediana, parte inteira, densidade de $\Q$, existência de $\sqrt 2$;
  - limites de sequências, sequências monótonas (número $e$ com as sequências $(1+1/n)^n$ e $(1+1/n)^{n+1}$), recursão linear e estado estacionário;
  - subsequências, Bolzano–Weierstrass, limites superior e inferior, critério de Cauchy, sequências contrativas e ponto fixo de contrações em $\R$ (ponte para Banach/Bellman);
  - séries (geométrica, harmônica, $\sum 1/n^p$, comparação, absoluta, razão, Leibniz);
  - expansões decimais, cumprindo a promessa do MAT-G01 (unicidade exceto $\ldots 999 = \ldots 000$);
  - valor presente: perpetuidade, Gordon e fluxos limitados;
  - 3 interativos (definição ε–N, iteração linear, somas parciais), laboratório, 9 exercícios, 14 flashcards.
- Capítulo **MAT-G03** *Funções de uma variável: limites, continuidade e derivadas* (status: rascunho), seguindo Lima (caps. 6–9), Simon & Blume e Sydsæter:
  - limites ε–δ e caracterização por sequências; continuidade; exponencial e logaritmo admitidos (construção prometida para o MAT-G04, onde o tópico foi acrescentado);
  - valor intermediário, ponto fixo em dimensão 1, existência de preço de equilíbrio, continuidade da inversa, Weierstrass;
  - derivada pela formulação de Carathéodory (regras do produto, quociente, cadeia e inversa), capitalização contínua;
  - Fermat (promessa do MAT-G01), Rolle, valor médio, cotas para $\log(1+x)$;
  - Taylor com resto de Lagrange, $e^x$ e $\log 2$ como séries (promessas do MAT-G02), condição de segunda ordem;
  - concavidade (quatro caracterizações), máximo global, elasticidade, receita e regra de Lerner;
  - aplicação: IPCA mensal desde 1980 (SGS 433), soma das taxas × inflação acumulada exata;
  - 3 interativos (secante → tangente, polinômios de Taylor, elasticidade e receita), laboratório, 9 exercícios, 14 flashcards.
- Trilha "Base quantitativa": MAT-G02, MAT-G03 e MAT-G04 incluídos entre MAT-G01 e MAT-G05, a pedido de David.

**Pendências**

- [ ] David conferir, no site, os números da aplicação do IPCA (a sandbox não acessa o BCB; o código foi testado com dados simulados).
- [ ] David revisar MAT-G01, MAT-G02 e MAT-G03.
- [ ] Próximo capítulo da trilha: MAT-G04 *Integração e aplicações* (inclui a construção do logaritmo e da exponencial) ou MAT-G05 *Álgebra linear I*.

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
