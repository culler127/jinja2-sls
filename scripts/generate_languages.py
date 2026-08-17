#!/usr/bin/env python3
"""Copy shared queries into each language dir and write config.toml / injections.scm."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERIES = ROOT / "queries"
LANGS = ROOT / "languages"

BRACKETS = """\
brackets = [
    { start = "{{", end = "}}", close = true, newline = false },
    { start = "{%", end = "%}", close = true, newline = false },
    { start = "{#", end = "#}", close = true, newline = false },
    { start = "(", end = ")", close = true, newline = false },
    { start = "[", end = "]", close = true, newline = true },
    { start = "{", end = "}", close = true, newline = true },
]
"""

LANGUAGES = [
    {
        "dir": "jinja",
        "name": "Jinja",
        "suffixes": ["njk", "nunjucks", "twig"],
        "injection": None,
        "tab_size": 2,
    },
    {
        "dir": "jinja-html",
        "name": "Jinja HTML",
        "suffixes": ["jinja", "jinja2", "j2", "html.j2", "html.jinja", "html.jinja2"],
        "injection": "html",
        "tab_size": 2,
    },
    {
        "dir": "jinja-css",
        "name": "Jinja CSS",
        "suffixes": ["css.j2", "css.jinja", "css.jinja2"],
        "injection": "css",
        "tab_size": 2,
    },
    {
        "dir": "jinja-json",
        "name": "Jinja JSON",
        "suffixes": ["json.j2", "json.jinja", "json.jinja2"],
        "injection": "json",
        "tab_size": 2,
    },
    {
        "dir": "jinja-md",
        "name": "Jinja Markdown",
        "suffixes": ["md.j2", "md.jinja", "md.jinja2"],
        "injection": "markdown",
        "tab_size": 2,
    },
    {
        "dir": "jinja-yaml",
        "name": "Jinja YAML",
        "suffixes": [
            "yml.j2",
            "yaml.j2",
            "yml.jinja",
            "yaml.jinja",
            "yml.jinja2",
            "yaml.jinja2",
            "sls",
        ],
        "injection": "yaml",
        "tab_size": 2,
    },
    {
        "dir": "jinja-shell",
        "name": "Jinja Shell",
        "suffixes": [
            "sh.j2",
            "bash.j2",
            "zsh.j2",
            "ksh.j2",
            "bashrc.j2",
            "bash_profile.j2",
            "bash_aliases.j2",
            "bash_login.j2",
            "bash_logout.j2",
            "profile.j2",
            "zshrc.j2",
            "zprofile.j2",
            "zlogin.j2",
            "zlogout.j2",
            "zshenv.j2",
            "zsh-theme.j2",
            "env.j2",
            "env.jinja",
            "env.jinja2",
        ],
        "injection": "bash",
        "tab_size": 2,
    },
    {
        "dir": "jinja-py",
        "name": "Jinja Python",
        "suffixes": [
            "py.j2",
            "py.jinja",
            "py.jinja2",
            "pyi.j2",
            "pyi.jinja",
            "pyi.jinja2",
        ],
        "injection": "python",
        "tab_size": 4,
    },
    {
        "dir": "jinja-js",
        "name": "Jinja JavaScript",
        "suffixes": ["js.j2", "js.jinja", "js.jinja2"],
        "injection": "javascript",
        "tab_size": 2,
    },
    {
        "dir": "jinja-ts",
        "name": "Jinja TypeScript",
        "suffixes": ["ts.j2", "ts.jinja", "ts.jinja2"],
        "injection": "typescript",
        "tab_size": 2,
    },
    {
        "dir": "jinja-c",
        "name": "Jinja C",
        "suffixes": ["c.j2", "c.jinja", "c.jinja2"],
        "injection": "c",
        "tab_size": 4,
    },
    {
        "dir": "jinja-cpp",
        "name": "Jinja C++",
        "suffixes": [
            "cpp.j2",
            "h.j2",
            "hpp.j2",
            "cc.j2",
            "cxx.j2",
            "cpp.jinja",
            "h.jinja",
            "hpp.jinja",
            "cpp.jinja2",
            "h.jinja2",
            "hpp.jinja2",
        ],
        "injection": "cpp",
        "tab_size": 4,
    },
    {
        "dir": "jinja-rust",
        "name": "Jinja Rust",
        "suffixes": ["rs.j2", "rs.jinja", "rs.jinja2"],
        "injection": "rust",
        "tab_size": 4,
    },
    {
        "dir": "jinja-xml",
        "name": "Jinja XML",
        "suffixes": ["xml.j2", "xml.jinja", "xml.jinja2"],
        "injection": "xml",
        "tab_size": 2,
        "needs_host_extension": "xml",
    },
    {
        "dir": "jinja-toml",
        "name": "Jinja TOML",
        "suffixes": ["toml.j2", "toml.jinja", "toml.jinja2"],
        "injection": "toml",
        "tab_size": 2,
        "needs_host_extension": "toml",
    },
    {
        "dir": "jinja-sql",
        "name": "Jinja SQL",
        "suffixes": ["sql.j2", "sql.jinja", "sql.jinja2"],
        "injection": "sql",
        "tab_size": 2,
        "needs_host_extension": "sql",
    },
    {
        "dir": "jinja-dockerfile",
        "name": "Jinja Dockerfile",
        "suffixes": ["dockerfile.j2", "dockerfile.jinja", "dockerfile.jinja2"],
        "injection": "dockerfile",
        "tab_size": 2,
        "needs_host_extension": "dockerfile",
    },
    {
        "dir": "jinja-php",
        "name": "Jinja PHP",
        "suffixes": ["php.j2", "php.jinja", "php.jinja2"],
        "injection": "php",
        "tab_size": 4,
        "needs_host_extension": "php",
    },
    {
        "dir": "jinja-java",
        "name": "Jinja Java",
        "suffixes": ["java.j2", "java.jinja", "java.jinja2"],
        "injection": "java",
        "tab_size": 4,
        "needs_host_extension": "java",
    },
    {
        "dir": "jinja-lua",
        "name": "Jinja Lua",
        "suffixes": ["lua.j2", "lua.jinja", "lua.jinja2"],
        "injection": "lua",
        "tab_size": 2,
        "needs_host_extension": "lua",
    },
]


def toml_list(values: list[str]) -> str:
    inner = ", ".join(f'"{v}"' for v in values)
    return f"[{inner}]"


def write_language(spec: dict) -> None:
    dest = LANGS / spec["dir"]
    dest.mkdir(parents=True, exist_ok=True)

    for name in ("highlights.scm", "brackets.scm", "indents.scm", "outline.scm"):
        (dest / name).write_text((QUERIES / name).read_text(), encoding="utf-8")

    suffixes = toml_list(spec["suffixes"])
    config = f'''name = "{spec["name"]}"
grammar = "jinja"
path_suffixes = {suffixes}
tab_size = {spec["tab_size"]}
block_comment = {{ start = "{{#", prefix = "", end = "#}}", tab_size = 0 }}
{BRACKETS}'''
    (dest / "config.toml").write_text(config, encoding="utf-8")

    injection = spec.get("injection")
    if injection:
        (dest / "injections.scm").write_text(
            f"""((text) @injection.content
 (#set! injection.language "{injection}")
 (#set! injection.combined))
""",
            encoding="utf-8",
        )


def main() -> None:
    LANGS.mkdir(parents=True, exist_ok=True)
    for spec in LANGUAGES:
        write_language(spec)
    print(f"wrote {len(LANGUAGES)} languages")


if __name__ == "__main__":
    main()
