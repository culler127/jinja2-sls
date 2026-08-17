#!/usr/bin/env python3
"""Generate language dirs, host injection languages, and extension.toml.

Language list and suffixes follow samuelcolvin/jinjahtml-vscode (Better Jinja) 0.20.0.

Host highlighting for languages that are not built into the Zed binary is
provided by hidden languages (``hidden = true``). The hidden language names
are unique (``jinja-host-*``), while grammar keys use the upstream parser
names (``html``, ``xml``, etc.) required by Zed's WASM linker. Highlight
queries are copied from ``queries/hosts/``.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERIES = ROOT / "queries"
LANGS = ROOT / "languages"

# Do not auto-close a lone `{` — it fights `{{` / `{%` (see zed#23711).
JINJA_BRACKETS = """\
autoclose_before = "}])>"
collapsed_placeholder = "{# ... #}"
brackets = [
    { start = "{{", end = "}}", close = true, newline = false, not_in = ["string", "comment"] },
    { start = "{%", end = "%}", close = true, newline = false, not_in = ["string", "comment"] },
    { start = "{#", end = "#}", close = true, newline = false, not_in = ["string", "comment"] },
    { start = "(", end = ")", close = true, newline = false, not_in = ["string", "comment"] },
    { start = "[", end = "]", close = true, newline = true, not_in = ["string", "comment"] },
    { start = '"', end = '"', close = true, newline = false, not_in = ["string", "comment"] },
    { start = "'", end = "'", close = true, newline = false, not_in = ["string", "comment"] },
]
"""

# Jupyter nbconvert / VS Code Jinja LaTeX delimiters (grammar still parses {{/%/#).
LATEX_BRACKETS = """\
autoclose_before = "}])>"
collapsed_placeholder = "((= ... =))"
brackets = [
    { start = "(((", end = ")))", close = true, newline = false, not_in = ["string", "comment"] },
    { start = "((*" , end = "*))", close = true, newline = false, not_in = ["string", "comment"] },
    { start = "((=", end = "=))", close = true, newline = false, not_in = ["string", "comment"] },
    { start = "{{", end = "}}", close = true, newline = false, not_in = ["string", "comment"] },
    { start = "{%", end = "%}", close = true, newline = false, not_in = ["string", "comment"] },
    { start = "{#", end = "#}", close = true, newline = false, not_in = ["string", "comment"] },
    { start = "(", end = ")", close = true, newline = false, not_in = ["string", "comment"] },
    { start = "[", end = "]", close = true, newline = true, not_in = ["string", "comment"] },
    { start = '"', end = '"', close = true, newline = false, not_in = ["string", "comment"] },
    { start = "'", end = "'", close = true, newline = false, not_in = ["string", "comment"] },
]
"""

QUERY_FILES = (
    "highlights.scm",
    "brackets.scm",
    "indents.scm",
    "outline.scm",
    "overrides.scm",
    "textobjects.scm",
)

# Grammars that Zed does not ship in crates/languages. `key` is the unique
# hidden language name; `grammar` must exactly match the upstream
# `tree_sitter_<grammar>` C symbol and therefore must be snake_case.
# Pins match the official Zed extensions as of 2026-08. Registering the same
# grammar name as a separately installed host extension is intentional; pins
# are kept aligned to minimize that interoperability risk.
BUNDLED_HOSTS = [
    {
        "key": "jinja-host-html",
        "grammar": "html",
        "repository": "https://github.com/tree-sitter/tree-sitter-html",
        "rev": "bfa075d83c6b97cd48440b3829ab8d24a2319809",
        "highlights": "html.scm",
        "injections": "html-injections.scm",
    },
    {
        "key": "jinja-host-xml",
        "grammar": "xml",
        "repository": "https://github.com/tree-sitter-grammars/tree-sitter-xml",
        "rev": "5000ae8f22d11fbe93939b05c1e37cf21117162d",
        "path": "xml",
        "highlights": "xml.scm",
    },
    {
        "key": "jinja-host-ruby",
        "grammar": "ruby",
        "repository": "https://github.com/tree-sitter/tree-sitter-ruby",
        "rev": "71bd32fb7607035768799732addba884a37a6210",
        "highlights": "ruby.scm",
    },
    {
        "key": "jinja-host-toml",
        "grammar": "toml",
        "repository": "https://github.com/tree-sitter/tree-sitter-toml",
        "rev": "342d9be207c2dba869b9967124c679b5e6fd0ebe",
        "highlights": "toml.scm",
    },
    {
        "key": "jinja-host-latex",
        "grammar": "latex",
        "repository": "https://github.com/497e0bdf29873/tree-sitter-latex",
        "rev": "858af2c24547c8ab9386281ece6ead6936dbc8d1",
        "highlights": "latex.scm",
    },
    {
        "key": "jinja-host-lua",
        "grammar": "lua",
        "repository": "https://github.com/tree-sitter-grammars/tree-sitter-lua",
        "rev": "10fe0054734eec83049514ea2e718b2a56acd0c9",
        "highlights": "lua.scm",
    },
    {
        "key": "jinja-host-ini",
        "grammar": "ini",
        "repository": "https://github.com/justinmk/tree-sitter-ini",
        "rev": "e4018b5176132b4f3c5d6e61cea383f42288d0f5",
        "highlights": "ini.scm",
    },
    {
        "key": "jinja-host-dockerfile",
        "grammar": "dockerfile",
        "repository": "https://github.com/camdencheek/tree-sitter-dockerfile",
        "rev": "868e44ce378deb68aac902a9db68ff82d2299dd0",
        "highlights": "dockerfile.scm",
    },
    {
        "key": "jinja-host-sql",
        "grammar": "sql",
        "repository": "https://github.com/DerekStride/tree-sitter-sql",
        "rev": "851e9cb257ba7c66cc8c14214a31c44d2f1e954e",
        "highlights": "sql.scm",
    },
    {
        "key": "jinja-host-hcl",
        "grammar": "hcl",
        "repository": "https://github.com/tree-sitter-grammars/tree-sitter-hcl",
        "rev": "fad991865fee927dd1de5e172fb3f08ac674d914",
        "highlights": "hcl.scm",
    },
    {
        "key": "jinja-host-nginx",
        "grammar": "nginx",
        "repository": "https://gitlab.com/joncoole/tree-sitter-nginx",
        "rev": "9413233132d1787aa8d7e8f295ee20b55ba991de",
        "highlights": "nginx.scm",
    },
    {
        "key": "jinja-host-groovy",
        "grammar": "groovy",
        "repository": "https://github.com/murtaza64/tree-sitter-groovy",
        "rev": "86911590a8e46d71301c66468e5620d9faa5b6af",
        "highlights": "groovy.scm",
    },
    {
        "key": "jinja-host-java",
        "grammar": "java",
        "repository": "https://github.com/tree-sitter/tree-sitter-java",
        "rev": "94703d5a6bed02b98e438d7cad1136c01a60ba2c",
        "highlights": "java.scm",
    },
    {
        "key": "jinja-host-php",
        "grammar": "php",
        "repository": "https://github.com/tree-sitter/tree-sitter-php",
        "rev": "5b5627faaa290d89eb3d01b9bf47c3bb9e797dea",
        "path": "php",
        "highlights": "php.scm",
    },
    {
        "key": "jinja-host-cisco",
        "grammar": "cisco_ios_jinja2",
        "repository": "https://github.com/dgethings/tree-sitter-cisco-ios-jinja2",
        "rev": "68003c0097e44727458f9e119480b72b2f4c4f74",
        "highlights": "cisco.scm",
    },
]

EXTENSION_TOML_HEADER = '''# Generated by scripts/generate_languages.py
id = "jinja2-sls"
name = "Jinja2 SLS Template Support"
version = "0.1.0"
schema_version = 1
authors = ["Yauhen Charniauski <culler8026@gmail.com>"]
description = "Jinja template highlighting for Salt SLS, YAML, HTML, Markdown, Python, and more (jinjahtml-vscode port)"
repository = "https://github.com/culler127/jinja2-sls"
'''

JINJA_GRAMMAR = '''
[grammars.jinja]
repository = "https://github.com/bennypowers/tree-sitter-jinja-dialects"
rev = "4f832fe6feeae8c9e5963d835bec0272a8331b47"
'''

SYSTEMD_UNITS = [
    "link",
    "netdev",
    "network",
    "service",
    "socket",
    "device",
    "mount",
    "automount",
    "swap",
    "target",
    "path",
    "timer",
    "snapshot",
    "slice",
    "scope",
]


def j2_family(*stems: str) -> list[str]:
    suffixes: list[str] = []
    for stem in stems:
        suffixes.extend([f"{stem}.j2", f"{stem}.jinja", f"{stem}.jinja2"])
    return suffixes


LANGUAGES = [
    {
        "dir": "jinja",
        "name": "Jinja",
        # VS Code raw jinja has no associations; njk/twig are extra (same grammar).
        "suffixes": ["njk", "nunjucks", "twig"],
        "injection": None,
        "tab_size": 2,
    },
    {
        "dir": "jinja-html",
        "name": "Jinja HTML",
        "suffixes": ["jinja", "jinja2", "j2", "html.j2", "html.jinja", "html.jinja2"],
        "injection": "jinja-host-html",
        "tab_size": 2,
        "word_characters": ["-"],
    },
    {
        "dir": "jinja-xml",
        "name": "Jinja XML",
        "suffixes": j2_family("xml"),
        "injection": "jinja-host-xml",
        "tab_size": 2,
    },
    {
        "dir": "jinja-css",
        "name": "Jinja CSS",
        "suffixes": j2_family("css"),
        "injection": "css",
        "tab_size": 2,
    },
    {
        "dir": "jinja-json",
        "name": "Jinja JSON",
        "suffixes": j2_family("json", "code-workspace"),
        "injection": "json",
        "tab_size": 2,
    },
    {
        "dir": "jinja-md",
        "name": "Jinja Markdown",
        "suffixes": j2_family("md"),
        "injection": "markdown",
        "tab_size": 2,
    },
    {
        "dir": "jinja-py",
        "name": "Jinja Python",
        "suffixes": j2_family("py", "pyi"),
        "injection": "python",
        "tab_size": 4,
    },
    {
        "dir": "jinja-cy",
        "name": "Jinja Cython",
        "suffixes": j2_family("pyx", "pxd", "pxi"),
        "injection": "python",
        "tab_size": 4,
    },
    {
        "dir": "jinja-rb",
        "name": "Jinja Ruby",
        "suffixes": ["rb.j2", "rbw.j2", "rb.jinja", "rbw.jinja", "rb.jinja2", "rbw.jinja2"],
        "injection": "jinja-host-ruby",
        "tab_size": 2,
    },
    {
        "dir": "jinja-js",
        "name": "Jinja JavaScript",
        "suffixes": j2_family("js"),
        "injection": "javascript",
        "tab_size": 2,
    },
    {
        "dir": "jinja-ts",
        "name": "Jinja TypeScript",
        "suffixes": j2_family("ts"),
        "injection": "typescript",
        "tab_size": 2,
    },
    {
        "dir": "jinja-yaml",
        "name": "Jinja YAML",
        "suffixes": j2_family("yml", "yaml") + ["sls"],
        "injection": "yaml",
        "tab_size": 2,
    },
    {
        "dir": "jinja-toml",
        "name": "Jinja TOML",
        "suffixes": j2_family("toml"),
        "injection": "jinja-host-toml",
        "tab_size": 2,
    },
    {
        "dir": "jinja-latex",
        "name": "Jinja LaTeX",
        "suffixes": [
            "latex.j2",
            "tex.j2",
            "latex.jinja",
            "tex.jinja",
            "latex.jinja2",
            "tex.jinja2",
        ],
        "injection": "jinja-host-latex",
        "tab_size": 4,
        "brackets": LATEX_BRACKETS,
        "block_comment": '{ start = "((=", prefix = "", end = "=))", tab_size = 0 }',
    },
    {
        "dir": "jinja-lua",
        "name": "Jinja Lua",
        "suffixes": j2_family("lua"),
        "injection": "jinja-host-lua",
        "tab_size": 2,
    },
    {
        "dir": "jinja-properties",
        "name": "Jinja Properties",
        # `.conf.j2` is claimed by Jinja Nginx (same overlap as VS Code).
        "suffixes": j2_family("properties", "cfg", "ini", "desktop", "directory"),
        "injection": "jinja-host-ini",
        "tab_size": 4,
    },
    {
        "dir": "jinja-shell",
        "name": "Jinja Shell",
        "suffixes": [
            "sh.j2",
            "bash.j2",
            "bashrc.j2",
            "bash_aliases.j2",
            "bash_profile.j2",
            "bash_login.j2",
            "ebuild.j2",
            "install.j2",
            "profile.j2",
            "bash_logout.j2",
            "zsh.j2",
            "zshrc.j2",
            "zprofile.j2",
            "zlogin.j2",
            "zlogout.j2",
            "zshenv.j2",
            "zsh-theme.j2",
            "ksh.j2",
            "env.jinja",
            "env.j2",
            "env.jinja2",
        ],
        "injection": "bash",
        "tab_size": 2,
    },
    {
        "dir": "jinja-dockerfile",
        "name": "Jinja Dockerfile",
        "suffixes": j2_family("dockerfile")
        + ["Dockerfile.j2", "Dockerfile.jinja", "Dockerfile.jinja2"],
        "injection": "jinja-host-dockerfile",
        "tab_size": 2,
    },
    {
        "dir": "jinja-sql",
        "name": "Jinja SQL",
        "suffixes": j2_family("sql"),
        "injection": "jinja-host-sql",
        "tab_size": 2,
    },
    {
        "dir": "jinja-terraform",
        "name": "Jinja Terraform",
        "suffixes": j2_family("tf", "tfvars", "hcl"),
        "injection": "jinja-host-hcl",
        "tab_size": 2,
    },
    {
        "dir": "jinja-nginx",
        "name": "Jinja Nginx",
        "suffixes": j2_family("conf"),
        "injection": "jinja-host-nginx",
        "tab_size": 4,
    },
    {
        "dir": "jinja-groovy",
        "name": "Jinja Groovy",
        "suffixes": j2_family("groovy"),
        "injection": "jinja-host-groovy",
        "tab_size": 4,
    },
    {
        "dir": "jinja-systemd",
        "name": "Jinja Systemd",
        "suffixes": j2_family(*SYSTEMD_UNITS),
        "injection": "jinja-host-ini",
        "tab_size": 2,
    },
    {
        "dir": "jinja-c",
        "name": "Jinja C",
        # VS Code folds .c.j2 into Jinja C++; Zed injects one host per language.
        "suffixes": j2_family("c"),
        "injection": "c",
        "tab_size": 4,
    },
    {
        "dir": "jinja-cpp",
        "name": "Jinja C++",
        "suffixes": j2_family("cpp", "h", "hpp", "cc", "cxx"),
        "injection": "cpp",
        "tab_size": 4,
    },
    {
        "dir": "jinja-cisco",
        "name": "Jinja Cisco Config",
        "suffixes": j2_family("ios", "cisco"),
        "injection": "jinja-host-cisco",
        "tab_size": 4,
    },
    {
        "dir": "jinja-java",
        "name": "Jinja Java",
        "suffixes": j2_family("java"),
        "injection": "jinja-host-java",
        "tab_size": 4,
    },
    {
        "dir": "jinja-php",
        "name": "Jinja PHP",
        "suffixes": j2_family("php"),
        "injection": "jinja-host-php",
        "tab_size": 4,
    },
    {
        "dir": "jinja-rust",
        "name": "Jinja Rust",
        "suffixes": j2_family("rs"),
        "injection": "rust",
        "tab_size": 4,
    },
]


def toml_list(values: list[str]) -> str:
    inner = ", ".join(f'"{v}"' for v in values)
    return f"[{inner}]"


def write_language(spec: dict) -> None:
    dest = LANGS / spec["dir"]
    dest.mkdir(parents=True, exist_ok=True)

    for name in QUERY_FILES:
        (dest / name).write_text((QUERIES / name).read_text(), encoding="utf-8")

    suffixes = toml_list(spec["suffixes"])
    brackets = spec.get("brackets", JINJA_BRACKETS)
    if "block_comment" in spec:
        block_comment = spec["block_comment"]
    else:
        block_comment = '{ start = "{#", prefix = "", end = "#}", tab_size = 0 }'

    extra = ""
    if spec.get("word_characters"):
        extra = f"word_characters = {toml_list(spec['word_characters'])}\n"

    config = f'''name = "{spec["name"]}"
grammar = "jinja"
path_suffixes = {suffixes}
tab_size = {spec["tab_size"]}
block_comment = {block_comment}
{extra}{brackets}'''
    (dest / "config.toml").write_text(config, encoding="utf-8")

    injections_path = dest / "injections.scm"
    injection = spec.get("injection")
    if injection:
        injections_path.write_text(
            f"""((text) @injection.content
 (#set! injection.language "{injection}")
 (#set! injection.combined))
""",
            encoding="utf-8",
        )
    elif injections_path.exists():
        injections_path.unlink()


def write_host_language(host: dict) -> None:
    dest = LANGS / host["key"]
    dest.mkdir(parents=True, exist_ok=True)

    highlights_src = QUERIES / "hosts" / host["highlights"]
    if not highlights_src.is_file():
        raise SystemExit(f"missing host highlights: {highlights_src}")

    (dest / "config.toml").write_text(
        f'''name = "{host["key"]}"
grammar = "{host["grammar"]}"
hidden = true
''',
        encoding="utf-8",
    )
    (dest / "highlights.scm").write_text(
        highlights_src.read_text(encoding="utf-8"), encoding="utf-8"
    )

    keep = {"config.toml", "highlights.scm"}
    injections_name = host.get("injections")
    injections_path = dest / "injections.scm"
    if injections_name:
        injections_src = QUERIES / "hosts" / injections_name
        if not injections_src.is_file():
            raise SystemExit(f"missing host injections: {injections_src}")
        injections_path.write_text(
            injections_src.read_text(encoding="utf-8"), encoding="utf-8"
        )
        keep.add("injections.scm")
    elif injections_path.exists():
        injections_path.unlink()

    for child in dest.iterdir():
        if child.is_file() and child.name not in keep:
            child.unlink()


def write_extension_toml() -> None:
    parts = [EXTENSION_TOML_HEADER, JINJA_GRAMMAR]
    for host in BUNDLED_HOSTS:
        block = (
            f'\n[grammars.{host["grammar"]}]\n'
            f'repository = "{host["repository"]}"\n'
            f'rev = "{host["rev"]}"\n'
        )
        if host.get("path"):
            block += f'path = "{host["path"]}"\n'
        parts.append(block)
    (ROOT / "extension.toml").write_text("".join(parts).lstrip("\n"), encoding="utf-8")


def main() -> None:
    LANGS.mkdir(parents=True, exist_ok=True)
    grammar_names = [host["grammar"] for host in BUNDLED_HOSTS]
    if len(grammar_names) != len(set(grammar_names)):
        raise SystemExit("duplicate bundled grammar name")
    for grammar_name in grammar_names:
        if not grammar_name.isidentifier() or grammar_name.lower() != grammar_name:
            raise SystemExit(f"grammar name must be lowercase snake_case: {grammar_name}")
    wanted = {spec["dir"] for spec in LANGUAGES} | {host["key"] for host in BUNDLED_HOSTS}
    write_extension_toml()
    for spec in LANGUAGES:
        write_language(spec)
    for host in BUNDLED_HOSTS:
        write_host_language(host)
    for child in LANGS.iterdir():
        if child.is_dir() and child.name not in wanted:
            raise SystemExit(f"unexpected language dir: {child}")
    print(
        f"wrote {len(LANGUAGES)} jinja languages and {len(BUNDLED_HOSTS)} bundled hosts"
    )


if __name__ == "__main__":
    main()
