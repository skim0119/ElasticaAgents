import importlib.metadata

try:
    # Try to get the version from the installed package
    __version__ = importlib.metadata.version("elasticaa_agents")
except importlib.metadata.PackageNotFoundError:
    __version__ = "None"
