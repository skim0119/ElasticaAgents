import os
import pkg_resources

try:
    # Try to get the version from the installed package
    __version__ = pkg_resources.get_distribution("elastica-agents").version
except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
    __version__ = None
