# Agent notes — jinja2-sls

This file is the working memory for agents. User-facing docs live in `README.md`. If this file and the repo disagree, the repo wins — then update this file.

## What this is

Zed extension: tree-sitter port of [samuelcolvin/jinjahtml-vscode](https://github.com/samuelcolvin/jinjahtml-vscode) (Better Jinja **0.20.0**).

Zed has no TextMate. One Jinja parser highlights delimiters; host language highlighting is Tree-sitter **injections** into Jinja `text` nodes.

Coverage must match Better Jinja 0.20.0 **plus** Salt `.sls`. Do not shrink the language picker to make the extension smaller.

## Identity

| Field | Value |
| --- | --- |
| Marketplace `id` | `jinja2-sls` |
| Display name | Jinja2 SLS Template Support |
| Version | `0.1.0` |
| License | MIT (`LICENSE`) |
| Author | Yauhen Charniauski `<culler8026@gmail.com>` |
| Git remote | `git@github.com:culler127/jinja2-sls.git` |
| Branch | `main` |
| Base | Both implementation PRs are merged into `main` |

Why `jinja2-sls`: user wanted something like `jinj2-sls template-support`; marketplace `id` `jinja2` is already taken.

## Decisions that must not be reversed without the user

1. **Own marketplace extension**, not a fork and not a PR into `ArcherHume/jinja2-support` (Path A abandoned: last push Oct 2024, LICENSE PR and issues unanswered).
2. **Do not PR to ArcherHume.**
3. **Host highlighting is mandatory** for every associated language. Do not tell users to install extra marketplace language extensions. Built-in Zed grammars are reused; everything else is bundled as hidden `jinja-host-*` languages.
4. **Do not drop languages** to shrink the picker.
5. Hidden **language names** must be unique (`jinja-host-xml`), but grammar keys
   must match upstream C symbols (`xml`, `php`, `html`, …). Zed links
   `tree_sitter_<grammar>`, so renamed grammar keys do not compile.
6. **Do not commit unless the user asks.** Do not push unless the user asks.
7. **Do not force-push `main`/`master`.**
8. Extra `queries/` and `scripts/` are maintainer-only; they are not a Zed runtime feature.

## Competing Zed extensions

| Extension | Approach | Conflict |
| --- | --- | --- |
| [`jinja2`](https://github.com/ArcherHume/jinja2-support) | Jinja → inject HTML | `.jinja` / `.jinja2` / `.j2`; stale since 2024 |
| [`html-jinja`](https://github.com/JaagupAverin/html-jinja) | HTML → inject Jinja | same suffixes |
| [jinja-universal #4913](https://github.com/zed-industries/extensions/pull/4913) | ~353 langs, stalled | broader than this port |

Differentiate in README (already done). If installed next to `jinja2` / `html-jinja`, disable one of them. `.sls` does not conflict.

Zed publish rules still apply: MIT LICENSE, `id` without `zed`/`extension`, test via **Install Dev Extension**, no duplicate of dead `jinja2` without README differentiation.

## Architecture

```
Jinja file (.yaml.j2, .sls, .html.j2, …)
  └─ language "Jinja YAML" / "Jinja HTML" / …
       grammar = "jinja"          ← bennypowers/tree-sitter-jinja-dialects
       highlights/brackets/…      ← copied from queries/*.scm
       injections.scm:
         ((text) @injection.content
          (#set! injection.language "yaml" | "jinja-host-html" | …)
          (#set! injection.combined))
```

Zed resolves `injection.language` via **case-insensitive name or path suffix** (`language_for_name_or_extension` + UniCase). `"python"` matches `"Python"`. Hidden languages (`hidden = true`) are valid injection targets (same idea as `markdown-inline`).

Injection shape (one host per Jinja language — Zed injects one host per language):

```scheme
((text) @injection.content
 (#set! injection.language "<name>")
 (#set! injection.combined))
```

## Layout

```
extension.toml                 # generated — do not hand-edit grammars
LICENSE                        # MIT
README.md                      # user-facing
AGENTS.md                      # this file
scripts/generate_languages.py  # source of truth for langs, hosts, extension.toml
queries/                       # Jinja queries (edit these)
queries/hosts/                 # host highlight queries (copied into hidden langs)
languages/jinja-*/             # generated Jinja languages (edit via generator)
languages/jinja-host-*/        # generated hidden hosts (no path_suffixes)
```

`languages/*/highlights.scm` (Jinja side) and `languages/*/config.toml` are **generated**. Edit `queries/*.scm` or `scripts/generate_languages.py`, then:

```bash
python3 scripts/generate_languages.py
```

The generator fails if it finds an unexpected directory under `languages/`.

Do not commit `scripts/__pycache__/`.

## Generator (`scripts/generate_languages.py`)

Source of truth for:

- `LANGUAGES` — Jinja language dirs, suffixes, injection target, tab size, extra config
- `BUNDLED_HOSTS` — hidden language `key`, upstream `grammar`, repository, `rev`, optional `path`, highlights, and optional injections
- `EXTENSION_TOML_HEADER` / `JINJA_GRAMMAR` — identity + Jinja grammar pin
- copies `QUERY_FILES` into each `languages/jinja-*` dir
- writes `languages/jinja-host-*/config.toml` + `highlights.scm` (+ `injections.scm` when set)
- rewrites `extension.toml`

### f-string pitfall

Default block comment is `{#` … `#}`. When interpolating a **plain** string into an f-string, write `{#` not `{{#`. LaTeX uses `block_comment = '{ start = "((=", ... }'` (not an f-string of the braces). Quote brackets in TOML use `start = '"'`.

### Hidden host config

```toml
name = "jinja-host-xml"
grammar = "xml"
hidden = true
```

No `path_suffixes` — these languages must not steal `.xml` / `.php` from
official extensions. Standard grammar names may also be registered by those
extensions; keep the same upstream pins where possible and verify coexistence
during dev testing.

## Jinja grammar

```toml
[grammars.jinja]
repository = "https://github.com/bennypowers/tree-sitter-jinja-dialects"
rev = "4f832fe6feeae8c9e5963d835bec0272a8331b47"
```

Docs prefer `rev`; `commit` is an alias. Keep `rev`.

The grammar has an external scanner (`raw` / `verbatim` / comments). First **Install Dev Extension** compiles WASM and is slow (Jinja + 15 host grammars).

## Zed query files (Jinja)

| File | Role |
| --- | --- |
| `queries/highlights.scm` | Jinja tokens |
| `queries/brackets.scm` | delimiter pairs. Quotes are **not** listed: the grammar exposes a single `(string)` token, not anonymous `"` / `'` nodes |
| `queries/indents.scm` | `@end` on `endif` / `endfor` / …; only **block** `{% set %}…{% endset %}` |
| `queries/outline.scm` | `block` / `macro` |
| `queries/overrides.scm` | `(comment) @comment.inclusive` and `(string) @string` so `not_in` works |
| `queries/textobjects.scm` | Vim text objects |

### Zed-practice pitfalls already applied

- **No lone `{` autoclose** — fights `{{` / `{%` ([zed#23711](https://github.com/zed-industries/zed/issues/23711)).
- Quotes autoclose with `not_in = ["string", "comment"]`.
- `autoclose_before = "}])>"`, `collapsed_placeholder = "{# ... #}"` (LaTeX uses `((= ... =))`).
- Jinja HTML: `word_characters = ["-"]`.
- `overrides.scm` is required for `not_in` on comments/strings.

## Host highlighting split

### Inject Zed built-ins (always in `crates/languages`)

`css`, `json`, `markdown`, `python`, `javascript`, `typescript`, `yaml`, `bash`, `c`, `cpp`, `rust`.

Cython templates (`.pyx.j2` / `.pxd.j2` / `.pxi.j2`) inject **`python`**, not a Cython grammar.

HTML is **not** in `crates/languages` (it is a first-party Zed extension). We still **bundle** `jinja-host-html` so `.j2` highlighting does not depend on that extension. HTML host also copies `queries/hosts/html-injections.scm` so `<script>` / `<style>` inject JavaScript / CSS (those two **are** built-in).

### Bundled hidden hosts (`jinja-host-*`)

Pins match official Zed extensions as of 2026-08. Hidden language keys are
unique; grammar keys match upstream symbols. Highlight queries live in
`queries/hosts/`; licensing and source attribution are in
`THIRD_PARTY_NOTICES.md`.

| Key | Upstream | Notes |
| --- | --- | --- |
| `jinja-host-html` | `tree-sitter/tree-sitter-html` | + `html-injections.scm` |
| `jinja-host-xml` | `tree-sitter-grammars/tree-sitter-xml` | `path = "xml"` |
| `jinja-host-ruby` | `tree-sitter/tree-sitter-ruby` | |
| `jinja-host-toml` | `tree-sitter/tree-sitter-toml` | |
| `jinja-host-latex` | `497e0bdf29873/tree-sitter-latex` | same pin as zed-latex |
| `jinja-host-lua` | `tree-sitter-grammars/tree-sitter-lua` | |
| `jinja-host-ini` | `justinmk/tree-sitter-ini` | Apache-2.0 grammar; used by Properties **and** Systemd |
| `jinja-host-dockerfile` | `camdencheek/tree-sitter-dockerfile` | |
| `jinja-host-sql` | `DerekStride/tree-sitter-sql` | large; WASM compile can be slow/fragile |
| `jinja-host-hcl` | `tree-sitter-grammars/tree-sitter-hcl` | Terraform / tfvars / hcl |
| `jinja-host-nginx` | `gitlab.com/joncoole/tree-sitter-nginx` | GitLab clone must work at install |
| `jinja-host-groovy` | `murtaza64/tree-sitter-groovy` | pin from valentinegb/zed-groovy (matches `groovy.scm`) |
| `jinja-host-java` | `tree-sitter/tree-sitter-java` | |
| `jinja-host-php` | `tree-sitter/tree-sitter-php` | `path = "php"` |
| `jinja-host-cisco` | `dgethings/tree-sitter-cisco-ios-jinja2` | MIT. Parses IOS **and** Jinja; we only inject it into Jinja `text` (IOS fragments). Do **not** use Alcarin/Tree-Sitter-Cisco (no license). |

When adding a host: use a unique `jinja-host-*` hidden language `key`, set
`grammar` to the exact upstream parser symbol suffix, pin `rev`, add
`queries/hosts/<name>.scm`, point `LANGUAGES[].injection` at the hidden
language name, regenerate, and test alongside the corresponding official
extension. Grammar keys must be lowercase snake_case.

## Languages (29 Jinja + 15 hidden hosts)

Bare `.j2` / `.jinja` / `.jinja2` → **Jinja HTML**. Compound suffixes win (Zed longest match), so `.yaml.j2` is Jinja YAML.

| Dir | Language name | Injection | Intentional vs VS Code |
| --- | --- | --- | --- |
| `jinja` | Jinja | none | VS Code raw Jinja has no associations; we add `.njk` / `.nunjucks` / `.twig` |
| `jinja-html` | Jinja HTML | `jinja-host-html` | |
| `jinja-xml` | Jinja XML | `jinja-host-xml` | |
| `jinja-css` | Jinja CSS | `css` | |
| `jinja-json` | Jinja JSON | `json` | also `code-workspace.*` |
| `jinja-md` | Jinja Markdown | `markdown` | |
| `jinja-py` | Jinja Python | `python` | |
| `jinja-cy` | Jinja Cython | `python` | Cython-specific keywords are not a separate grammar |
| `jinja-rb` | Jinja Ruby | `jinja-host-ruby` | |
| `jinja-js` | Jinja JavaScript | `javascript` | |
| `jinja-ts` | Jinja TypeScript | `typescript` | |
| `jinja-yaml` | Jinja YAML | `yaml` | **`.sls` is the Salt reason this extension exists** |
| `jinja-toml` | Jinja TOML | `jinja-host-toml` | |
| `jinja-latex` | Jinja LaTeX | `jinja-host-latex` | see LaTeX delimiters below |
| `jinja-lua` | Jinja Lua | `jinja-host-lua` | |
| `jinja-properties` | Jinja Properties | `jinja-host-ini` | `.conf.j2` is **not** here |
| `jinja-shell` | Jinja Shell | `bash` | |
| `jinja-dockerfile` | Jinja Dockerfile | `jinja-host-dockerfile` | |
| `jinja-sql` | Jinja SQL | `jinja-host-sql` | |
| `jinja-terraform` | Jinja Terraform | `jinja-host-hcl` | |
| `jinja-nginx` | Jinja Nginx | `jinja-host-nginx` | owns `.conf.j2` (VS Code listed it on Properties too) |
| `jinja-groovy` | Jinja Groovy | `jinja-host-groovy` | |
| `jinja-systemd` | Jinja Systemd | `jinja-host-ini` | unit suffixes from `SYSTEMD_UNITS` |
| `jinja-c` | Jinja C | `c` | VS Code folds `.c.j2` into C++; Zed cannot inject two hosts in one language |
| `jinja-cpp` | Jinja C++ | `cpp` | `.h.j2` is C++ here |
| `jinja-cisco` | Jinja Cisco Config | `jinja-host-cisco` | |
| `jinja-java` | Jinja Java | `jinja-host-java` | |
| `jinja-php` | Jinja PHP | `jinja-host-php` | |
| `jinja-rust` | Jinja Rust | `rust` | |

Raw Jinja (`.njk` / `.twig`) has **no host** — delimiter highlighting only.

## LaTeX delimiters

Better Jinja / nbconvert uses `((*` `*))`, `(((` `)))`, `((=` `=))` because `{%` clashes with LaTeX.

- Autoclose pairs and LaTeX `block_comment` **are** set up for those.
- `tree-sitter-jinja-dialects` still only parses `{{` / `{%` / `{#`.
- Host LaTeX highlighting still runs on `text` nodes.

Do not claim nbconvert tags are parsed as Jinja until the grammar (or a fork) supports them.

## How to test

1. Zed command palette → `zed: install dev extension` → this repo root.
2. First compile is slow (16 WASM grammars). GitLab must be reachable for nginx.
3. Open `.sls`, `.yaml.j2`, `.html.j2`, `.xml.j2`, `.j2`.
4. `editor: open syntax tree`, `zed: open log`.
5. Confirm Jinja delimiters **and** host tokens highlight without other language extensions.

## Known limitations / residual risk

- Pinned third-party grammar WASM (Jinja + hosts) is the main supply-chain surface. No runtime extension code, no network I/O at editor runtime.
- SQL grammar is large; nginx comes from GitLab.
- Cisco host grammar also understands Jinja; we only feed it `text` between our Jinja tags.
- Cython ≈ Python highlighting.
- PHP grammar typically wants `<?php`; templates without a tag may highlight poorly.
- Security review of the earlier skeleton: no medium+ issues. Re-review if grammar pins or generator behavior change.

## Git status (as of 2026-08-17)

`main` contains both implementation PRs through merge commit `ed06d6b`.
The old feature branch was deleted locally and remotely. Current follow-up
fixes (grammar key correction, notices, docs) are uncommitted; do not commit
unless asked.

## Do not

- PR to `ArcherHume/jinja2-support`
- Hand-edit `extension.toml` grammars or `languages/**` copies (except debugging; then put the change in `queries/` / the generator)
- Rename grammar keys away from their upstream Tree-sitter C symbols
- Give hidden hosts `path_suffixes`
- Auto-close a lone `{`
- Promise marketplace install until the user asks to publish (Zed extensions registry PR)
- Add features unrelated to highlighting/association without being asked
- Dump secrets; there are none in this repo
