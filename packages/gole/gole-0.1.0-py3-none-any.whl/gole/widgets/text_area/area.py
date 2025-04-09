from __future__ import annotations

from aiopath import AsyncPath
from rich.console import RenderableType
from textual.document._edit import Edit
from textual.events import Key, Mount
from textual.theme import Theme
from textual.widgets import TextArea as _TextArea
from textual.widgets.text_area import Selection

from gole.config import settings
from gole.widgets.text_area.binding import BINDINGS
from gole.widgets.text_area.language import get_language


class TextArea(_TextArea, inherit_bindings=False):
    BINDINGS = BINDINGS

    class Saved(_TextArea.Changed):
        """Post message on save text area"""

    def __init__(
        self,
        text: str = '',
        language: str = 'markdown',
        path: AsyncPath | None = None,
        *,
        read_only: bool = False,
        line_number_start: int = 1,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        tooltip: RenderableType | None = None,
    ):
        super().__init__(
            text,
            language=language,
            theme=settings.THEME,
            soft_wrap=settings.SOFT_WRAP,
            tab_behavior=settings.TAB_BEHAVIOR,
            show_line_numbers=settings.SHOW_LINE_NUMBERS,
            max_checkpoints=settings.MAX_CHECKPOINTS,
            read_only=read_only,
            line_number_start=line_number_start,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            tooltip=tooltip,
        )
        self.match_cursor_bracket = settings.MATCH_CURSOR_BRACKET
        self.cursor_blink = settings.CURSOR_BLINK

        self.path: AsyncPath | None = path
        self.recorded_text: str = text

    async def _on_mount(self, event: Mount) -> None:
        super()._on_mount(event)
        if self.path:
            path = await self.path.resolve()
            if await path.exists():
                self.text = await path.read_text()
            self.language = get_language(path.name)

        self.recorded_text = self.text

        self.on_theme_change(self.app.current_theme)
        self.app.theme_changed_signal.subscribe(self, self.on_theme_change)

        if not settings.SHOW_SCROLL:
            self.add_class('hide-scroll')

        self.post_message(self.Changed(self))

    def on_theme_change(self, theme: Theme):
        self.theme = theme.name

    # Comment

    def _has_comment(self, text: str, template: str) -> bool:
        template_schema = template.split('{}')
        before, after = (
            template_schema
            if len(template_schema) == 2
            else (template_schema[0], '')
        )

        lines = [
            line.strip().startswith(before) and line.rstrip().endswith(after)
            for line in text.splitlines(keepends=True)
            if line.strip()
        ]
        return all(lines)

    def _uncomment_selection(self, line: str, template: str, depth: int):
        template_schema = template.split('{}')
        before, after = (
            template_schema
            if len(template_schema) == 2
            else (template_schema[0], '')
        )

        line = line.replace(before, '', 1)
        return line[::-1].replace(after[::-1], '', 1)[::-1]

    def _get_chars_before(self, word: str) -> tuple[str, str]:
        index = 0
        if words := word.strip().split():
            index = word.index(words[0][0])

        return word[:index], word[index:]

    def _get_depth(self, text: str) -> int:
        return min(
            len(chars[0])
            for line in text.splitlines(keepends=True)
            if (chars := self._get_chars_before(line)) and chars[1].strip()
        )

    def _comment_selection(self, line: str, template: str, depth: int):
        newline = self.document.newline

        before, line = line[:depth], line[depth:]
        template = before + template

        if line.endswith(newline):
            line = line.removesuffix(newline)
            template += newline

        return template.format(line)

    def _comment(self, text: str):
        template = settings.LANGUAGE.get(self.language, default={}).get(
            'comment', default='# {}'
        )

        commenter = (
            self._uncomment_selection
            if self._has_comment(text, template)
            else self._comment_selection
        )

        depth = self._get_depth(text)

        return ''.join(
            commenter(line, template, depth) if line.strip() else line
            for line in text.splitlines(keepends=True)
        )

    def action_comment_section(self):
        """Comment out selected section or current line."""
        start, end = sorted((self.selection.start, self.selection.end))
        start_line, _ = start
        end_line, _ = end

        if start == end:
            end_line = start_line
            end_column = len(self.get_line(start_line))
        else:
            end_column = len(self.get_line(end_line))

        tabs = []
        for line in range(start_line, end_line):
            tabs.append(self.wrapped_document.get_tab_widths(line))

        text = self.get_text_range((start_line, 0), (end_line, end_column))

        return self.edit(
            Edit(
                self._comment(text),
                (start_line, 0),
                (end_line, end_column),
                True,
            ),
        )

    def update_path(self, path: AsyncPath):
        """Update path, language and post the message `TextArea.Changed`."""
        self.path = path
        self.language = get_language(path.name)
        self.post_message(self.Changed(self))

    async def _on_key(self, event: Key) -> None:
        pairs = {
            '(': '()',
            '[': '[]',
            '{': '{}',
            '<': '<>',
            "'": "''",
            '"': '""',
            '´': '´´',
            '`': '``',
        }

        if (pair := pairs.get(event.character)) and (
            text := self.selected_text
        ):
            event.prevent_default()
            self.replace(pair[0] + text + pair[1], *self.selection)
            return

        if settings.CLOSE_AUTOMATIC_PAIRS and event.character and pair:
            self.insert(pair)
            self.move_cursor_relative(columns=-1)
            event.prevent_default()
            return

        await super()._on_key(event)

    async def action_save(self):
        """Save file (create if not exists)."""
        if not await self.path.exists():
            if not await self.path.parent.exists():
                await self.path.parent.mkdir(parents=True)
            await self.path.touch()
        await self.path.write_text(self.text)

        self.recorded_text = self.text
        self.post_message(self.Saved(self))

    def action_copy(self) -> None:
        """Copy selection to clipboard."""
        if not (text := self.selected_text):
            text = self.document.get_line(self.cursor_location[0])
        self.app.copy_to_clipboard(text)

    def action_indent_section(self) -> None:
        """Indent line/selection."""
        if self.indent_type == 'tabs':
            indent = 1
            indent_value = '\t'
        else:
            indent = self.indent_width
            indent_value = ' ' * indent

        if selected_text := self.selected_text:
            # indent selection
            text = ''.join(
                indent_value + line if line.strip() else line
                for line in selected_text.splitlines(keepends=True)
            )
            self.replace(text, *self.selection)
        else:
            # indent line
            line, column = self.cursor_location
            self.insert(indent_value, (line, 0))
            self.selection = Selection.cursor((line, column + indent))

    def action_outdent_section(self) -> None:
        """Outdent line/selection."""
        if self.indent_type == 'tabs':
            indent = 1
            indent_value = '\t'
        else:
            indent = self.indent_width
            indent_value = ' ' * indent

        if selected_text := self.selected_text:
            # outdent selection
            text = selected_text
            text = ''.join(
                line.removeprefix(indent_value) if line.strip() else line
                for line in selected_text.splitlines(keepends=True)
            )
            self.replace(text, *self.selection)
        else:
            # outdent line
            line, column = self.cursor_location
            text = self.document[line]
            self.replace(
                text.removeprefix(indent_value),
                (line, 0),
                (line, len(text)),
                maintain_selection_offset=False,
            )
            self.selection = Selection.cursor((line, column - indent))

    def action_duplicate_section(self) -> None:
        """Duplicate selected section or current line."""
        if text := self.selected_text:
            return self._duplicate_selection(text)
        self._duplicate_line()

    def _duplicate_selection(self, text: str) -> None:
        location = (self.selection.end[0] + 1, 0)
        result = self.insert(text, location, maintain_selection_offset=False)

        self.selection = Selection(location, result.end_location)

    def _duplicate_line(self) -> None:
        line, column = self.cursor_location
        text = self.document[line] + self.document.newline

        location = (self.selection.end[0], 0)
        result = self.insert(text, location, maintain_selection_offset=False)

        self.selection = Selection.cursor((result.end_location[0], column))

    @property
    def unsaved(self) -> bool:
        return self.recorded_text != self.text
