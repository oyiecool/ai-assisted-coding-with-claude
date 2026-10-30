"""Turn the exported doc markdown into book-structured markdown for pandoc."""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8").read().splitlines()

# 1. Drop the title block (everything before the Preface) and the Contents section.
start = next(i for i, line in enumerate(lines) if line.strip() == "## Preface")
lines = lines[start:]
c0 = next(i for i, line in enumerate(lines) if line.strip() == "## Contents")
c1 = next(i for i, line in enumerate(lines) if line.startswith("# Part I "))
lines = lines[:c0] + lines[c1:]

FIGS = {
    "agent loop": "fig-agent-loop",
    "core loop": "fig-core-loop",
    "security gates": "fig-security-gates",
}

out = []
in_fence = False
for line in lines:
    if line.startswith("```"):
        in_fence = not in_fence
        out.append(line)
        continue
    if in_fence:
        out.append(line)
        continue

    if "embedded content:" in line:
        key = next(k for k in FIGS if k in line)
        out += ["", "```{=latex}", f"\\input{{figures/{FIGS[key]}.tex}}", "```", ""]
        continue

    if line.strip() == "## Preface":
        out.append("## Preface {.unnumbered}")
        continue
    m = re.match(r"^# Part [IVX]+ — (.+)$", line)
    if m:
        if line.startswith("# Part I "):
            out += ["```{=latex}", "\\mainmatter", "```", ""]
        out.append(f"# {m.group(1)}")
        continue
    if line.strip() == "# Appendices":
        out += ["```{=latex}", "\\appendix", "\\bookpart{Appendices}", "```"]
        continue
    m = re.match(r"^## (?:Chapter \d+|Appendix [A-Z]) — (.+)$", line)
    if m:
        out.append(f"## {m.group(1)}")
        continue
    out.append(line)

open(dst, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("ok", len(out))
