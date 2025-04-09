import re

DEFAULT_LANGUAGES = {
    'python': r'\.(py[23cdioxw]?|xsh|xonshrc)$',
    'json': r'\.json$',
    'markdown': r'\.((live)?mk?d|mkdn|rmd|markdown|mdx)$',
    'yaml': r'\.ya?ml$',
    'toml': r'\.toml$',
    'rust': r'\.rs(lib)?$',
    'html': r'\.html?[45]?$',
    'css': r'\.(t?css|less)$',
    'xml': r'\.(xml|sgml?|rng|svg|plist)$',
    'regex': r'\.regex$',
    'sql': r'\.sql$',
    'javascript': r'\.(m?js|es[5678]?)$',
    'java': r'\.java$',
    'bash': (
        r'(^(APK|PKG)BUILD|(Pkgfile|(pkgmk|rc)\\.conf)|'
        r'^\.bash_(aliases|functions|profile|history|logout)|\.(ba|z)shrc|'
        r'\.(ebuild|profile)|\.(a|c|k|z|ba|fi)?sh|'
        r'\.z(shenv|profile|login|logout))$'
    ),
    'go': r'(\.go(doc|lo)?|^go\.(mod|sum))$',
}


def get_language(file_name: str) -> str:
    for language, pattern in DEFAULT_LANGUAGES.items():
        if re.search(pattern, file_name):
            return language
    return 'markdown'
