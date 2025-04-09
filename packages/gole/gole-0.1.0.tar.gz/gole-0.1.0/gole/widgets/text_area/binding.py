from textual.binding import Binding, BindingType

# TODO: pegar do settings
BINDINGS: list[BindingType] = [
    Binding('up', 'cursor_up', 'Cursor up', show=False),
    Binding('down', 'cursor_down', 'Cursor down', show=False),
    Binding('left', 'cursor_left', 'Cursor left', show=False),
    Binding('right', 'cursor_right', 'Cursor right', show=False),
    Binding('ctrl+left', 'cursor_word_left', 'Cursor word left', show=False),
    Binding(
        'ctrl+right', 'cursor_word_right', 'Cursor word right', show=False
    ),
    Binding('home', 'cursor_line_start', 'Cursor line start', show=False),
    Binding('end', 'cursor_line_end', 'Cursor line end', show=False),
    Binding('pageup', 'cursor_page_up', 'Cursor page up', show=False),
    Binding('pagedown', 'cursor_page_down', 'Cursor page down', show=False),
    # Making selections (generally holding the shift key and moving cursor)
    Binding(
        'ctrl+shift+left',
        'cursor_word_left(True)',
        'Cursor left word select',
        show=False,
    ),
    Binding(
        'ctrl+shift+right',
        'cursor_word_right(True)',
        'Cursor right word select',
        show=False,
    ),
    Binding(
        'shift+home',
        'cursor_line_start(True)',
        'Cursor line start select',
        show=False,
    ),
    Binding(
        'shift+end',
        'cursor_line_end(True)',
        'Cursor line end select',
        show=False,
    ),
    Binding('shift+up', 'cursor_up(True)', 'Cursor up select', show=False),
    Binding(
        'shift+down', 'cursor_down(True)', 'Cursor down select', show=False
    ),
    Binding(
        'shift+left', 'cursor_left(True)', 'Cursor left select', show=False
    ),
    Binding(
        'shift+right',
        'cursor_right(True)',
        'Cursor right select',
        show=False,
    ),
    # Shortcut ways of making selections
    # Binding('f5', 'select_word', 'select word', show=False),
    Binding('f6', 'select_line', 'Select line', show=False),
    Binding('f7,ctrl+a', 'select_all', 'Select all', show=False),
    # Deletion
    Binding('backspace', 'delete_left', 'Delete character left', show=False),
    Binding(
        'delete',
        'delete_right',
        'Delete character right',
        show=False,
    ),
    Binding(
        'ctrl+f',
        'delete_word_right',
        'Delete right to start of word',
        show=False,
    ),
    Binding(
        'ctrl+u',
        'delete_to_start_of_line',
        'Delete to line start',
        show=False,
    ),
    Binding(
        'alt+backspace',
        'delete_word_left',
        'Delete the left word',
        show=False,
    ),
    Binding(
        'ctrl+k',
        'delete_to_end_of_line_or_delete_line',
        'Delete to line end',
        show=False,
    ),
    Binding(
        'ctrl+shift+k',
        'delete_line',
        'Delete line',
        show=False,
    ),
    Binding(
        'ctrl+shift+d',
        'duplicate_section',
        'Duplicate section',
        show=False,
    ),
    Binding('ctrl+slash', 'comment_section', 'Comment section', show=False),
    Binding(
        'alt+right_square_bracket',
        'indent_section',
        'Indent section',
        show=False,
    ),
    Binding(
        'alt+left_square_bracket',
        'outdent_section',
        'Outdent section',
        show=False,
    ),
    # Showing
    Binding(
        'ctrl+s',
        'save',
        'Save',
        tooltip='Save the file.',
    ),
    Binding(
        'ctrl+c',
        'copy',
        'Copy',
        tooltip='Copy selected content.',
    ),
    Binding(
        'ctrl+v',
        'paste',
        'Paste',
        tooltip='Paste the copied content.',
    ),
    Binding(
        'ctrl+z',
        'undo',
        'Undo',
        tooltip='Revert the last change.',
    ),
    Binding(
        'ctrl+y,ctrl+shift+z',
        'redo',
        'Redo',
        tooltip=('The change comes back.'),
    ),
    Binding(
        'ctrl+x',
        'cut',
        'Cut',
        tooltip='Cut current line.',
    ),
]
