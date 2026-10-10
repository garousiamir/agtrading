"""CLAUDE.md rule 13: no secret may appear in files committed to the repo.

Scans every tracked or untracked-but-not-ignored file. Later phases extend the
same detector to logs, database rows and JSON columns.

Sample secrets in the self-tests are assembled at runtime so that this file
never contains a literal match for its own patterns.
"""

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

SECRET_PATTERNS: dict[str, re.Pattern[str]] = {
    "private key block": re.compile(
        r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----"
    ),
    "age secret key": re.compile(r"AGE-SECRET-KEY-1[0-9A-Z]{50,}"),
    "AWS access key id": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "Anthropic API key": re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    "OpenAI-style key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9]{32,}"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})"),
    "Slack token": re.compile(r"\bxox[abposr]-[A-Za-z0-9\-]{10,}"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    "otpauth URI": re.compile(r"otpauth://t?otp/[^\s\"']*secret=[A-Z2-7]{16,}", re.IGNORECASE),
    # Exchange keys (Binance, Kraken, Coinbase, ...) have no fixed prefix, so
    # catch them when assigned to a credential-looking name.
    "credential assignment": re.compile(
        r"""(?ix)
        \b[\w.\-]*(?:api[_\-]?key|api[_\-]?secret|secret[_\-]?key|access[_\-]?key
            |private[_\-]?key|client[_\-]?secret|passphrase|password|passwd
            |auth[_\-]?token|access[_\-]?token|bearer|totp[_\-]?secret)[\w\-]*
        ["']?\s*[:=]\s*["']?
        (?P<value>[A-Za-z0-9+/_\-=.]{16,})
        """
    ),
}

PLACEHOLDER_HINTS = ("example", "placeholder", "changeme", "your", "dummy", "redacted", "xxxx")

MAX_FILE_BYTES = 5_000_000


def find_secrets(text: str) -> list[tuple[str, str]]:
    """Return (pattern name, matched text) for every suspected secret in text."""
    hits: list[tuple[str, str]] = []
    for name, pattern in SECRET_PATTERNS.items():
        for match in pattern.finditer(text):
            value = match.groupdict().get("value") or match.group(0)
            lowered = value.lower()
            if name == "credential assignment" and (
                any(hint in lowered for hint in PLACEHOLDER_HINTS) or len(set(value)) < 6
            ):
                continue
            hits.append((name, match.group(0)))
    return hits


def repo_files() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    ).stdout
    paths = [REPO_ROOT / p for p in out.decode().split("\0") if p]
    return [p for p in paths if p.is_file()]


def test_repo_contains_no_secrets() -> None:
    files = repo_files()
    assert files, "secret scan found no files; git ls-files returned nothing"
    findings = []
    for path in files:
        data = path.read_bytes()
        if len(data) > MAX_FILE_BYTES or b"\0" in data[:8192]:
            # Large or binary files are not expected in this repo; flag them
            # rather than silently skipping.
            findings.append(f"{path.relative_to(REPO_ROOT)}: binary or oversized file not scanned")
            continue
        for name, snippet in find_secrets(data.decode("utf-8", errors="replace")):
            shown = snippet[:12] + "..."  # never echo the full secret
            findings.append(f"{path.relative_to(REPO_ROOT)}: {name}: {shown}")
    assert not findings, "possible secrets found:\n" + "\n".join(findings)


def _fake(prefix: str, body_len: int, alphabet: str = "aB3dE5gH7jK9mN1pQ") -> str:
    body = (alphabet * (body_len // len(alphabet) + 1))[:body_len]
    return prefix + body


@pytest.mark.parametrize(
    "sample",
    [
        "-----BEGIN " + "RSA PRIVATE KEY-----",
        "-----BEGIN " + "OPENSSH PRIVATE KEY-----",
        _fake("AKI" + "A", 16, "ABCDEFGHIJ0123456789"),
        _fake("sk-" + "ant-api03-", 40),
        _fake("gh" + "p_", 36),
        _fake("xox" + "b-", 24),
        _fake("AI" + "za", 35),
        _fake("AGE-SECRET-" + "KEY-1", 58, "QWERTYUIOPASDFGH0123456789"),
        "otpauth://totp/me?" + "secret=" + "JBSWY3DPEHPK3PXPJBSWY3DP",
        "BINANCE_API_" + 'SECRET = "' + _fake("", 64) + '"',
        "kraken_private_" + "key: " + _fake("", 88) + "==",
        '{"api' + 'Key": "' + _fake("", 32) + '"}',
        "DB_PASS" + "WORD=" + _fake("", 20),
    ],
)
def test_detector_flags_known_secret_shapes(sample: str) -> None:
    assert find_secrets(sample), f"detector missed: {sample[:20]}..."


@pytest.mark.parametrize(
    "sample",
    [
        "api_key = os.environ['BINANCE_API_KEY']",
        'API_KEY="your-api-key-here-please"',
        "password: changeme-changeme-changeme",
        "sha256 = 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
        "Argon2id passwords, TOTP mandatory",
        "api_key: <set in age-encrypted secrets file>",
    ],
)
def test_detector_ignores_benign_text(sample: str) -> None:
    assert not find_secrets(sample)
