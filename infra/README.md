# infra

Docker Compose files with `local` and `host` profiles (`APP_ENV=local|host`).
Added once there are services to run. The execution service will get its own
container and network policy (see `docs/01-decisions.md`, Hosting).
