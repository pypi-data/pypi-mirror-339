from labels.model.core import (
    Advisory,
    Package,
    PackageType,
)


def matches_namespace(package: Package, advisory: Advisory) -> bool:
    namespace_type = advisory.namespace.split(":")[1]
    if namespace_type == "distro":
        return package.type in {
            PackageType.DebPkg,
            PackageType.ApkPkg,
            PackageType.RpmPkg,
        }

    return False
