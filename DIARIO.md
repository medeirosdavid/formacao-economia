# Diário do projeto — Formação em Economia

Registro curto de cada sessão: o que foi feito, decisões e pendências. Entradas mais recentes no topo.

## 26/11/2026 — EST-G01 a EST-G06 (graduação de Probabilidade e Estatística)

**Feito** (seis capítulos, status rascunho, com referências padrão: DeGroot & Schervish, Casella & Berger e Bussab & Morettin)

- **EST-G01** *Probabilidade: axiomas, condicionamento e Bayes*:
  - axiomas de Kolmogorov e consequências, inclusão–exclusão por indução, continuidade da probabilidade;
  - contagem (Mega-Sena, aniversários, encontros $\to 1/e$), probabilidade condicional, regra do produto, probabilidade total;
  - Bayes e forma de razão de chances (sinal de recessão), independência dois a dois × mútua, independência condicional, ensaios repetidos;
  - aplicação: persistência das quedas do PIB (série 22109). Interativos: grade de frequências de Bayes e problema do aniversário.
- **EST-G02** *Variáveis aleatórias e distribuições*:
  - propriedades da função de distribuição, casos discreto, contínuo e misto, função quantil e VaR;
  - Bernoulli, binomial, geométrica (falta de memória), Poisson como limite da binomial, hipergeométrica;
  - uniforme, exponencial, normal, gama ($\Gamma(1/2) = \sqrt\pi$), log-normal, Pareto; teorema da transformação e transformada integral de probabilidade;
  - aplicação: distribuição da inflação mensal (IPCA, série 433) e contagens anuais pela binomial. Interativos: binomial × Poisson e método da inversa.
- **EST-G03** *Esperança, momentos e distribuições conjuntas*:
  - esperança, LOTUS, fórmula da cauda, momentos, FGM, Jensen (equivalente certo);
  - conjuntas, marginais e condicionais; covariância, variância da soma, correlação em $[-1, 1]$, diversificação;
  - esperança condicional, esperanças iteradas, variância total, melhor preditor; normal multivariada por combinações lineares e condicional normal;
  - aplicação: pares consecutivos do IPCA, esperança condicional por faixas contra a melhor previsão linear. Interativos: normal bivariada e Jensen.
- **EST-G04** *Amostragem e teoremas-limite*:
  - Markov, Chebyshev, LGN fraca, continuidade em probabilidade, consistência da variância amostral;
  - TCL demonstrado pela FGM, de Moivre–Laplace, Slutsky, estatística $t$ assintótica, método delta (lema de Carathéodory);
  - $\chi^2$, $t$ (densidade derivada) e $F$; teorema das amostras normais;
  - aplicação: reamostragem do IPCA para ver o TCL agir numa população assimétrica. Interativos: LGN (inclusive Pareto $\alpha = 1{,}5$ e Cauchy) e TCL.
- **EST-G05** *Estimação pontual e intervalar*:
  - viés, EQM, consistência; escore, informação de Fisher, Cramér–Rao demonstrado;
  - momentos e máxima verossimilhança (exemplos, invariância, normalidade assintótica);
  - intervalos: normal exato, Wald, Wilson, diferença de médias, baseado no EMV;
  - aplicação: inflação média em 2004–2008, 2010–2014 e 2017–2019, com erro padrão corrigido por AR(1). Interativos: cobertura de intervalos e verossimilhança.
- **EST-G06** *Testes de hipóteses*:
  - erros, tamanho, poder do teste $z$ e tamanho amostral; valor-p uniforme sob $H_0$ e más interpretações;
  - Neyman–Pearson demonstrado, teste UMP unilateral, razão de verossimilhança e Wilks (mencionado);
  - médias, proporções, variância combinada, Welch, pareado; dualidade testes–intervalos; testes múltiplos e Bonferroni;
  - aplicação: IPCA de 2017–2018 contra a meta de 4,5% e comparação entre períodos. Interativos: poder e histograma de valores-p.
