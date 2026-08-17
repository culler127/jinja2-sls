# Jinja2 SLS Template Support

Zed extension for Jinja (and Nunjucks / Twig / Tera) templates, with host-language highlighting.

This is a tree-sitter port of [samuelcolvin/jinjahtml-vscode](https://github.com/samuelcolvin/jinjahtml-vscode) (Better Jinja). It uses one Jinja parser ([tree-sitter-jinja-dialects](https://github.com/bennypowers/tree-sitter-jinja-dialects)) and injects the host language into `text` nodes.

Language coverage matches Better Jinja 0.20.0 (plus Salt `.sls`, Nunjucks/Twig, and a separate Jinja C language). Host highlighting is included: languages that Zed already ships (YAML, Python, CSS, …) are injected into those built-in grammars; everything else is bundled as a hidden language so it works without installing extra marketplace extensions.

## Why not `jinja2` / `html-jinja`?

The marketplace already has:

| Extension | Approach | Coverage |
| --- | --- | --- |
| [`jinja2`](https://github.com/ArcherHume/jinja2-support) | Jinja-first → inject HTML | `.jinja` / `.jinja2` / `.j2` + HTML only |
| [`html-jinja`](https://github.com/JaagupAverin/html-jinja) | HTML-first → inject Jinja | HTML + the same suffixes |

`jinja2` has not been updated since 2024, so this is a separate extension (`jinja2-sls`) rather than a fork. If this extension is installed next to `jinja2` or `html-jinja`, disable one of them: they all claim `.jinja` / `.j2`. `.sls` does not conflict.

## File associations

Compound suffixes such as `.yaml.j2` win over a bare `.j2` (Zed picks the longest match). Bare `.j2` is Jinja HTML.

| Language | Suffixes | Host highlighting |
| --- | --- | --- |
| Jinja YAML | `.yml.j2`, `.yaml.j2`, `.yml.jinja`, `.yaml.jinja`, `.yml.jinja2`, `.yaml.jinja2`, **`.sls`** | YAML (Zed built-in) |
| Jinja HTML | `.jinja`, `.jinja2`, `.j2`, `.html.j2`, `.html.jinja`, `.html.jinja2` | HTML (bundled) |
| Jinja Markdown | `.md.j2`, `.md.jinja`, `.md.jinja2` | Markdown (Zed built-in) |
| Jinja Python | `.py.j2`, `.py.jinja`, `.py.jinja2`, `.pyi.j2`, … | Python (Zed built-in) |
| Jinja Cython | `.pyx.j2`, `.pxd.j2`, `.pxi.j2`, … | Python (Zed built-in) |
| Jinja CSS | `.css.j2`, `.css.jinja`, `.css.jinja2` | CSS (Zed built-in) |
| Jinja JSON | `.json.j2`, `.json.jinja`, `.json.jinja2`, `.code-workspace.j2`, … | JSON (Zed built-in) |
| Jinja JavaScript | `.js.j2`, `.js.jinja`, `.js.jinja2` | JavaScript (Zed built-in) |
| Jinja TypeScript | `.ts.j2`, `.ts.jinja`, `.ts.jinja2` | TypeScript (Zed built-in) |
| Jinja C | `.c.j2`, `.c.jinja`, `.c.jinja2` | C (Zed built-in) |
| Jinja C++ | `.cpp.j2`, `.h.j2`, `.hpp.j2`, `.cc.j2`, `.cxx.j2`, … | C++ (Zed built-in) |
| Jinja Rust | `.rs.j2`, `.rs.jinja`, `.rs.jinja2` | Rust (Zed built-in) |
| Jinja Shell | `.sh.j2`, `.bash.j2`, `.zsh.j2`, `.env.j2`, `.ebuild.j2`, … | Shell Script (Zed built-in) |
| Jinja (raw) | `.njk`, `.nunjucks`, `.twig` | none |
| Jinja XML | `.xml.j2`, `.xml.jinja`, `.xml.jinja2` | XML (bundled) |
| Jinja TOML | `.toml.j2`, `.toml.jinja`, `.toml.jinja2` | TOML (bundled) |
| Jinja SQL | `.sql.j2`, `.sql.jinja`, `.sql.jinja2` | SQL (bundled) |
| Jinja Dockerfile | `.dockerfile.j2`, `Dockerfile.j2`, … | Dockerfile (bundled) |
| Jinja PHP | `.php.j2`, `.php.jinja`, `.php.jinja2` | PHP (bundled) |
| Jinja Java | `.java.j2`, `.java.jinja`, `.java.jinja2` | Java (bundled) |
| Jinja Lua | `.lua.j2`, `.lua.jinja`, `.lua.jinja2` | Lua (bundled) |
| Jinja Ruby | `.rb.j2`, `.rbw.j2`, `.rb.jinja2`, … | Ruby (bundled) |
| Jinja LaTeX | `.tex.j2`, `.latex.j2`, `.tex.jinja2`, … | LaTeX (bundled) |
| Jinja Properties | `.properties.j2`, `.cfg.j2`, `.ini.j2`, `.desktop.j2`, `.directory.j2` | INI (bundled) |
| Jinja Nginx | `.conf.j2`, `.conf.jinja`, `.conf.jinja2` | Nginx (bundled) |
| Jinja Terraform | `.tf.j2`, `.tfvars.j2`, `.hcl.j2`, … | HCL (bundled) |
| Jinja Groovy | `.groovy.j2`, `.groovy.jinja`, `.groovy.jinja2` | Groovy (bundled) |
| Jinja Systemd | `.service.j2`, `.timer.j2`, `.mount.j2`, … | INI (bundled) |
| Jinja Cisco Config | `.ios.j2`, `.cisco.j2`, … | Cisco IOS (bundled) |

Jinja delimiters highlight in every associated file. First install compiles extra WASM grammars for the bundled hosts and can take a while.

VS Code maps `.c.j2` to Jinja C++; here it is Jinja C so the host injection can be C rather than C++. VS Code lists `.conf.j2` on both Properties and Nginx; here `.conf.j2` is Jinja Nginx (`.ini.j2` / `.cfg.j2` stay Properties). Cython templates use the Python grammar (same approach as injecting a host that understands the overlapping syntax).

### Jinja LaTeX delimiters

Better Jinja uses Jupyter nbconvert delimiters (`((*` / `*))`, `(((` / `)))`, `((=` / `=))`) because `{%` clashes with LaTeX. Auto-close pairs are set up for those. The tree-sitter grammar still parses standard `{{` / `{%` / `{#`; nbconvert-style tags are not parsed as Jinja yet. LaTeX host highlighting still applies to the rest of the file.

## Development

In Zed: **Install Dev Extension** (command palette: `zed: install dev extension`) and point it at this repository. That compiles the grammar WASM, including the external scanner for `raw` / `verbatim` and comments, plus the bundled host grammars.

Useful commands while testing: `editor: open syntax tree`, `zed: open log`.

Shared Tree-sitter queries live in `queries/`. After editing them (or host pins in the generator), regenerate:

```bash
python3 scripts/generate_languages.py
```

## License

[MIT](LICENSE)
