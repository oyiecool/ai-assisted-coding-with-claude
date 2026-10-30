-- Size table columns by their content instead of giving every column the
-- same width. Each column first gets enough room for its longest single
-- word (which cannot wrap); the remaining width is shared in proportion to
-- how much text each column holds, capped so one column cannot take all.
--
-- LINE_CHARS is roughly how many characters of table text (\small Pagella)
-- fit across the text block of the A4 layout in header.tex.
local LINE_CHARS, PAD, CAP, TOTAL = 95, 5, 60, 0.98

local function stats(cell)
  local text = pandoc.utils.stringify(cell.contents)
  local word = 0
  for w in text:gmatch("%S+") do word = math.max(word, utf8.len(w) or #w) end
  return math.min(utf8.len(text) or 0, CAP), word
end

function Table(tbl)
  local n = #tbl.colspecs
  if n < 2 then return nil end
  local textlen, wordlen = {}, {}
  for i = 1, n do textlen[i], wordlen[i] = 1, 1 end
  local function scan(rows)
    for _, row in ipairs(rows) do
      for i, cell in ipairs(row.cells) do
        if i <= n then
          local t, w = stats(cell)
          textlen[i] = math.max(textlen[i], t)
          wordlen[i] = math.max(wordlen[i], w)
        end
      end
    end
  end
  scan(tbl.head.rows)
  for _, body in ipairs(tbl.bodies) do scan(body.body) end

  local mins, minsum, extra, extrasum = {}, 0, {}, 0
  for i = 1, n do
    mins[i] = (wordlen[i] + PAD) / LINE_CHARS
    minsum = minsum + mins[i]
    extra[i] = math.max(textlen[i] - wordlen[i], 0)
    extrasum = extrasum + extra[i]
  end
  local spare = math.max(TOTAL - minsum, 0)
  local scale = minsum > TOTAL and TOTAL / minsum or 1
  for i = 1, n do
    local share = extrasum > 0 and spare * extra[i] / extrasum or spare / n
    tbl.colspecs[i] = { tbl.colspecs[i][1], mins[i] * scale + share }
  end
  return tbl
end