- Cada capítulo tem laboratório, 8 exercícios resolvidos e 13–14 flashcards (81 cartões no total).
- Resultados admitidos (enunciados, com referência): unicidade da FGM (escalar e vetorial), continuidade de Lévy via FGM, Slutsky, LOTUS geral, troca de integrais (Tonelli), derivação sob o sinal de integral, LGN de Khinchin, mudança de variáveis multivariada (densidade da normal), normalidade assintótica do EMV, Wilks. Todos voltam com prova nos EST-M01 a EST-M05.
- As aplicações foram testadas na sandbox com séries sintéticas no formato do SGS (a API do BCB não é acessível daqui); os resumos em texto são gerados a partir dos dados, sem números fixos no texto.

**Pendências**

- [ ] David conferir no site as seis aplicações com dados reais (PIB 22109 e IPCA 433), em especial as frases geradas a partir dos dados.
- [ ] David revisar EST-G01 a EST-G06 (nível das provas, escolha dos resultados admitidos).
- [ ] Pendências anteriores continuam: revisar MAT-M01 e MAT-M10; conferir as aplicações do IPCA do MAT-G03 e MAT-G08; informar a fonte dos sumários.
- [ ] Próximos capítulos naturais: ECM-G02 *Regressão linear múltipla*, que agora tem toda a base de graduação, ou EST-M01 *Probabilidade com teoria da medida*, que paga as admissões acima.

## 24/11/2026 — MAT-M01 e MAT-M10

**Feito** (dois capítulos, status rascunho, com referências padrão e duas novas: Lima, *Espaços Métricos*, e Kreyszig)

- **MAT-M01** *Análise real em $\R^n$ e espaços métricos*:
  - métricas ($d_1$, $d_2$, $d_\infty$, discreta, supremo em $B(S)$, $d_1$ em $C[a, b]$); abertos, fechados, interior, fecho e fronteira;
  - topologia relativa, métricas equivalentes e uniformemente equivalentes, produtos; fecho por sequências;
  - completude: $\R^n$ e $B(S)$ completos, teorema da interseção de Cantor, completamento pelo mergulho de Kuratowski (com unicidade);
  - continuidade (quatro caracterizações), continuidade uniforme, Lipschitz, homeomorfismos (completude não é topológica), extensão de funções uniformemente contínuas;
  - compacidade: três caracterizações métricas (com número de Lebesgue), celas encaixadas, celas compactas por bisseção, Heine–Borel, Bolzano–Weierstrass, Heine–Cantor;
  - Weierstrass, existência da demanda, funções coercivas; conexidade, intervalos, valor intermediário, caminhos.
  - Interativos: bolas em quatro métricas (com a métrica ferroviária) e bisseção de Bolzano–Weierstrass.
- **MAT-M10** *Espaços normados e com produto interno*:
  - normas; Young, Hölder e Minkowski; produtos internos, Cauchy–Schwarz, lei do paralelogramo;
  - Banach $\iff$ séries absolutamente convergentes convergem; $\ell^p$ completo; exemplos incompletos ($c_{00}$, $C[0,1]$ com $\norm\cdot_1$, polinômios);
  - equivalência das normas em dimensão finita; lema de Riesz e bola compacta só em dimensão finita;
  - operadores limitados, norma de operador, $\mathcal L(X, Y)$ de Banach, derivação ilimitada; série de Neumann (generaliza Leontief);
  - aplicação: preço de um ativo numa cadeia de Markov com investidor neutro ao risco (números ilustrativos);
  - teorema da projeção (convexos completos), projeção sobre subespaços, complemento ortogonal, Gram–Schmidt, MQO como projeção, HJ como exercício.
  - Interativos: bolas de $\norm\cdot_p$ (inclusive $p < 1$) e projeção de funções sobre polinômios de Legendre.
- Cada capítulo tem laboratório, 9 exercícios resolvidos e 16 flashcards.
- Estrutura: macros `\inner`, `\diam`, `\interior`; MAT-M10 entra na trilha "Base quantitativa" (depois de MAT-M01) e vira pré-requisito de MAT-M08, que pode citar o teorema da projeção em vez de reprová-lo.
- Divisão de trabalho com MAT-M07: a completude de $B(S)$ ficou no MAT-M01; o MAT-M07 fica com $C_b$ fechado em $B(S)$, Dini, Arzelà–Ascoli e Bellman.
- Admissão nova: recíproca da lei do paralelogramo (Jordan–von Neumann), apenas mencionada.

