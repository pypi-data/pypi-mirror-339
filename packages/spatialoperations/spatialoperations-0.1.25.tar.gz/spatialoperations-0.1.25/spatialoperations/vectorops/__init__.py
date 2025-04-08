from .geoduck import GeoDuck2
from .intake import Intake
from .pmtiles import Exporter

# from rasterops.storage import PlainOlZarrStore
# from rasterops.api import API
import warnings

class AccessorRegistrationWarning(Warning):
    """Warning for when an accessor is being registered that overrides a preexisting attribute."""
    pass

class _CachedAccessor:
    """
    Custom property-like object for caching accessors.
    """
    def __init__(self, name, accessor):
        self._name = name
        self._accessor = accessor
        self._accessor_obj = None

    def __get__(self, obj, cls):
        if self._accessor_obj is None:
            self._accessor_obj = self._accessor(obj)

        return self._accessor_obj

def register_geoduck_accessor(name):
    """
    Register a custom accessor for DataCube objects.

    Parameters
    ----------
    name : str
        Name under which the accessor should be registered. A warning is issued
        if this name conflicts with a preexisting attribute.

    Returns
    -------
    callable
        A decorator that registers the accessor class.
    """
    def decorator(accessor):
        if hasattr(GeoDuck2, name):
            warnings.warn(
                f"registration of accessor {accessor!r} under name {name!r} for DataCube is "
                "overriding a preexisting attribute with the same name.",
                AccessorRegistrationWarning,
                stacklevel=2,
            )
        setattr(GeoDuck2, name, _CachedAccessor(name, accessor))
        return accessor

    return decorator


register_geoduck_accessor("intake")(Intake)
register_geoduck_accessor("pmtiles")(Exporter)
# register_datacube_accessor("api")(API)
# register_datacube_accessor("storage")(PlainOlZarrStore)

__all__ = ["GeoDuck2"]
