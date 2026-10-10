"""Apply ordered SQL migrations from migrations/.

Phase 0: no migrations and no database exist yet, so this only lists what it
finds. Applying them against PostgreSQL is added with the first migration.
"""

import sys
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "migrations"


def main() -> int:
    migrations = sorted(MIGRATIONS_DIR.glob("*.sql"))
    if not migrations:
        print("migrate: no migrations to apply")
        return 0
    print(f"migrate: found {len(migrations)} migration(s) but no runner is configured yet")
    return 1


if __name__ == "__main__":
    sys.exit(main())
