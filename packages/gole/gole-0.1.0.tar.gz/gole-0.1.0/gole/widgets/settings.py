from functools import singledispatch
from typing import Any

from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.content import ContentType
from textual.message import Message
from textual.widget import Widget
from textual.widgets import (
    Collapsible,
    Input,
    Markdown,
    Select,
    Switch,
    TabPane,
)

from gole.config import BoolVar, EnumVar, IntVar, Var, settings


@singledispatch
def to_widgets(var: Var, name: str) -> ComposeResult:
    yield Input(placeholder=settings[name], name=name)


@to_widgets.register
def _(var: BoolVar, name: str) -> ComposeResult:
    yield Switch(settings[name], name=name)


@to_widgets.register
def _(var: EnumVar, name: str) -> ComposeResult:
    yield Select.from_values(
        var.choices,
        value=settings[name],
        prompt=settings[name],
        allow_blank=False,
        name=name,
    )


@to_widgets.register
def _(var: IntVar, name: str) -> ComposeResult:
    yield Input(placeholder=str(settings[name]), type='integer', name=name)


class SettingsPane(TabPane):
    class Changed(Message):
        def __init__(self, option: str, value: Any) -> None:
            self.option = option
            self.value = value
            super().__init__()

    def __init__(
        self,
        *children: Widget,
        title: ContentType = '[$green]Settings[/]',
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        super().__init__(
            title,
            *children,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    def compose(self) -> ComposeResult:
        with VerticalScroll(classes='hide-scroll') as scroll:
            for var in settings.validators:
                for name in map(str.lower, var.names):
                    with Collapsible(title=name, name=name):
                        yield from to_widgets(var, name)
                        yield Markdown(var.description, name=name)
            scroll.focus()

    @on(Input.Submitted)
    async def settings_input_submitted(self, event: Input.Submitted):
        if settings[event.input.name] == event.value:
            return

        if await self.post_settings_changed(event.input.name, event.value):
            event.stop()
            return

    @on(Select.Changed)
    async def settings_select_changed(self, event: Select.Changed):
        if settings[event.select.name] == event.value:
            return

        if await self.post_settings_changed(event.select.name, event.value):
            event.stop()
            return

    @on(Switch.Changed)
    async def settings_switch_changed(self, event: Switch.Changed):
        if settings[event.switch.name] == event.value:
            return

        if await self.post_settings_changed(event.switch.name, event.value):
            event.stop()
            return

    async def post_settings_changed(self, option: str, value: Any):
        msg_type = f'{option}_changed'.title().replace('_', '')
        if not (message := getattr(self, msg_type, None)):
            return False

        self.post_message(message(option, value))
        await settings.save(**{option: value})

        theme = self.app.current_theme
        self.notify(
            f'Configuration upgraded to [{theme.accent}]{value}[/]',
            title=f'{option}',
        )
        return True

    @property
    def scroll(self) -> VerticalScroll:
        return self.query_one(VerticalScroll)


# Create message, like Settins.ThemeChanged, Settins.ShowTreeChanged
# Settins.<Option>Changed
# Option in PascalCase
for option in settings.OPTIONS:
    messenger = f'{option}_changed'.title().replace('_', '')
    class_ = type(messenger, (SettingsPane.Changed,), {})
    setattr(SettingsPane, messenger, class_)
else:
    del option
    del messenger
    del class_
