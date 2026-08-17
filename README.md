# Jinja2 SLS Template Support

Zed extension for Jinja (and Nunjucks / Twig / Tera) templates, with host-language highlighting.

This is a tree-sitter port of [samuelcolvin/jinjahtml-vscode](https://github.com/samuelcolvin/jinjahtml-vscode) (Better Jinja). It uses one Jinja parser ([tree-sitter-jinja-dialects](https://github.com/bennypowers/tree-sitter-jinja-dialects)) and injects the host language into `text` nodes.

## Why not `jinja2` / `html-jinja`?

The marketplace already has:

| Extension | Approach | Coverage |
| --- | --- | --- |
| [`jinja2`](https://github.com/ArcherHume/jinja2-support) | Jinja-first → inject HTML | `.jinja` / `.jinja2` / `.j2` + HTML only |
| [`html-jinja`](https://github.com/JaagupAverin/html-jinja) | HTML-first → inject Jinja | HTML + the same suffixes |

`jinja2` has not been updated since 2024 (open issues and a LICENSE PR sit unanswered), so this is a separate extension (`jinja2-sls`) rather than a fork. It covers YAML **including SaltStack `.sls`**, Markdown, Python, SQL, and the other hosts below — not only HTML.

If this extension is installed next to `jinja2` or `html-jinja`, disable one of them: they all claim `.jinja` / `.j2`. `.sls` does not conflict.

## File associations

| Language | Suffixes | Host injection |
| --- | --- | --- |
| Jinja YAML | `.yml.j2`, `.yaml.j2`, `.yml.jinja`, `.yaml.jinja`, `.yml.jinja2`, `.yaml.jinja2`, **`.sls`** | YAML (built-in) |
| Jinja HTML | `.jinja`, `.jinja2`, `.j2`, `.html.j2`, `.html.jinja`, `.html.jinja2` | HTML (built-in) |
| Jinja Markdown | `.md.j2`, `.md.jinja`, `.md.jinja2` | Markdown (built-in) |
| Jinja Python | `.py.j2`, `.py.jinja`, `.py.jinja2`, `.pyi.j2`, … | Python (built-in) |
| Jinja CSS / JSON / JS / TS / C / C++ / Rust / Shell | matching `*.<host>.j2` (and `.jinja` / `.jinja2`) | built-in host |
| Jinja (raw) | `.njk`, `.nunjucks`, `.twig` | none |
| Jinja XML / TOML / SQL / Dockerfile / PHP / Java / Lua | matching host suffixes | needs host extension |

Compound suffixes such as `.yaml.j2` win over a bare `.j2` (Zed picks the longest match). Bare `.j2` is treated as Jinja HTML.

## Host extensions (optional)

Jinja delimiters highlight either way. Host highlighting for these languages needs the matching extension installed:

| Language | Install |
| --- | --- |
| XML | `xml` |
| TOML | `toml` |
| SQL | `sql` |
| Dockerfile | `dockerfile` |
| PHP | `php` |
| Java | `java` |
| Lua | `lua` |

## Development

In Zed: **Install Dev Extension** (command palette: `zed: install dev extension`) and point it at this repository. That compiles the grammar WASM, including the external scanner for `raw` / `verbatim` and comments.

Useful commands while testing: `editor: open syntax tree`, `zed: open log`.

Shared Tree-sitter queries live in `queries/`. After editing them, regenerate per-language copies:

```bash
python3 scripts/generate_languages.py
```

## License

[MIT](LICENSE)
