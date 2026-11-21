--[[
refs-pendentes.lua — referências a capítulos que ainda não estão no PDF.

O PDF só inclui capítulos já escritos. Uma referência como @sec-ecm-m02 a um
capítulo ainda em esboço ficaria "?@sec-ecm-m02". Este filtro troca essas
referências por texto: "capítulo *Título* [ECM-M02]". No site (HTML), onde
todos os capítulos existem, nada muda.

A lista de capítulos vem de _capitulos.json, gerado por
scripts/gerar_estrutura.py a partir de curriculo.yml.
]]

local capitulos = nil

local function carregar()
  if capitulos then return capitulos end
  local dir = (quarto.project and quarto.project.directory) or "."
  local f = io.open(pandoc.path.join({ dir, "_capitulos.json" }), "r")
  if not f then
    capitulos = {}
    return capitulos
  end
  local texto = f:read("a")
  f:close()
  capitulos = pandoc.json.decode(texto, false)
  return capitulos
end

function Cite(el)
  if quarto.doc.is_format("html") then return nil end
  if #el.citations ~= 1 then return nil end
  local codigo = el.citations[1].id:match("^sec%-(%a%a%a%-[gmd]%d%d)$")
  if not codigo then return nil end
  local info = carregar()[codigo:upper()]
  if info == nil or info.no_pdf then return nil end
  local titulo = pandoc.read(info.titulo, "markdown").blocks[1].content
  return pandoc.Inlines({
    pandoc.Str("capítulo"), pandoc.Space(), pandoc.Emph(titulo),
    pandoc.Space(), pandoc.Str("[" .. codigo:upper() .. "]"),
  })
end
