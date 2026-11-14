from styrmin_backend.actions import (
    GlobalContext,
    start_components,
    stop_components,
    upgrade_deployment_version,
)
from prefect import flow, get_run_logger


@flow
async def upgrade(context: GlobalContext, target_version: str):
    logger = get_run_logger()
    logger.info("Starting NetBox upgrade...")

    # Keep the database and cache running. The NetBox container applies the
    # database migrations when it starts with the new version.
    await stop_components(components=["server", "worker"], context=context)

    await upgrade_deployment_version(target_version=target_version, context=context)

    await start_components(components=["server", "worker"], context=context)

    logger.info(f"NetBox upgrade to {target_version} complete.")


@flow
def pre_setup(context: GlobalContext):
    logger = get_run_logger()
    logger.info("Executing NetBox pre-setup...")


@flow
def post_setup(context: GlobalContext):
    logger = get_run_logger()
    logger.info("Executing NetBox post-setup...")