**Pendências**

- [ ] David revisar MAT-M01 e MAT-M10, em especial o nível de detalhe das provas de compacidade.
- [ ] Pendências anteriores continuam: conferir a aplicação do IPCA do MAT-G08; informar a fonte dos sumários.
- [ ] Próximos capítulos naturais: MAT-M02 *Álgebra linear II* (critério de Sylvester, SVD) e MAT-M08 *Conjuntos convexos e separação*.

## 24/11/2026 — MAT-G04 a MAT-G08

**Feito** (cinco capítulos, status rascunho, com referências padrão: Lima, Rudin, Simon & Blume, Sydsæter, Strang, Sundaram)

- **MAT-G04** *Integração e aplicações*:
  - Darboux, integrabilidade de funções monótonas e contínuas (continuidade uniforme), propriedades e TFC;
  - logaritmo como integral e exponencial, cumprindo o que o MAT-G03 admitiu; substituição e partes;
  - integrais impróprias, teste da integral, constante de Euler–Mascheroni e função gama;
  - regra de Leibniz com limites variáveis e integral gaussiana;
  - excedentes e peso morto, valor presente contínuo e duration;
  - aplicação com curva de Lorenz e Gini calibrados ao Gini do IBGE (PNAD 2023).
- **MAT-G05** *Álgebra linear I*:
  - Cauchy–Schwarz e correlação; matrizes como transformações lineares;
  - eliminação de Gauss–Jordan, existência e unicidade, lema da troca, dimensão, posto linha = posto coluna, núcleo e imagem;
  - sete caracterizações da inversa; determinante pela fórmula de Leibniz, Laplace, Cramer;
  - Leontief com série de Neumann (matriz ilustrativa de três setores); mercados completos.
- **MAT-G06** *Cálculo em várias variáveis*:
  - derivada como aplicação linear e galeria de contraexemplos; $C^1$ implica diferenciável;
  - regra da cadeia, contabilidade do crescimento, valor médio e desigualdade do valor médio;
  - gradiente e TMS; Schwarz (e contraexemplo); Taylor de segunda ordem; Euler e esgotamento do produto;
  - Fubini no retângulo, demonstrado pela regra de Leibniz; mudança de variáveis admitida.
- **MAT-G07** *Otimização*:
  - CPO, formas quadráticas ($2 \times 2$ demonstrado; Sylvester admitido) e CSO;
  - concavidade e ótimos globais; MQO como otimização;
  - função implícita no plano (demonstrada), Lagrange ($n = 2$ demonstrado, geral enunciado), qualificação (cúspide);
  - multiplicador como preço sombra; hessiana orlada ($n = 2$ demonstrado);
  - consumidor, firma, carteira de variância mínima.
- **MAT-G08** *Equações em diferenças e diferenciais*:
  - primeira ordem, teia de aranha, solução para frente e bolhas; complexos e De Moivre (trigonometria admitida);
  - segunda ordem e triângulo de estabilidade (demonstrado); Samuelson;
  - EDOs de primeira e segunda ordem; sistemas $2 \times 2$ com autovalores; linearização; Solow;
  - aplicação: AR(1) da inflação mensal (IPCA, SGS 433, desde 2000).
- Cada capítulo tem 2 interativos, laboratório, 7 a 9 exercícios resolvidos e cerca de 14 flashcards.
- Admissões explícitas, para cumprir depois: funções trigonométricas; critério de Sylvester (MAT-M02); teorema de Lagrange geral e função implícita em $\R^n$ (MAT-M04); mudança de variáveis em integrais duplas (EST-M01); Picard–Lindelöf (MAT-M06).

**Pendências**

