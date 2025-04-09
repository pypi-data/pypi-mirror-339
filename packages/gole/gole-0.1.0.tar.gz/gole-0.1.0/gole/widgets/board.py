import asyncio
from collections.abc import Iterable
from typing import ClassVar

from aiopath import AsyncPath
from textual.binding import Binding, BindingType
from textual.content import ContentType
from textual.css.query import NoMatches
from textual.widgets import TabbedContent

from gole.dialogs.confirm import Confirm
from gole.widgets.text_area import TextArea, TextPane


class Board(TabbedContent):
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding(
            'ctrl+w',
            'close_tab',
            'Close',
            tooltip='Close current pane.',
        ),
    ]

    def __init__(
        self,
        *titles: ContentType,
        path: AsyncPath | None = None,
        initial: str = "",
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        super().__init__(
            *titles,
            initial=initial,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.path: AsyncPath | None = path

    async def action_close_tab(self):
        try:
            area = self.query_one(f'#{self.active}', TextArea)
        except NoMatches:
            return await self._remove_active_pane()

        if not area.unsaved:
            return await self._remove_active_pane()

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
        self.app.push_screen(
            screen, lambda yes: self._remove_active_pane() if yes else None
        )

    async def _remove_active_pane(self):
        return await self.remove_pane(self.active)

    async def action_add_text_pane(self, file_path: AsyncPath | None = None):
        pane = TextPane(path=file_path)

        try:
            pane = self.get_pane(pane.id)
        except NoMatches:
            await self.add_pane(pane)
        self.active = pane.id
        pane.area.focus()

    async def action_save_all(self):
        await asyncio.gather(*[area.action_save() for area in self.unsaved])

    async def remove_area(self, path: AsyncPath):
        path_str = str(await path.resolve())
        for area in self.areas:
            if str(await area.path.resolve()) == path_str:
                self.remove_pane(area.id)

    @property
    def text_area(self) -> TextArea | None:
        if not (_id := self.active):
            return

        pane = self.get_pane(_id)
        if isinstance(pane, TextPane):
            return pane.area

    @property
    def areas(self) -> Iterable[TextArea]:
        return self.query(TextArea).results()

    @property
    def unsaved(self) -> list[TextArea]:
        return [area for area in self.areas if area.unsaved]
