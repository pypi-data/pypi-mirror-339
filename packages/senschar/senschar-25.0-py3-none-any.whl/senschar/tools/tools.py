"""
*azcam.tools* contains the `Tools` base tool class.
"""

import azcam
import azcam.exceptions


class Tools(object):
    """
    Base class used by tools (controller, instrument, telescope, etc.).
    """

    def __init__(self, tool_id: str, description: str | None = None):
        """
        Args:
            tool_id: name used to reference the tool (controller, display, etc.)
            description: description of this tool
        """

        #: name used to reference the tool ("controller", "display", ...)
        self.tool_id: str = tool_id

        #: descriptive tool name
        self.description: str = ""
        if description is None:
            self.description = self.tool_id
        else:
            self.description = description

        #: 1 when tool is enabled
        self.is_enabled: int = 1

        #: 1 when tool has been initialized
        self.is_initialized: int = 0

        #: 1 when tool has been reset
        self.is_reset: int = 0

        # save tool name
        azcam.db.tools.update({self.tool_id: self})

        # add tool to CLI
        azcam.db.cli.update({self.tool_id: self})

        #: verbosity for debug, >0 is more verbose
        self.verbosity = 0

    def initialize(self) -> None:
        """
        Initialize the tool.
        """

        if self.is_initialized:
            return

        if not self.is_enabled:
            azcam.exceptions.warning(f"{self.description} is not enabled")
            return

        self.is_initialized = 1

        return

    def reset(self) -> None:
        """
        Reset the tool.
        """

        self.is_reset = 1

        return
