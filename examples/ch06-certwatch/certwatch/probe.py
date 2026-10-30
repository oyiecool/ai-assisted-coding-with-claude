"""Connect to a host over TLS and report certificate expiry.

The network call is injectable (``connect``) so tests never touch the
network. All time arithmetic is in UTC.
"""
from __future__ import annotations

import os
import socket
import ssl
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime

from .parse import Target

# A connect function takes (host, port, timeout, verify) and returns the
# peer certificate in the dictionary form of ssl.SSLSocket.getpeercert().
Connector = Callable[[str, int, float, bool], dict]


@dataclass
class ProbeResult:
    target: Target
    days_left: int | None = None
    not_after: datetime | None = None
    subject: str = ""
    issuer: str = ""
    error: str = ""

    @property
    def ok(self) -> bool:
        return not self.error


def _name(rdns: tuple) -> str:
    """Flatten getpeercert()'s subject/issuer tuples to 'CN=x, O=y'."""
    short = {"commonName": "CN", "organizationName": "O", "countryName": "C"}
    parts = []
    for rdn in rdns:
        for key, value in rdn:
            parts.append(f"{short.get(key, key)}={value}")
    return ", ".join(parts)


def _decode_der(der: bytes) -> dict:
    """Decode a DER certificate into getpeercert() form.

    Used only with verification off, when getpeercert() returns an empty
    dict. Relies on CPython's private ssl._ssl._test_decode_cert, which is
    the only standard-library way to decode a certificate.
    """
    pem = ssl.DER_cert_to_PEM_cert(der)
    fd, path = tempfile.mkstemp(suffix=".pem")
    try:
        with os.fdopen(fd, "w") as handle:
            handle.write(pem)
        return ssl._ssl._test_decode_cert(path)  # type: ignore[attr-defined]
    finally:
        os.unlink(path)


def tls_connect(host: str, port: int, timeout: float, verify: bool) -> dict:
    """Real network connector. Reads the certificate; sends no data."""
    context = ssl.create_default_context()
    if not verify:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    with socket.create_connection((host, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=host) as tls:
            if verify:
                return tls.getpeercert()
            der = tls.getpeercert(binary_form=True)
            return _decode_der(der) if der else {}


def probe(
    target: Target,
    timeout: float = 5.0,
    verify: bool = True,
    connect: Connector = tls_connect,
    now: datetime | None = None,
) -> ProbeResult:
    """Probe one target. Never raises; failures are reported in .error."""
    now = now or datetime.now(UTC)
    try:
        cert = connect(target.host, target.port, timeout, verify)
    except (OSError, ssl.SSLError) as exc:
        return ProbeResult(target, error=f"{type(exc).__name__}: {exc}")
    if not cert or "notAfter" not in cert:
        return ProbeResult(target, error="no certificate returned")
    not_after = datetime.fromtimestamp(
        ssl.cert_time_to_seconds(cert["notAfter"]), tz=UTC
    )
    days_left = (not_after - now).days
    return ProbeResult(
        target,
        days_left=days_left,
        not_after=not_after,
        subject=_name(cert.get("subject", ())),
        issuer=_name(cert.get("issuer", ())),
    )
