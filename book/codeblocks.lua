function CodeBlock(el)
  return pandoc.RawBlock('latex',
    '\\begin{codebox}\n\\begin{Verbatim}\n' .. el.text .. '\n\\end{Verbatim}\n\\end{codebox}')
end
