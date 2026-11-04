# Styrmin drivers

Application drivers for [Styrmin](https://docs.styrmin.app/).

## Drivers

The directories under `drivers/` are byte-for-byte copies of `driver/examples/` in
[opsmill/styrmin](https://github.com/opsmill/styrmin/tree/2d6aee04711a34eea3ea9ea3fac853ee898d2197/driver/examples):
db-test, generic-app, infrahub, infrahub-enterprise, infrahub-mcp, semaphore,
simple-app, and slurpit. The exceptions are `infrahub-1.12` and
`infrahub-enterprise-1.12`, which exist only in this repository (see
[Prereleases of Infrahub](#prereleases-of-infrahub)). The db-test and simple-app
directories include their application source and Helm charts. The byte-for-byte copies
have not been deployed or tested from this repository.

The db-test and simple-app examples need preparation before deployment: build and
distribute their application images, publish their Helm charts, and replace the bare
chart locations (`db-test` and `simple-app`) in the driver specifications with the
published chart URLs. Fetch the db-test chart's MariaDB and MongoDB dependencies before
packaging it. Including the source directories here does not perform these steps.

The drivers contain fixed public credentials, including admin passwords, database
passwords, and service tokens. Replace them with your own before a real deployment.
Source issues are preserved in these copies, including simple-app's unauthenticated
`/probe` endpoint that fetches arbitrary HTTP URLs and Slurpit's missing service and
ingress wiring. Review the source before deploying.

## Load a driver

```bash
styrminctl drivers load-version https://github.com/opsmill/styrmin-drivers.git main \
  --driver-directory drivers/infrahub
```

## Prereleases of Infrahub

A driver range matches a prerelease such as `1.12.0b0` only if one of its clauses
names a prerelease. This is described in the section "Prereleases in
`supported_versions`" of the Styrmin driver documentation, proposed in the open pull
request [opsmill/styrmin#594](https://github.com/opsmill/styrmin/pull/594). The ranges of
`drivers/infrahub` and `drivers/infrahub-enterprise` are `>=1.5,<2.0`, so Styrmin
refuses every prerelease of Infrahub with them.

`drivers/infrahub-1.12` and `drivers/infrahub-enterprise-1.12` deploy the prereleases
of Infrahub 1.12. Each is a copy of the driver with the same name and these changes
in `driver.styrmin.yml`:

| Driver | Directory | Driver version | `supported_versions` |
|---|---|---|---|
| `infrahub` | `drivers/infrahub` | 5 | `>=1.5,<2.0` |
| `infrahub` | `drivers/infrahub-1.12` | 6 | `>=1.12.0b0,<1.13` |
| `infrahub-enterprise` | `drivers/infrahub-enterprise` | 4 | `>=1.5,<2.0` |
| `infrahub-enterprise` | `drivers/infrahub-enterprise-1.12` | 5 | `>=1.12.0b0,<1.13` |

Load the 1.12 driver in addition to the standard one:

```bash
styrminctl drivers load-version https://github.com/opsmill/styrmin-drivers.git main \
  --driver-directory drivers/infrahub-1.12
```

Notes:

- The range `>=1.12.0b0,<1.13` also accepts the stable releases 1.12.0 and later 1.12.x.
  Styrmin binds those deployments to the 1.12 driver version, because it has the highest
  driver version of the driver.
- A prerelease of another minor version, such as 1.13.0b0, is refused until a driver with
  a range for that version is loaded.
- The only differences between a driver and its 1.12 copy are the driver version, the
  range and the comment above the range. Apply every other change to both directories.
  `diff -r drivers/infrahub drivers/infrahub-1.12` and
  `diff -r drivers/infrahub-enterprise drivers/infrahub-enterprise-1.12` must show only
  those lines.
- Keep the driver version of the 1.12 copy higher than the driver version of the standard
  driver. Stable 1.12.x releases match both ranges, and Styrmin binds them to the highest
  driver version. With equal driver versions, the load time decides. When you raise the
  driver version of a standard driver, raise its 1.12 copy above it.

Status, 2026-11-04:

- `drivers/infrahub-1.12` was deployed with Infrahub `1.12.0b0` on Styrmin 0.1.56 (kind,
  Kubernetes 1.37, arm64): all 8 pods were Ready, Styrmin reported the deployment
  `running`, and `/api/info` of Infrahub returned version `1.12.0b0`.
- `drivers/infrahub-enterprise-1.12` was not deployed itself. A lab-only driver that
  differs from it only by a comment (the range and the driver version are the same) was
  deployed the same way in
  [opsmill/styrmin#591](https://github.com/opsmill/styrmin/issues/591): all 8 pods were
  Ready. The Enterprise image `1.12.0b0` reported the version `1.12.0b1.dev9+gd70874a98`
  through `/api/info`. The cause is not known.
- No test checks that the copies stay in step.
