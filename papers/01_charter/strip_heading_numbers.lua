-- Strip a leading authored "N. " prefix from heading text before LaTeX
-- emission. The charter's Markdown headings are hand-numbered (e.g.
-- "## 1. Purpose of This Charter"), but the Frontiers LaTeX class numbers
-- \section/\subsection headings automatically at compile time -- without
-- this filter, the authored number and the class's automatic number both
-- appear, double-numbering every heading.
function Header(el)
  if #el.content >= 2
      and el.content[1].t == "Str"
      and el.content[1].text:match("^%d+%.$")
      and el.content[2].t == "Space" then
    table.remove(el.content, 1)
    table.remove(el.content, 1)
  end
  return el
end
