# The Slurp'it chart of this driver

`chart/` is the Helm chart of [gitlab.com/slurpit.io/images](https://gitlab.com/slurpit.io/images/-/tree/main/helm-charts)
(`helm-charts/slurpit/`) at commit `b65e64a`, with the changes below. OpsMill publishes it as
`oci://registry.opsmill.io/external/slurpit`, version `1.3.7`.

The previous OpsMill version, `1.3.6`, does not have the retriever component that the upstream
chart added in April 2026.

## Changes to the upstream chart

| File | Change | Why |
|------|--------|-----|
| `templates/mariadb.yaml`, `templates/mongodb.yaml` | `extraVolumes` and `extraVolumeMounts` | The Styrmin `mariadb` and `mongodb` backups write their dump to a `backup` volume. The same change was in `1.3.6` |
| `templates/portal.yaml` | `portal.ingress.extraHosts` | The upstream Ingress has one host. The driver adds the short host that Styrmin shows (`slurpit-<environment>`) |
| `Chart.yaml` | Version `1.3.7` | The upstream `Chart.yaml` still says `1.3.4` |

## Application versions

Slurp'it versions each component separately: for example the portal is at `1.4.235` and the scraper
at `1.4.76`. Each image also has a tag for its release line, which moves to each new patch release.
The driver's application version is therefore the release line (`1.3` or `1.4`), and
`values.j2.yml` maps it to the tag of each component:

| Release line | portal, warehouse, scanner, retriever | scraper |
|--------------|---------------------------------------|---------|
| `1.3` | `1.3.x` | `1.3` |
| `1.4` | `1.4` | `1.4` |

The image pull policy is `Always`, so a pod that starts pulls the newest patch release of its line.

## Publish the chart

```shell
helm package drivers/slurpit/chart
helm push slurpit-1.3.7.tgz oci://registry.opsmill.io/external
```
