# Styrmin drivers

The application drivers for [Styrmin](https://docs.styrmin.app/). A driver describes
how Styrmin installs, configures, backs up and upgrades one application: which Helm
chart to deploy, which settings an operator can change, and which actions to run during
the deployment lifecycle.

## Available drivers

| Driver | Application | Helm chart |
|--------|-------------|------------|
| `infrahub` | Infrahub | `oci://registry.opsmill.io/opsmill/chart/infrahub` 4.33.2 |
| `infrahub-enterprise` | Infrahub Enterprise | `oci://registry.opsmill.io/opsmill/chart/infrahub-enterprise` 4.19.2 |
| `infrahub-mcp` | Infrahub MCP server, for an existing Infrahub instance | `oci://registry.opsmill.io/opsmill/chart/infrahub-mcp` 0.1.0 |
| `semaphore` | Semaphore UI for Ansible, Terraform and other tools | `https://semaphoreui.github.io/charts/semaphore` 16.0.11 |
| `slurpit` | Slurpit network discovery and inventory | `oci://registry.opsmill.io/external/slurpit` 1.3.6 |
| `generic-app` | Any single-container HTTP application that listens on port 8080 ([documentation](https://docs.styrmin.app/docs/drivers/generic-app)) | `oci://ghcr.io/bjw-s-labs/helm/app-template` 5.2.1 |
| `simple-app` | Example FastAPI application with PostgreSQL | Built from `drivers/simple-app/src/` |
| `db-test` | Test application with MariaDB and MongoDB, for backup testing | Built from `drivers/db-test/src/` |

## Load a driver

You need `styrminctl` connected to a Styrmin instance. To load from a fixed release,
replace `main` with a tag or commit.

```bash
styrminctl drivers load-version https://github.com/opsmill/styrmin-drivers.git main \
  --driver-directory drivers/infrahub
```

[Load a driver](https://docs.styrmin.app/docs/drivers/loading-drivers) describes the
other ways to load a driver and what happens after it is loaded.

## Before you deploy

### Credentials

The drivers contain fixed public credentials, including admin passwords, database
passwords and service tokens. Replace them with your own before a real deployment.

### db-test and simple-app

1. Build and publish their application images.
2. Publish their Helm charts. For db-test, first fetch the MariaDB and MongoDB chart
   dependencies.
3. Replace the chart locations `db-test` and `simple-app` in `driver.styrmin.yml` with
   the published chart URLs.

### Known issues

- simple-app: the `/probe` endpoint has no authentication and fetches any HTTP URL.
- slurpit: the service and ingress are not connected.

## Files in a driver directory

- `driver.styrmin.yml` (required): the driver specification. It lists the Helm chart,
  parameters, components, environment variables, services and actions.
- `values.j2.yml` (optional): a Jinja2 template that Styrmin renders into the Helm
  values.
- `actions.py` (required only when the specification declares actions): Prefect flows
  for the lifecycle actions, such as `upgrade`.
- `src/` (optional): application source, `Dockerfile` and Helm chart, for drivers that
  build their own application.

## Add a driver

Create a directory under `drivers/` and follow
[Create a driver](https://docs.styrmin.app/docs/drivers/creating-a-driver). The guide
walks through each file and ends with a validation checklist.
