# P12 Hardening Summary

- Dockerfile: pinned base image tags and non-root runtime user already configured.
- Docker Compose: port bindings restricted to 127.0.0.1 and secrets externalized via env vars.
- IaC (K8s): non-root, seccomp, dropped capabilities, read-only root FS, resource limits.
