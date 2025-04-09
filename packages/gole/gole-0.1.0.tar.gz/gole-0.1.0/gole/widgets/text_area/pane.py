from __future__ import annotations

import re
import unicodedata
from contextlib import suppress
from uuid import uuid4

from aiopath import AsyncPath
from textual import on
from textual.app import ComposeResult
from textual.css.query import NoMatches
from textual.widget import Widget
from textual.widgets import Label, TabPane
from textual.widgets._label import LabelVariant
from textual.widgets.tabbed_content import ContentTab

from gole.config import settings
from gole.widgets.text_area.area import TextArea


def normalize(text: str) -> str:
    normalized = unicodedata.normalize('NFD', text).encode('ascii', 'ignore')
    pattern = r'(/|\s|\+|\.)+'
    return re.sub(pattern, '-', normalized.decode('utf-8').lower())


class TextLine(Label):
    def __init__(
        self,
        area: TextArea,
        *,
        variant: LabelVariant | None = None,
        expand: bool = False,
        shrink: bool = False,
        markup: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        self.area: TextArea = area

        super().__init__(
            self._render_line(),
            variant=variant,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    def _render_line(self) -> str:
        # content = '{title}   {line}:{column}/{num_lines}'
        content = settings.TEXT_LINE_FMT

        name = str(self.area.path)
        if self.area.unsaved:
            name = f'[$warning]{name} *[/]'

        _, end = self.area.selection
        line, column = end

        args = {
            'name': name,
            'line': line + 1,
            'column': column,
            'num_lines': self.area.document.line_count,
        }
        for key, value in args.items():
            content = content.replace('{' + key + '}', str(value))
        return content

    def update(self) -> None:
        return super().update(self._render_line())


class TextPane(TabPane):

    def __init__(
        self,
        path: AsyncPath | None = None,
        *children: Widget,
        name: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        title = path.name if path else r'\[sketch]'

        path_id = str(path) if path else uuid4().hex
        _id = f'path-{normalize(path_id)}'

        self.area: TextArea = TextArea(path=path, id=_id)
        super().__init__(
            title,
            self.area,
            name=name,
            id=self.area.id,
            classes=classes,
            disabled=disabled,
        )

        self.path: AsyncPath | None = path

    def compose(self) -> ComposeResult:
        yield TextLine(self.area)

    def on_text_pane_focused(self, event: TextPane.Focused):
        self.area.focus()

    @on(TextArea.SelectionChanged)
    def _update_footer(self):
        self.text_line.update()

    @on(TextArea.Changed)
    @on(TextArea.Saved)
    def _update_title(self, event: TextArea.Changed | TextArea.Saved):
        area = event.text_area

        title = area.path.name
        if area.unsaved:
            title = f'[$error]{title} *[/]'

        with suppress(NoMatches):
            self.app.board.query_one(
                f'#--content-tab-{area.id}', ContentTab
            ).label = title

        self.text_line.update()

    @property
    def text_line(self) -> TextLine:
        return self.query_one(TextLine)
