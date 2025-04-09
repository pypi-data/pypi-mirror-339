from pathlib import Path
from typing import Literal

from aiopath import AsyncPath
from cyclopts import App
from dynaconf import ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from gole.app import Gole
from gole.config import settings

console = Console()
app = App(
    console=console,
    version=settings.VERSION,
    version_flags=['--version', '-v'],
)


@app.default
def default(path: str = '.'):
    """Simple editor for simple things.

    Parameters
    ----------
    path : str, default=.
        File or directory to be worked.
    """
    Gole(AsyncPath(path), Path.cwd()).run()


# Config
CONFIG_CMD = '--config'
app.command(
    App(
        name=(CONFIG_CMD, '-c'),
        group='Config',
        version_flags=[],
        console=console,
        help='Manages configuration settings',
    )
)

Options = Literal[tuple(settings.OPTIONS)]


@app[CONFIG_CMD].command
def list():
    """List the active configuration."""
    table = Table(title='Configs')
    table.add_column('OPTION', style='cyan')
    table.add_column('VALUE', style='white')

    for option in settings.OPTIONS:
        table.add_row(option, str(settings[option]))

    console.print(table)


@app[CONFIG_CMD].command
def edit():
    """Edit the configuration file in the editor."""
    cwd = Path.cwd()
    Gole(cwd, cwd, open_settings_on_mount=True).run()


@app[CONFIG_CMD].command
def get(option: Options):
    """Get the value associated with OPTION.

    Parameters
    ----------
    option : Options
        Option to look for the value.
    """
    table = Table(title='Configs')
    table.add_column('OPTION', style='cyan')
    table.add_column('VALUE', style='white')

    table.add_row(option, str(settings[option]))
    console.print(table)


@app[CONFIG_CMD].command
async def set(option: Options, value: str):
    """Set the OPTION VALUE.

    Parameters
    ----------
    option : Options
        Option to be changed.
    value : str
        Value to be defined.
    """
    try:
        await settings.save(**{option: value})
    except ValidationError as error:
        panel = Panel.fit(
            Text.from_markup(f'{error}', justify='center'),
            title='Error',
            border_style='red',
        )
        console.print(panel)
        return True

    panel = Panel.fit(
        Text.from_markup(
            f'setted:  [cyan]{option.upper()}[/] = {value}',
            justify='center',
        ),
        title='Success',
        border_style='green',
    )
    console.print(panel)
