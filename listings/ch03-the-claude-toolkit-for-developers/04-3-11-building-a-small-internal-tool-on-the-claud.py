"""pr_summary.py — draft a reviewer summary of the current branch's diff."""
import subprocess
import anthropic

SYSTEM = (
    "You summarise code changes for reviewers. Be factual and brief. "
    "Sections: Purpose (inferred), Changes by file, Risks, What to review "
    "hardest. If intent is unclear, say so. Never invent behaviour that "
    "is not visible in the diff."
)

def main(base: str = "origin/main") -> None:
    diff = subprocess.run(
        ["git", "diff", f"{base}...HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout
    if not diff.strip():
        print("No changes.")
        return
    if len(diff) > 200_000:
        raise SystemExit("Diff too large to summarise; split the PR.")

    client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY
    msg = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1500,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"<diff>\n{diff}\n</diff>"}],
    )
    print(msg.content[0].text)

if __name__ == "__main__":
    main()
