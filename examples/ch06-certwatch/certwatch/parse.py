"""Parse a hosts file: one host[:port] per line, # comments allowed."""
from __future__ import annotations

from dataclasses import dataclass

DEFAULT_PORT = 443


@dataclass(frozen=True)
class Target:
    host: str
    port: int = DEFAULT_PORT

    def __str__(self) -> str:
        host = f"[{self.host}]" if ":" in self.host else self.host
        return f"{host}:{self.port}"


def parse_line(line: str) -> Target | None:
    """Return a Target for one line, or None for blank and comment lines.

    Accepted forms: ``example.com``, ``example.com:8443``, ``[2001:db8::1]``
    and ``[2001:db8::1]:8443``. Raises ValueError for anything else.
    """
    text = line.split("#", 1)[0].strip()
    if not text:
        return None
    if text.startswith("["):
        end = text.find("]")
        if end == -1:
            raise ValueError(f"unclosed IPv6 bracket: {line.strip()!r}")
        host, rest = text[1:end], text[end + 1 :]
        if rest and not rest.startswith(":"):
            raise ValueError(f"unexpected text after IPv6 address: {line.strip()!r}")
        port_text = rest[1:] if rest else ""
    elif text.count(":") > 1:
        raise ValueError(f"IPv6 addresses must be in brackets: {line.strip()!r}")
    else:
        host, _, port_text = text.partition(":")
    if not host:
        raise ValueError(f"missing host: {line.strip()!r}")
    port = DEFAULT_PORT
    if port_text:
        if not port_text.isdigit() or not 1 <= int(port_text) <= 65535:
            raise ValueError(f"invalid port {port_text!r} in {line.strip()!r}")
        port = int(port_text)
    return Target(host, port)


def parse_hosts(text: str) -> list[Target]:
    """Parse a whole hosts file. Errors name the offending line number."""
    targets = []
    for number, line in enumerate(text.splitlines(), start=1):
        try:
            target = parse_line(line)
        except ValueError as exc:
            raise ValueError(f"line {number}: {exc}") from None
        if target is not None:
            targets.append(target)
    return targets
