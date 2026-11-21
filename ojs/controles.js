// Controles dos interativos (OJS) sem depender de @observablehq/inputs:
// funcionam em qualquer hospedagem, inclusive com política de segurança restrita.
// Uso numa célula {ojs}:
//   import {controle, alternador} from "/ojs/controles.js"
//   viewof a = controle("rótulo", [0, 1], {valor: 0.5, passo: 0.01, casas: 2})
//   viewof b = alternador("rótulo", {valor: false})

export function controle(rotulo, [min, max], {valor = min, passo = 1, casas} = {}) {
  const form = document.createElement("form");
  form.className = "controle";
  const nome = document.createElement("span");
  nome.className = "controle-rotulo";
  nome.textContent = rotulo;
  const input = document.createElement("input");
  Object.assign(input, {type: "range", min, max, step: passo, value: valor});
  const saida = document.createElement("output");
  const fmt = v => (casas === undefined ? String(+v) : (+v).toFixed(casas)).replace(".", ",");
  saida.textContent = fmt(valor);
  form.append(nome, input, saida);
  form.value = +valor;
  input.addEventListener("input", () => { form.value = +input.value; saida.textContent = fmt(input.value); });
  form.addEventListener("submit", e => e.preventDefault());
  return form;
}

export function alternador(rotulo, {valor = false} = {}) {
  const form = document.createElement("form");
  form.className = "controle controle-alternador";
  const label = document.createElement("label");
  const input = document.createElement("input");
  input.type = "checkbox";
  input.checked = valor;
  label.append(input, document.createTextNode(" " + rotulo));
  form.append(label);
  form.value = valor;
  input.addEventListener("input", () => { form.value = input.checked; });
  form.addEventListener("submit", e => e.preventDefault());
  return form;
}
