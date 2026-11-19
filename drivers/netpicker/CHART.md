# The Netpicker chart of this driver

`chart/` is the Helm chart of [github.com/netpicker/netpicker](https://github.com/netpicker/netpicker)
(`netpicker-chart/`) at commit `a2111fe`, with the changes below. Netpicker does not publish the
chart to a chart repository, so OpsMill publishes this copy as
`oci://registry.opsmill.io/external/netpicker`, version `2.8.1-opsmill.1`.

## Changes to the upstream chart

| File | Change | Why |
|------|--------|-----|
| `templates/ingress.yaml` | New: an Ingress to the frontend, with `ingress.hosts` | The upstream chart has no Ingress, so Netpicker is not reachable from outside the cluster |
| `templates/db-deployment.yaml` | `db.extraEnv`, `db.extraVolumes` and `db.extraVolumeMounts` | The Styrmin `postgres` backup reads `POSTGRES_USER` and `POSTGRES_DATABASE` and writes its dump to a `backup` volume |
| `templates/db-deployment.yaml` | The volume claim template has the selector labels only, without `helm.sh/chart` and `app.kubernetes.io/version` | Kubernetes does not allow a change of a StatefulSet's volume claim templates, so with the chart version in a label, each new chart version fails to upgrade |
| `templates/secrets.yaml` | `db.apiUser`, `db.apiPassword`, `minio.rootPassword` and `redis.passwordValue`, with the upstream values as defaults | The upstream chart hard-codes these credentials |
| `templates/db-migration-job.yaml` | The Job name ends with a hash of the API image and the target database revision | A Job's pod template cannot change: an upgrade that changes the image of a Job with the same name fails |
| `templates/committer-deployment.yaml` | The Deployment is labeled `app.kubernetes.io/component: committer`, as its pods are | Upstream labels the Deployment `celery`, so a selector on the workload label matches both worker Deployments |
| `Chart.yaml` | Version `2.8.1-opsmill.1` | Tells this copy apart from the upstream chart |

## What the driver sets

- `storageClass.enabled: false`: the upstream chart creates a cluster-wide StorageClass.
- `persistence.config.enabled: false` and `persistence.transferium.enabled: false`: no pod mounts
  these volumes, so with a `WaitForFirstConsumer` storage class they stay Pending and the install
  times out.
- `gitd.service.type: ClusterIP`: the upstream default `NodePort` opens the git daemon on every
  node of the cluster.
- `api.alembicVersion` from the version map in `values.j2.yml`. The API and the workers wait in
  their init container until the database has exactly this revision. `head` does not work: the
  pods then wait forever.
- `db.apiUser: postgres`: the API, the workers and the migration Job connect as the database
  superuser. The Styrmin restore runs `pg_restore --no-owner` as `POSTGRES_USER`, so the restored
  tables belong to that user. With the upstream user `netpicker`, the restore cannot replace the
  extensions that the `postgres` user owns.

## Add a Netpicker version

1. Read the database revision of the new version:

   ```shell
   docker run --rm --entrypoint sh netpicker/api:<version> -c 'cd /opt && alembic heads'
   ```

2. Add the version and the revision to `alembic_revisions` in `values.j2.yml`.
3. If the version is outside `supported_versions`, compare the upstream chart with `chart/` and
   publish a new chart version when the templates changed.

A deployment can also set the `alembic_revision` parameter, which takes precedence over the map.

## Publish the chart

```shell
helm package drivers/netpicker/chart
helm push netpicker-2.8.1-opsmill.1.tgz oci://registry.opsmill.io/external
```
