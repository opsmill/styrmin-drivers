# Styrmin drivers

Application drivers for [Styrmin](https://docs.styrmin.app/).

## Drivers

The directories under `drivers/` are byte-for-byte copies of `driver/examples/` in
[opsmill/styrmin](https://github.com/opsmill/styrmin/tree/2d6aee04711a34eea3ea9ea3fac853ee898d2197/driver/examples):
db-test, generic-app, infrahub, infrahub-enterprise, infrahub-mcp, semaphore,
simple-app, and slurpit. The db-test and simple-app directories include their
application source and Helm charts. These copies have not been deployed or tested
from this repository.

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
