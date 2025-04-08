import os
from concurrent.futures import ThreadPoolExecutor

from labels.advisories.images.database import DATABASE as IMAGES_DATABASE
from labels.advisories.roots import DATABASE as ROOTS_DATABASE
from labels.config.bugsnag import initialize_bugsnag
from labels.config.logger import LOGGER, configure_logger, modify_logger_level
from labels.core.source_dispatcher import resolve_sbom_source
from labels.format import format_sbom
from labels.internal.file_resolver.container_image import ContainerImage
from labels.model.core import SbomConfig
from labels.pkg.cataloger.complete import complete_package
from labels.pkg.operations.package_operation import package_operations_factory
from labels.sources.directory_source import Directory


def initialize_scan_environment(sbom_config: SbomConfig) -> None:
    configure_logger()
    initialize_bugsnag()

    if sbom_config.debug:
        modify_logger_level()

    ROOTS_DATABASE.initialize()
    IMAGES_DATABASE.initialize()


def execute_labels_scan(sbom_config: SbomConfig) -> None:
    try:
        initialize_scan_environment(sbom_config)

        main_sbom_resolver = resolve_sbom_source(sbom_config)
        LOGGER.info(
            "📦 Generating SBOM from %s: %s",
            sbom_config.source_type.value,
            sbom_config.source,
        )

        packages, relationships = gather_packages_and_relationships(main_sbom_resolver)

        LOGGER.info("📦 Preparing %s report", sbom_config.output_format)
        format_sbom(
            packages=packages,
            relationships=relationships,
            config=sbom_config,
            resolver=main_sbom_resolver,
        )
    except Exception:
        LOGGER.exception(
            "Error executing labels scan",
            extra={"execution_id": sbom_config.execution_id},
        )
        raise


def gather_packages_and_relationships(
    resolver: Directory | ContainerImage,
    max_workers: int = 32,
) -> tuple[list, list]:
    packages, relationships = package_operations_factory(resolver)

    worker_count = min(
        max_workers,
        (os.cpu_count() or 1) * 5 if os.cpu_count() is not None else max_workers,
    )
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        LOGGER.info("📦 Gathering additional package information")
        packages = list(filter(None, executor.map(complete_package, packages)))

    return packages, relationships
