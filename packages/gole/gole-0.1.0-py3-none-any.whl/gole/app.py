import asyncio
from collections import deque
from collections.abc import Iterable
from contextlib import suppress
from itertools import chain
from pathlib import Path
from typing import ClassVar

import pyperclip
from aiopath import AsyncPath
from textual import on, work
from textual.app import App, ComposeResult, ReturnType, SystemCommand
from textual.binding import Binding, BindingType
from textual.css.query import NoMatches
from textual.driver import Driver
from textual.screen import Screen
from textual.types import CSSPathType
from textual.widgets import Footer, TabbedContent
from textual_fspicker import FileOpen

from gole.config import settings
from gole.dialogs import Confirm
from gole.widgets import (
    Board,
    DirectoryTree,
    SettingsPane,
    TextArea,
    TextPane,
    TreeView,
)


class Gole(App[ReturnType]):
    CSS_PATH = 'gole.tcss'

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding(
            'ctrl+backslash',
            'toggle_tree',
            'Tree',
            tooltip='Toggle tree viewer',
        ),
        Binding(
            'ctrl+n',
            'new_tab',
            'New',
            tooltip='Open a new tab',
        ),
        Binding(
            'ctrl+q',
            'quit',
            'Quit',
            tooltip='Quit the app and return to the command prompt',
            priority=True,
        ),
        Binding(
            'ctrl+o',
            'open_file',
            'Open',
            tooltip='Open a new file',
        ),
        Binding(
            'ctrl+e',
            'settings_pane',
            'Settings',
            tooltip='Open settings panel',
        ),
        Binding('ctrl+c', 'help_quit', show=False, system=True),
    ]

    @property
    def _clipboard(self) -> str:
        try:
            # Trying to copy from external clipboard
            return pyperclip.paste()
        except pyperclip.PyperclipException:
            # Using an internal fallback clipboard
            return getattr(self, '_internal_clipboard', '')

    @_clipboard.setter
    def _clipboard(self, text: str) -> None:
        if not text:
            return

        # saving text to the internal fallback clipboard
        self._internal_clipboard = text

        # Trying to copy to external clipboard
        with suppress(pyperclip.PyperclipException):
            pyperclip.copy(text)

    def __init__(
        self,
        current_file: AsyncPath | Path | None = None,
        workdir: AsyncPath | Path | None = None,
        open_settings_on_mount: bool = False,
        driver_class: type[Driver] | None = None,
        css_path: CSSPathType | None = None,
        watch_css: bool = False,
        ansi_color: bool = False,
    ) -> None:
        super().__init__(driver_class, css_path, watch_css, ansi_color)

        self.workdir: AsyncPath = AsyncPath(workdir or Path.cwd())
        self.current_file: AsyncPath = AsyncPath(current_file or self.workdir)
        self.open_settings_on_mount: bool = open_settings_on_mount

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)

        yield SystemCommand(
            'Quit all',
            'Quit all files without saving',
            self.action_quit_all,
        )

        yield SystemCommand('Toggle', 'Toggle tree', self.action_toggle_tree)
        yield SystemCommand(
            'Close', 'Close current tab', self.action_close_tab
        )
        yield SystemCommand('New', 'Create a new tab', self.action_new_tab)
        yield SystemCommand(
            'Settings', 'Open settings panel', self.action_settings_pane
        )

    def compose(self) -> ComposeResult:
        self.tree_view = TreeView(self.current_file, self.workdir)
        self.tree_view.display = settings.SHOW_TREE
        yield self.tree_view

        self.board = Board()
        yield self.board

        self.footer = Footer()
        self.footer.display = settings.SHOW_FOOTER
        yield self.footer

    # Actions

    @work
    async def action_quit(self) -> None:
        """An action to quit the app as soon as possible."""
        if not (unsaved := self.board.unsaved):
            self.exit()
            return

        cancels = []
        for area in unsaved:
            message = (
                f'[$accent]{await area.path.absolute()}[/]\n\n'
                'The file contains changes that have not been saved. \n'
                'Would you like to continue?'
            )
            screen = Confirm(
                'Close file',
                message,
                save_text='Save',
                save_action=area.action_save,
            )
            if not await self.app.push_screen_wait(screen):
                cancels.append(area)
        if not cancels:
            self.exit()
            return

        paths = await asyncio.gather(
            *[area.path.absolute() for area in cancels]
        )
        theme = self.app.current_theme
        message = (
            'It was not possible to close the application '
            'because the following files would lose their changes:\n\n'
            f'{"\n".join(f"- [{theme.warning}]{a}[/]" for a in paths)}'
        )
        self.notify(message, severity='error')

    async def action_quit_all(self) -> None:
        """An action to quit the app without saving any files."""
        if not (unsaved := self.board.unsaved):
            self.exit()
            return

        paths = await asyncio.gather(
            *[area.path.absolute() for area in unsaved]
        )

        message = (
            '[i $accent]Do you want to continue?[/] \n\n'
            'The following files have not been saved:\n\n'
            'The following files have not been saved, '
            r'press [$accent]\[s][/] to save all or '
            r'[$accent]\[y][/] to exit without saving:\n\n'
            f'{"\n".join(f"- [$warning]{a}[/]" for a in paths)}'
        )
        screen = Confirm(
            'Quit all',
            message,
            save_text='Save all',
            save_action=self.board.action_save_all,
        )
        self.app.push_screen(screen, lambda yes: self.exit() if yes else None)

    async def action_toggle_tree(self):
        """Toggle tree view."""
        display = not self.tree_view.display
        self.tree_view.display = display

        if display:
            if self.tree_view.dir_tree:
                self.tree_view.dir_tree.focus()
            else:
                await self.tree_view.open_cwd()
        elif text_area := self.text_area:
            text_area.focus()

    async def action_settings_pane(self):
        """Open/focus settings pane."""
        if pane := self.settings_pane:
            return pane.scroll.focus()

        pane = SettingsPane()
        return self.board.add_pane(pane)

    async def action_close_tab(self):
        """Close current tab."""
        await self.board.action_close_tab()

    async def action_new_tab(self, file_path: AsyncPath | None = None):
        """New tab."""
        if file_path:
            return await self.board.action_add_text_pane(file_path)
        await self.action_open_file(must_exist=False)

    async def action_open_file(
        self, workdir: AsyncPath | None = None, must_exist: bool = True
    ):
        """Open file."""
        workdir = workdir or self.workdir
        board = self.board

        async def callback(opened: str | None):
            if opened:
                await board.action_add_text_pane(AsyncPath(opened))

        screen = FileOpen(
            workdir,
            cancel_button='Cancel',
            must_exist=must_exist,
        )
        self.push_screen(screen, callback)

    # Events handler

    async def on_mount(self):
        self.theme = settings.THEME

        self.current_file = await self.current_file.resolve()
        if not await self.current_file.is_dir():
            await self.board.action_add_text_pane(self.current_file)

        if self.open_settings_on_mount:
            await self.action_settings_pane()

    def on_tabbed_content_tab_activated(
        self, event: TabbedContent.TabActivated
    ):
        pane = event.pane
        pane.children[0].focus()

    async def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ):
        await self.action_new_tab(AsyncPath(event.path))

    @on(SettingsPane.ThemeChanged)
    def on_settings_pane_theme_changed(self, event: SettingsPane.ThemeChanged):
        self.theme = event.value

    @on(SettingsPane.ShowTreeChanged)
    def on_settings_pane_show_tree_changed(
        self, event: SettingsPane.ShowTreeChanged
    ):
        self.tree_view.display = event.value

    @on(SettingsPane.ShowFooterChanged)
    def on_settings_pane_show_footer_changed(
        self, event: SettingsPane.ShowFooterChanged
    ):
        self.footer.display = event.value

    @on(SettingsPane.SoftWrapChanged)
    def on_settings_pane_soft_wrap_changed(
        self, event: SettingsPane.SoftWrapChanged
    ):
        for area in self.board.areas:
            area.soft_wrap = event.value

    @on(SettingsPane.TabBehaviorChanged)
    def on_settings_pane_tab_behavior_changed(
        self, event: SettingsPane.TabBehaviorChanged
    ):
        for area in self.board.areas:
            area.tab_behavior = event.value

    @on(SettingsPane.ShowLineNumbersChanged)
    def on_settings_pane_show_line_numbers_changed(
        self, event: SettingsPane.ShowLineNumbersChanged
    ):
        for area in self.board.areas:
            area.show_line_numbers = event.value

    @on(SettingsPane.MaxCheckpointsChanged)
    def on_settings_pane_max_checkpoints_changed(
        self, event: SettingsPane.MaxCheckpointsChanged
    ):
        max_len = int(event.value)

        for area in self.board.areas:
            area.history.max_checkpoints = max_len
            area.history._undo_stack = deque(
                area.history._undo_stack, maxlen=max_len
            )

    @on(SettingsPane.MatchCursorBracketChanged)
    def on_settings_pane_match_cursor_bracket_changed(
        self, event: SettingsPane.MatchCursorBracketChanged
    ):
        for area in self.board.areas:
            area.match_cursor_bracket = event.value

    @on(SettingsPane.CursorBlinkChanged)
    def on_settings_pane_cursor_blink_changed(
        self, event: SettingsPane.CursorBlinkChanged
    ):
        for area in self.board.areas:
            area.cursor_blink = event.value

    @on(SettingsPane.ShowScrollChanged)
    def on_settings_pane_show_scroll_changed(
        self, event: SettingsPane.ShowScrollChanged
    ):
        for area in chain(self.board.areas, self.tree_view.projects):
            if event.value:
                area.remove_class('hide-scroll')
            else:
                area.add_class('hide-scroll')
        self.refresh_css()

    @on(SettingsPane.TextLineFmtChanged)
    def on_settings_pane_text_line_fmt_changed(
        self, event: SettingsPane.TextLineFmtChanged
    ):
        for pane in self.query(TextPane).results():
            pane.text_line.update()

    @on(DirectoryTree.DeletedPath)
    @work
    async def on_directory_tree_deleted_path(
        self, event: DirectoryTree.DeletedPath
    ):
        path = str(await event.path.resolve())

        for area in self.board.areas:
            area_path = str(await area.path.resolve())
            if area_path != path:
                continue

            message = (
                f'[$accent]{area_path}[/]\n\n'
                'The file is open, do you want to close it?\n'
            )
            if await self.app.push_screen_wait(Confirm('Close file', message)):
                await self.board.remove_area(area.path)

    @on(DirectoryTree.RenamedPath)
    async def on_directory_tree_renamed_path(
        self, event: DirectoryTree.RenamedPath
    ):
        old_path = str(await event.old_path.resolve())
        for area in self.board.areas:
            if str(await area.path.resolve()) == old_path:
                area.update_path(event.path)

    async def _watch_theme(self, theme_name: str) -> None:
        super()._watch_theme(theme_name)
        if theme_name != settings.THEME:
            await settings.save(theme=theme_name)

    # Components

    @property
    def text_area(self) -> TextArea | None:
        """Text area."""
        return self.board.text_area

    @property
    def settings_pane(self) -> SettingsPane | None:
        """Settings pane."""
        with suppress(NoMatches):
            return self.board.query_one(SettingsPane)
