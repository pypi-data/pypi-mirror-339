from typing import List

from bluer_options.terminal import show_usage, xtra
from bluer_ai.help.generic import help_functions as generic_help_functions

from bluer_south import ALIAS


def help_browse(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "actions|repo"

    return show_usage(
        [
            "@south",
            "browse",
            f"[{options}]",
        ],
        "browse bluer_south.",
        mono=mono,
    )


help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "browse": help_browse,
    }
)