- [ ] David conferir, no site, os números da aplicação do IPCA do MAT-G08 (testada só com dados simulados).
- [ ] Saber de que livro ou notas são os sumários enviados, para incluí-los nas leituras.
- [ ] Próximos capítulos naturais: MAT-M01 *Análise real em $\R^n$ e espaços métricos* e MAT-M02 *Álgebra linear II* (que demonstra o critério de Sylvester).

## 24/11/2026 — Currículo confrontado com o sumário de um livro de análise para economistas

**Feito**

- Segundo sumário enviado por David (26 capítulos, de lógica a pontos fixos): 97 de 140 itens já cobertos, 16 parciais, 27 ausentes; a lacuna principal era a análise convexa.
- Novos capítulos planejados:
  - **MAT-M10** *Espaços normados e com produto interno* (entre MAT-M01 e MAT-M07; traz Banach e Hilbert para o mestrado);
  - **MAT-M08** *Conjuntos convexos e separação* (com Farkas e Gordan);
  - **MAT-M09** *Funções convexas e subdiferencial* (com Jensen).
- MAT-M03 passa a se chamar *Otimização com restrições de desigualdade e dualidade* (Fritz John, KKT, Slater, ponto de sela, dualidade, sensibilidade) e depende de MAT-M09. O nome do arquivo foi mantido, para não quebrar links.
- Tópicos acrescentados: MAT-M01 (topologia relativa, métricas equivalentes, completamento, Lipschitz, homeomorfismos, extensão de uniformemente contínuas), MAT-M07 (Dini, aproximação de Weierstrass, séries de potências), MAT-G06 (derivada como aplicação linear, direcionais, contraexemplos, $C^1$, desigualdade do valor médio, conjuntos de nível, Schwarz), MAT-G07 (qualificação de restrições), MAT-M04 (conjuntos de nível e espaço tangente), MAT-M05 (Sperner, Schauder), MAT-D04 (reorientado para $L^p$, duais e Riesz), EST-G03 (Jensen).
- Trilha "Base quantitativa": MAT-M08 e MAT-M09 antes de MAT-M03.
- Seções novas nos capítulos escritos:
  - MAT-G02: reta estendida; limites superior e inferior na reta estendida; equivalências da completude (cinco formas, com demonstração); rearranjos (Dirichlet e Riemann); séries de potências e raio de convergência; laboratório do rearranjo; 2 exercícios e 4 flashcards.
  - MAT-G03: descontinuidades de funções monótonas; valor médio de Cauchy e regra de L'Hôpital (0/0 e ∞/∞), com a utilidade CRRA convergindo para o logaritmo; laboratório; 2 exercícios e 2 flashcards.
- `gerar_estrutura.py`: esboços de capítulos planejados sem texto próprio passam a ser regenerados por inteiro (título e roteiro acompanham o currículo).
- Referências novas: Rockafellar (1970), Boyd e Vandenberghe (2004), Luenberger (1969).

## 24/11/2026 — Currículo confrontado com um sumário de Análise

**Feito**

- David enviou o sumário de um curso de Análise (pré-requisitos, $\R$ e $\R^n$, sequências, continuidade, diferenciação, sequências de funções) para conferir a cobertura do currículo: 19 de 26 itens já cobertos, 4 parciais, 3 ausentes.
- Novo capítulo **MAT-M07** *Sequências de funções: convergência uniforme e equicontinuidade* (planejado), entre MAT-M01 e MAT-M05; passa a ser pré-requisito de MAT-D02 (o operador de Bellman precisa da completude das funções limitadas com a norma do supremo) e de MAT-D04.
- Tópicos acrescentados: MAT-M01 (produto interno, normas e Cauchy–Schwarz; celas encaixadas, Bolzano–Weierstrass e Heine–Borel em $\R^n$), MAT-G06 (Taylor em várias variáveis), MAT-M04 (teorema da função inversa).
- MAT-G02: teorema dos intervalos encaixados, com demonstração, contraexemplos, flashcard e linha na ficha-resumo.

**Pendências**

- [ ] Saber de que livro ou notas é o sumário, para incluí-lo nas leituras.

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
