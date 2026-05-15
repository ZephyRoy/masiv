class MasivError(Exception):
    """Base exception for MASIV."""


class VcfParseError(MasivError):
    """Raised when VCF input cannot be parsed safely."""


class RulePackError(MasivError):
    """Raised when a rule pack is malformed or cannot be resolved."""


class CombinerError(MasivError):
    """Raised when criterion results cannot be combined."""
