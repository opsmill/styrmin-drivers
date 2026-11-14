# AGENTS.md

Instructions for AI coding agents working in this repository. This file is the single
source of truth for those instructions. `CLAUDE.md` imports it, and other agent
adapters must point back to it instead of copying it.

## What this repository contains

The application drivers for [Styrmin](https://docs.styrmin.app/). New drivers are added
here. Each directory under `drivers/` is one driver that a Styrmin operator loads with
`styrminctl`:

```bash
styrminctl drivers load-version https://github.com/opsmill/styrmin-drivers.git main \
  --driver-directory drivers/<driver-name>
```

See `README.md` for the preparation that db-test and simple-app need before deployment.

## Writing or changing a driver

Read [Create a driver](https://docs.styrmin.app/docs/drivers/creating-a-driver) before
you write or change a driver. It explains each part of the driver specification, the
Helm values template, lifecycle actions and parameters, and ends with a validation
checklist. [Load a driver](https://docs.styrmin.app/docs/drivers/loading-drivers)
explains how to load and reload a driver while you test it.

## Files in a driver directory

- `driver.styrmin.yml` (required): the driver specification (`apiVersion:
  styrmin.io/v1`, `kind: ApplicationDriver`). It declares the Helm chart, parameters,
  components, environment variables, services and actions.
- `values.j2.yml` (optional): a Jinja2 template that Styrmin renders into the Helm
  values. It reads deployment data such as `app.version` and
  `services['<name>'].primary_fqdn`.
- `actions.py` (required only when the specification declares actions): Prefect flows
  for the lifecycle actions, for example `upgrade`, `pre_setup` and `post_setup`. The
  flows call helpers from `styrmin_backend.actions`.
- `src/` (only db-test and simple-app): the application source code, `Dockerfile` and
  Helm chart.

## Rules for changes

- The drivers contain fixed public credentials (admin passwords, database passwords,
  service tokens). Do not add new real credentials. Do not present the existing ones as
  safe for a real deployment.
- `README.md` lists known issues, for example simple-app's unauthenticated `/probe`
  endpoint and Slurpit's missing service and ingress wiring. When a change fixes or
  affects one, update that list and say so in the pull request.

## Agent layout

- `.agents/skills/`, `.agents/commands/`, `.agents/rules/`: shared skills, commands and
  rules for all agents. Add new content here.
- `.claude/skills`, `.claude/commands`, `.claude/rules`: symlinks to the matching
  `.agents/` directories. Do not add files to them directly.
