"""Config module

Attributes
----------
settings : Settings
    Settings instance.
"""

from collections.abc import Sequence
from functools import singledispatch
from importlib.metadata import metadata
from sys import version_info
from typing import Any, Callable

import tomlkit
from aiopath import AsyncPath
from dynaconf import Dynaconf, Validator
from platformdirs import user_config_path

from gole.theme import BUILTIN_THEMES

if version_info < (3, 13):  # pragma: no cover
    from typing_extensions import TypeIs
else:
    from typing import TypeIs

app_name = 'gole'
app_metadata = metadata(app_name)
app_author = app_metadata.get('author')
app_version = app_metadata.get('version')


def bool_condition(value: bool) -> TypeIs[bool]:
    return isinstance(value, bool)


def bool_cast(value: str | bool | None) -> str | bool | None:
    if bool_condition(value):
        return value
    if value is None:
        return None
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False
    return value


class Var(Validator):
    """Variable."""

    def __init__(
        self,
        *names: str,
        description: str,
        must_exist: bool | None = None,
        required: bool | None = None,
        condition: Callable[[Any], bool] | None = None,
        when: Validator | None = None,
        env: str | Sequence[str] | None = None,
        messages: dict[str, str] | None = None,
        cast: Callable[[Any], Any] | None = None,
        default: Any | Callable[[Any, Validator], Any] | None = ...,
        apply_default_on_none: bool | None = False,
        **operations: Any,
    ) -> None:
        super().__init__(
            *names,
            description=description,
            must_exist=must_exist,
            required=required,
            condition=condition,
            when=when,
            env=env,
            messages=messages,
            cast=cast,
            default=default,
            apply_default_on_none=apply_default_on_none,
            **operations,
        )


class IntVar(Var):
    """Integer variable."""

    def __init__(
        self,
        *names: str,
        description: str,
        must_exist: bool | None = None,
        required: bool | None = None,
        condition: Callable[[Any], bool] | None = None,
        when: Validator | None = None,
        env: str | Sequence[str] | None = None,
        messages: dict[str, str] | None = None,
        cast: Callable[[Any], Any] | None = int,
        default: Any | Callable[[Any, Validator], Any] | None = ...,
        apply_default_on_none: bool | None = False,
        **operations: Any,
    ) -> None:
        super().__init__(
            *names,
            description=description,
            must_exist=must_exist,
            required=required,
            condition=condition,
            when=when,
            env=env,
            messages=messages,
            cast=cast,
            default=default,
            apply_default_on_none=apply_default_on_none,
            **operations,
        )


class BoolVar(Var):
    """Boolean variable."""

    def __init__(
        self,
        *names: str,
        description: str,
        must_exist: bool | None = None,
        required: bool | None = None,
        when: Validator | None = None,
        env: str | Sequence[str] | None = None,
        messages: dict[str, str] | None = None,
        default: Any | Callable[[Any, Validator], Any] | None = True,
        apply_default_on_none: bool | None = False,
        **operations: Any,
    ) -> None:
        messages = messages or {}
        messages.setdefault(
            'condition',
            (
                '[cyan]{name}[/] needs a valid boolean like '
                '[yellow]true[/] or [yellow]false[/], no [red]{value}[/]'
            ),
        )

        super().__init__(
            *names,
            description=description,
            must_exist=must_exist,
            required=required,
            condition=bool_condition,
            when=when,
            env=env,
            messages=messages,
            cast=bool_cast,
            default=default,
            apply_default_on_none=apply_default_on_none,
            **operations,
        )


class EnumVar(Var):
    """Enum variable."""

    def __init__(
        self,
        *names: str,
        description: str,
        choices: Sequence[str],
        must_exist: bool | None = None,
        required: bool | None = None,
        when: Validator | None = None,
        env: str | Sequence[str] | None = None,
        messages: dict[str, str] | None = None,
        cast: Callable[[Any], Any] | None = None,
        default: Any | Callable[[Any, Validator], Any] | None = ...,
        apply_default_on_none: bool | None = False,
        **operations: Any,
    ) -> None:
        messages = messages or {}
        messages.setdefault(
            'condition',
            (
                '[red]{value}[/] is not a valid [cyan]{name}[/]. '
                f'The options are: [yellow] {choices}'
            ),
        )

        md_description = f'''
{description}

{'\n'.join(f'- {c}' for c in choices)}
        '''

        self.choices = choices
        super().__init__(
            *names,
            description=md_description,
            must_exist=must_exist,
            required=required,
            condition=lambda v: v in choices,
            when=when,
            env=env,
            messages=messages,
            cast=cast,
            default=default,
            apply_default_on_none=apply_default_on_none,
            **operations,
        )


AVAILABLE_THEMES = list(BUILTIN_THEMES)


@singledispatch
def lower_keys(value):
    return value


@lower_keys.register
def _(value: dict):
    return {k.lower(): lower_keys(v) for k, v in value.items()}


