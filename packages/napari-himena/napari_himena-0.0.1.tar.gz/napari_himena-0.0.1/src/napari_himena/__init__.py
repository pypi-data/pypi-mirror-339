__version__ = "0.0.1"

__all__ = ["QNapariHimenaPipeline"]


def __getattr__(name: str):
    if name == "QNapariHimenaPipeline":
        from ._widget import QNapariHimenaPipeline

        return QNapariHimenaPipeline
    raise AttributeError(f"module {__name__} has no attribute {name}")
