from styrmin_backend.actions import (
    GlobalContext,
    start_components,
    stop_components,
    upgrade_deployment_version,
)
from prefect import flow, get_run_logger

# The components that write to the database. The other components keep running, so
# devices can still send syslog messages and the configuration backups stay readable.
DATABASE_WRITERS = ["api", "celery", "committer"]


@flow
async def upgrade(context: GlobalContext, target_version: str):
    logger = get_run_logger()
    logger.info("Starting Netpicker upgrade...")

    await stop_components(components=DATABASE_WRITERS, context=context)

    # The new chart values run a new migration Job, which migrates the database to the
    # revision of the target version (or back to it, for a downgrade). The API and the
    # workers wait in their init container until the database has that revision.
    await upgrade_deployment_version(target_version=target_version, context=context)

    await start_components(components=DATABASE_WRITERS, context=context)

    logger.info(f"Netpicker upgrade to {target_version} complete.")


@flow
def pre_setup(context: GlobalContext):
    logger = get_run_logger()
    logger.info("Executing Netpicker pre-setup...")


@flow
def post_setup(context: GlobalContext):
    logger = get_run_logger()
    logger.info("Executing Netpicker post-setup...")
