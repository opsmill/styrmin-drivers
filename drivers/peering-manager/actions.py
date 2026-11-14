from styrmin_backend.actions import (
    GlobalContext,
    execute_commands,
    get_component_images,
    start_components,
    stop_components,
    upgrade_deployment_version,
)
from prefect import flow, get_run_logger


@flow
async def upgrade(context: GlobalContext, target_version: str):
    """Upgrade Peering Manager with no old code running against the migrated database.

    Stops the worker and the web application, changes the version, runs the Django
    migrations in a Job with the new image, then starts the web application and the
    worker.
    """
    logger = get_run_logger()
    logger.info(f"Upgrading Peering Manager to {target_version}...")

    await stop_components(components=["worker", "web"], context=context)

    await upgrade_deployment_version(target_version=target_version, context=context)

    images = await get_component_images(component="web", context=context)
    # images[0] is the component container's image; drop any digest, then the tag
    # (a ":" followed by a "/" is a registry port, not a tag).
    name = images[0].split("@", 1)[0]
    repository, separator, tag = name.rpartition(":")
    image_base = repository if separator and "/" not in tag else name

    # The image tags are the versions with a "v" prefix (v1.11.1).
    await execute_commands(
        [
            "/opt/peering-manager/venv/bin/python",
            "/opt/peering-manager/manage.py",
            "migrate",
            "--no-input",
        ],
        image=f"{image_base}:v{target_version}",
        context=context,
        env_from_component="web",
        labels_from_component="web",
    )

    await start_components(components=["web", "worker"], context=context)

    logger.info(f"Peering Manager upgrade to {target_version} complete.")
