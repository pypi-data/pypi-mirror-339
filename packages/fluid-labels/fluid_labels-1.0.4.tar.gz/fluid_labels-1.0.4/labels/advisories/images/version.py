import logging
import re
from typing import Self

from packageurl import PackageURL
from univers.version_range import (
    RANGE_CLASS_BY_SCHEMES,
    InvalidVersionRange,
    VersionConstraint,
    VersionRange,
)
from univers.versions import (
    AlpineLinuxVersion,
    DebianVersion,
    InvalidVersion,
    RpmVersion,
    SemverVersion,
    Version,
)

from labels.model.core import (
    Advisory,
    Package,
)

LOGGER = logging.getLogger(__name__)


def _get_version_scheme_by_namespace(package: Package, namespace: str) -> Version | None:
    schemes = {
        "distro": {
            "alpine": AlpineLinuxVersion,
            "debian": DebianVersion,
            "redhat": RpmVersion,
            "ubuntu": DebianVersion,
        },
        "type": {
            "apk": AlpineLinuxVersion,
            "cocoapods": SemverVersion,
            "deb": DebianVersion,
            "rpm": RpmVersion,
        },
    }

    def _get_distro_scheme() -> Version | None:
        if package.p_url:
            package_url = PackageURL.from_string(package.p_url)
            if isinstance(package_url.qualifiers, dict) and (
                distro := package_url.qualifiers.get("distro_id")
            ):
                return schemes["distro"].get(distro)
        return None

    parts = namespace.split(":")
    if len(parts) < 3:
        return _get_distro_scheme()

    namespace_type, subtype = parts[1], parts[2]
    result = schemes.get(namespace_type, {}).get(subtype)

    return result or _get_distro_scheme()


class ApkVersionRange(VersionRange):  # type: ignore[misc]
    scheme = "apk"
    version_class = AlpineLinuxVersion

    @classmethod
    def from_native(cls, string: str) -> Self:
        constraints: list[str] = []
        match = re.match(r"([<>=~!^]*)(.*)", string)
        if not match:
            LOGGER.error("Invalid version range format: %s", string)
            return cls(constraints=constraints)
        comparator, version = match.groups()
        version = version.strip()
        return cls(
            constraints=[
                VersionConstraint(comparator=comparator, version=cls.version_class(version)),
            ],
        )


def _compare_single_constraint(version: Version, constraint: str, scheme: str) -> bool:
    version_range: VersionRange | None = {
        **RANGE_CLASS_BY_SCHEMES,
        "apk": ApkVersionRange,
    }.get(scheme)

    if not version_range:
        LOGGER.error(
            "Invalid version scheme: %s",
            scheme,
        )
        return False
    try:
        return version in version_range.from_native(constraint)
    except (InvalidVersion, InvalidVersionRange, TypeError):
        return False


def _matches_constraint(version: Version, constraint: str, version_scheme: str) -> bool:
    if not constraint:
        return True

    constraints = constraint.split(",")
    return all(
        _compare_single_constraint(version, constraint.strip(), version_scheme)
        for constraint in constraints
    )


def matches_version(package: Package, advisory: Advisory) -> bool:
    version_type = _get_version_scheme_by_namespace(package, advisory.namespace)
    if version_type is None:
        LOGGER.debug(
            "No version scheme found for namespace %s",
            advisory.namespace,
        )
        return False

    if advisory.version_constraint is None:
        return True
    if not package.p_url:
        return False

    try:
        match = re.match(r"([<>=~!^]*)(.*)", package.version)
        if not match:
            return False

        _, version = match.groups()
        version = version.strip()

        return any(
            _matches_constraint(
                version_type(version),
                constraint.strip(),
                PackageURL.from_string(package.p_url).type,
            )
            for constraint in advisory.version_constraint.split("||")
        )
    except (AttributeError, InvalidVersion):
        return False
