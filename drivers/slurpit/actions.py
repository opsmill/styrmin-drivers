from styrmin_backend.actions import (
    GlobalContext,
    start_components,
    stop_components,
    upgrade_deployment_version,
)
from prefect import flow, get_run_logger

APPLICATION_COMPONENTS = ["portal", "warehouse", "scanner", "scraper", "retriever"]


@flow
async def upgrade(context: GlobalContext, target_version: str):
    logger = get_run_logger()
    logger.info("Starting Slurpit upgrade...")

    # Stop application services, keep databases running. The portal migrates the
    # MariaDB database when it starts on the new version.
    await stop_components(components=APPLICATION_COMPONENTS, context=context)

    await upgrade_deployment_version(target_version=target_version, context=context)

    await start_components(components=APPLICATION_COMPONENTS, context=context)

    logger.info(f"Slurpit upgrade to {target_version} complete.")


@flow
def pre_setup(context: GlobalContext):
    logger = get_run_logger()
    logger.info("Executing Slurpit pre-setup...")


@flow
def post_setup(context: GlobalContext):
    logger = get_run_logger()
    logger.info("Executing Slurpit post-setup...")