class Settings(Dynaconf):
    """Settings class"""

    async def save(self, **options):
        """Save config file."""
        self.update(options, validate='all')

        config_file = AsyncPath(self.CONFIG_FILE)
        configs = tomlkit.parse(await config_file.read_text())

        new_configs = lower_keys(self.to_dict())
        for exclude in ['version', 'options', 'config_file']:
            new_configs.pop(exclude, None)

        configs |= new_configs

        await config_file.write_text(tomlkit.dumps(configs))


settings = Settings(
    envvar_prefix=app_name.upper(),
    root_path=user_config_path(app_name, app_author, ensure_exists=True),
    settings_files='config.toml',
    validators=[
        EnumVar(
            'THEME',
            description='The theme to use.',
            default='catppuccin-mocha',
            choices=AVAILABLE_THEMES,
        ),
        BoolVar(
            'SOFT_WRAP',
            description='Enable/disable soft wrapping.',
            default=False,
        ),
        EnumVar(
            'TAB_BEHAVIOR',
            default='indent',
            choices=['focus', 'indent'],
            description=(
                'If `focus`, pressing tab will switch focus. '
                'If `indent`, pressing tab will insert a tab.'
            ),
        ),
        BoolVar(
            'SHOW_LINE_NUMBERS',
            description='Show line numbers on the left edge.',
        ),
        IntVar(
            'MAX_CHECKPOINTS',
            description=(
                'The maximum number of undo history checkpoints to retain.'
            ),
            default=50,
        ),
        BoolVar(
            'MATCH_CURSOR_BRACKET',
            description=(
                'If the cursor is at a bracket, '
                'highlight the matching bracket.'
            ),
        ),
        BoolVar(
            'CURSOR_BLINK', description='True if the cursor should blink.'
        ),
        BoolVar(
            'CLOSE_AUTOMATIC_PAIRS',
            description=(
                'If True, every pair will be closed automatically, '
                'like: `<>`, ``, `""`, `()`, `[]`, `{}`'
            ),
            default=False,
        ),
        BoolVar('SHOW_TREE', description='Open tree on mount.'),
        BoolVar('SHOW_FOOTER', description='Show the footer.'),
        BoolVar(
            'SHOW_SCROLL',
            description='Enable/disable scrollbar visualization.',
        ),
        Var(
            'TEXT_LINE_FMT',
            default='{name}   {line}:{column}/{num_lines}',
            description='''File line space format.

| tag              | description                        |
| ---------------- | ---------------------------------- |
| _`{name}`_       | file name                          |
| _`{line}`_       | current cursor line                |
| _`{column}`_     | current cursor column              |
| _`{num_lines}`_  | total number of lines in the file  |
''',
        ),
        Var(
            'LANGUAGE.PYTHON.COMMENT',
            description='Language comment',
            default='# {}',
        ),
        Var(
            'LANGUAGE.JSON.COMMENT',
            description='Language comment',
            default='// {}',
        ),
        Var(
            'LANGUAGE.MARKDOWN.COMMENT',
            description='Language comment',
            default='<!-- {} -->',
        ),
        Var(
            'LANGUAGE.YAML.COMMENT',
            description='Language comment',
            default='# {}',
        ),
        Var(
            'LANGUAGE.TOML.COMMENT',
            description='Language comment',
            default='# {}',
        ),
        Var(
            'LANGUAGE.RUST.COMMENT',
            description='Language comment',
            default='// {}',
        ),
        Var(
            'LANGUAGE.HTML.COMMENT',
            description='Language comment',
            default='<!-- {} -->',
        ),
        Var(
            'LANGUAGE.CSS.COMMENT',
            description='Language comment',
            default='/* {} */',
        ),
        Var(
            'LANGUAGE.XML.COMMENT',
            description='Language comment',
            default='<!-- {} -->',
        ),
        Var(
            'LANGUAGE.REGEX.COMMENT',
            description='Language comment',
            default='# {}',
        ),
        Var(
            'LANGUAGE.SQL.COMMENT',
            description='Language comment',
            default='-- {}',
        ),
        Var(
            'LANGUAGE.JAVASCRIPT.COMMENT',
            description='Language comment',
            default='// {}',
        ),
        Var(
            'LANGUAGE.JAVA.COMMENT',
            description='Language comment',
            default='// {}',
        ),
        Var(
            'LANGUAGE.BASH.COMMENT',
            description='Language comment',
            default='# {}',
        ),
        Var(
            'LANGUAGE.GO.COMMENT',
            description='Language comment',
            default='// {}',
        ),
    ],
)

settings.validators.validate_all()

# NOTE: cli needs this
settings.VERSION = app_version

# NOTE: `settings.save` needs this
settings.OPTIONS = [v.names[0].lower() for v in settings.validators]
settings.CONFIG_FILE = (
    settings.ROOT_PATH_FOR_DYNACONF / settings.SETTINGS_FILE_FOR_DYNACONF
)
settings.CONFIG_FILE.touch()
