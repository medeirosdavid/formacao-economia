--[[
caixas-pdf.lua — divs com classes de estilo que, no HTML, são formatadas
pelo CSS (estilos/tema.scss) e, no PDF, viram caixas tcolorbox definidas em
tex/preambulo.tex.
]]

local CAIXAS = {
  ["ficha-resumo"] = "caixaficha",
  ["cabecalho-capitulo"] = "caixacabecalho",
}

function Div(el)
  if not quarto.doc.is_format("latex") then return nil end
  for classe, ambiente in pairs(CAIXAS) do
    if el.classes:includes(classe) then
      local blocos = pandoc.List({ pandoc.RawBlock("latex", "\\begin{" .. ambiente .. "}") })
      blocos:extend(el.content)
      blocos:insert(pandoc.RawBlock("latex", "\\end{" .. ambiente .. "}"))
      return blocos
    end
  end
end
