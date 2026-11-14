# AGENTS.md

Instructions for AI coding agents working in this repository. This file is the single
source of truth for those instructions. `CLAUDE.md` imports it, and other agent
adapters must point back to it instead of copying it.

## What this repository contains

Application drivers for [Styrmin](https://docs.styrmin.app/). Each directory under
`drivers/` is one driver that a Styrmin operator loads with `styrminctl`:

```bash
styrminctl drivers load-version https://github.com/opsmill/styrmin-drivers.git main \
  --driver-directory drivers/<driver-name>
```

The drivers are copies of `driver/examples/` in
[opsmill/styrmin](https://github.com/opsmill/styrmin/tree/2d6aee04711a34eea3ea9ea3fac853ee898d2197/driver/examples).
They have not been deployed or tested from this repository. See `README.md` for the
preparation that db-test and simple-app need before deployment.

## Files in a driver directory

- `driver.styrmin.yml`: the driver specification (`apiVersion: styrmin.io/v1`,
  `kind: ApplicationDriver`). It declares the Helm chart, parameters, components,
  environment variables, services and actions.
- `values.j2.yml`: a Jinja2 template that Styrmin renders into the Helm values. It
  reads deployment data such as `app.version` and `services['<name>'].primary_fqdn`.
- `actions.py` (optional): Prefect flows for the lifecycle actions that the driver
  specification declares, for example `upgrade`, `pre_setup` and `post_setup`. The
  flows call helpers from `styrmin_backend.actions`.
- `src/` (only db-test and simple-app): the application source code, `Dockerfile` and
  Helm chart.

## Rules for changes

- The drivers contain fixed public credentials (admin passwords, database passwords,
  service tokens). Do not add new real credentials. Do not present the existing ones as
  safe for a real deployment.
- Known source issues are kept on purpose, for example simple-app's unauthenticated
  `/probe` endpoint and Slurpit's missing service and ingress wiring. Do not fix them
  silently. Say in the pull request when a change affects one.

## Agent layout

- `.agents/skills/`, `.agents/commands/`, `.agents/rules/`: shared skills, commands and
  rules for all agents. Add new content here.
- `.claude/skills`, `.claude/commands`, `.claude/rules`: symlinks to the matching
  `.agents/` directories. Do not add files to them directly.
