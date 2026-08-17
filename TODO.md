# TODO: Zed-расширение Jinja (порт jinjahtml-vscode)

Порт [samuelcolvin/jinjahtml-vscode](https://github.com/samuelcolvin/jinjahtml-vscode) на Zed.
Zed не поддерживает TextMate — расширение на tree-sitter: грамматика
[bennypowers/tree-sitter-jinja-dialects](https://github.com/bennypowers/tree-sitter-jinja-dialects)
(MIT, Jinja2/Django/Twig/Nunjucks/Tera; узлы `text` заточены под injections).

**Принцип:** один парсер (`jinja`) на файл; host-язык — через `injections.scm` в `text`.
Built-in хосты Zed (YAML, Python, CSS, …) инжектятся по имени.
Остальные вшиты как скрытые языки `jinja-host-*` — **чужие marketplace-расширения
не нужны**. Рабочая память агента: `AGENTS.md`.

Источник правды для языков / host-пинов / `extension.toml`:
`python3 scripts/generate_languages.py` (не править копии в `languages/` руками).

---

## Стратегия

В реестре уже есть:

| id | репо | подход | покрытие |
|---|---|---|---|
| `jinja2` | [ArcherHume/jinja2-support](https://github.com/ArcherHume/jinja2-support) | Jinja-first → inject HTML | только `.jinja`/`.jinja2`/`.j2` + HTML |
| `html-jinja` | [JaagupAverin/html-jinja](https://github.com/JaagupAverin/html-jinja) | HTML-first → inject Jinja | только HTML + те же суффиксы |

[CONTRIBUTING](https://github.com/zed-industries/extensions/blob/main/CONTRIBUTING.md):
сначала чинить/расширять существующее, а не дублировать.

- [x] **Выбрать путь (до кода):**
  - ~~A: PR / форк `jinja2-support`~~ — апстрим мёртв (последний пуш 2024-10,
    LICENSE PR и issues без ответа). **Не слать PR в ArcherHume.**
  - **B (выбрано):** своё расширение, id `jinja2-sls`, name
    `Jinja2 SLS Template Support`. Scope = порт jinjahtml-vscode включая `.sls`.
- [x] Зафиксировать решение в README (почему не `jinja2` / `html-jinja`).

Ниже этапы — **путь B**.

**Справка:**
- Языки: https://zed.dev/docs/extensions/languages
- Dev + publish: https://zed.dev/docs/extensions/developing-extensions
- Примеры для тестов: скачать/клонировать `samuelcolvin/jinjahtml-vscode` → `examples/`
  (в этот репозиторий examples **не** коммитить, если не нужны; локально достаточно)
- Отладка: `editor: open syntax tree`, `zed: open log`, при необходимости `zed --foreground`

---

## Этап 0 — Репозиторий и именование

- [x] GitHub-репо переименован в `jinja2-sls`; manifest и `origin` обновлены.
- [x] **id** (в `extension.toml`): `jinja2-sls`
      (не `jinja` / `jinja2` / `html-jinja` — заняты).
- [x] `name`: `Jinja2 SLS Template Support`
- [x] В README описано: рядом с `jinja2`/`html-jinja` суффиксы `.jinja`/`.j2`
      конфликтуют — отключать одно из расширений. `.sls` не конфликтует.

---

## Этап 1 — Скелет (grammar-only, без Rust)

Custom Rust **не нужен** (нет LSP / debugger / MCP). Как у `html-jinja` и `jinja2`:
только манифест + `languages/` + grammars.

- [x] `extension.toml` (генерируется скриптом): id/name/version/schema/authors/
      description/repository; `[grammars.jinja]` с **`rev`** (не `commit`)
      `4f832fe6feeae8c9e5963d835bec0272a8331b47` плюс 15 host-грамматик.
      Grammar keys совпадают с export symbols (`html`, `xml`, `cisco_ios_jinja2`, …).
- [x] `LICENSE` в корне (MIT)
- [x] `.gitignore` (`.DS_Store`, Python cache; `AGENTS.md`/`TODO.md` не теряются
      из-за global ignore)
- [x] `THIRD_PARTY_NOTICES.md` + `LICENSE-APACHE` для скопированных host queries
- [x] **Не** добавлять `Cargo.toml` / `src/lib.rs`
- [ ] Dev-install: Extensions → **Install Dev Extension** (или `zed: install dev extension`)
      на каталог репо — WASM-сборка грамматики + external scanner
      (`raw` / `verbatim` / comments) **и** bundled host grammars без ошибок в log.
      Ещё не подтверждалось на этой машине; первая сборка будет долгой (~16 WASM).

---

## Этап 2 — Якорь: Jinja HTML (`languages/jinja-html/`)

Сделано через генератор (не руками). От исходного черновика отличается намеренно
(zed-practice): нет autoclose одиночной `{` (zed#23711); quotes + `not_in`;
`overrides.scm`; `word_characters = ["-"]`; host = **`jinja-host-html`**, не `html`.

- [x] `config.toml` — `Jinja HTML`, `grammar = "jinja"`, суффиксы включая голый `.j2`
- [x] `highlights.scm` — `queries/highlights.scm` (preferred captures справа:
      `@function @function.builtin`)
- [x] `injections.scm` — combined injection в `jinja-host-html`; у хоста ещё
      `html-injections.scm` (`<script>` → javascript, `<style>` → css)
- [x] `brackets.scm`, `indents.scm` (`@end` на endif/endfor/…; только block `{% set %}`),
      `outline.scm`, плюс `overrides.scm` и `textobjects.scm`
- [ ] Smoke: dev-extension + examples оригинала; syntax tree без лавины ERROR

---

## Этап 3 — Остальные языки

Генератор копирует shared queries в каждый `languages/jinja-*` и пишет
`config.toml` / `injections.scm`. Hidden hosts — `languages/jinja-host-*`.

### 3.1 Built-in host (есть в Zed без доп. extensions)

| каталог | `name` | injection | path_suffixes (минимум) |
|---|---|---|---|
| `jinja` (raw) | Jinja | — | `njk`, `nunjucks`, `twig` |
| `jinja-css` | Jinja CSS | `css` | `css.j2`, … |
| `jinja-json` | Jinja JSON | `json` | `json.j2`, … + `code-workspace.*` |
| `jinja-md` | Jinja Markdown | `markdown` | `md.j2`, … |
| `jinja-yaml` | Jinja YAML | `yaml` | `yml.j2`, `yaml.j2`, …, **`sls`** |
| `jinja-shell` | Jinja Shell | `bash` | `sh.j2`, `bash.j2`, `zsh.j2`, `env.j2`, … |
| `jinja-py` | Jinja Python | `python` | `py.j2`, `pyi.j2`, … |
| `jinja-js` | Jinja JavaScript | `javascript` | `js.j2`, … |
| `jinja-ts` | Jinja TypeScript | `typescript` | `ts.j2`, … |
| `jinja-c` | Jinja C | `c` | `c.j2`, … |
| `jinja-cpp` | Jinja C++ | `cpp` | `cpp.j2`, `h.j2`, `hpp.j2`, … |
| `jinja-rust` | Jinja Rust | `rust` | `rs.j2`, … |

- [x] Все языки 3.1 сгенерированы (29 Jinja-языков всего, включая 3.2/3.3)
- [x] Shell injection зафиксирован как `bash` (language name `"Shell Script"`
      резолвится через UniCase / name_or_extension; `bash` — имя грамматики built-in)
- [x] C и C++ — **разные** языки (одна инъекция на язык). `.c.j2` → Jinja C
      (в VS Code это было C++)

### 3.2 Host, которого нет в `crates/languages`

**Сделано иначе, чем в исходном плане:** не «опционально + таблица нужных
extensions», а **вшитые hidden languages**. Пользователь потребовал подсветку
хоста для всех языков без чужих расширений.

Имена скрытых языков уникальные (`jinja-host-xml`), `hidden = true`, без
`path_suffixes`. Grammar key намеренно стандартный (`xml`): Zed экспортирует
`tree_sitter_<grammar>`, поэтому переименование ключа ломает WASM link.

| каталог | injection | host grammar |
|---|---|---|
| `jinja-html` | `jinja-host-html` | tree-sitter-html (HTML не built-in) |
| `jinja-xml` | `jinja-host-xml` | tree-sitter-xml `path = "xml"` |
| `jinja-toml` | `jinja-host-toml` | tree-sitter-toml |
| `jinja-sql` | `jinja-host-sql` | tree-sitter-sql (тяжёлый WASM) |
| `jinja-dockerfile` | `jinja-host-dockerfile` | tree-sitter-dockerfile |
| `jinja-php` | `jinja-host-php` | tree-sitter-php `path = "php"` |
| `jinja-java` | `jinja-host-java` | tree-sitter-java |
| `jinja-lua` | `jinja-host-lua` | tree-sitter-lua |
| `jinja-rb` | `jinja-host-ruby` | tree-sitter-ruby |

- [x] Все хосты 3.2 вшиты в v0.1.0 (не откладывались)
- [x] README больше **не** говорит «нужен host extension»

### 3.3 Было «отложено (v2)» — сделано в этом же наборе

| каталог | injection | примечание |
|---|---|---|
| `jinja-latex` | `jinja-host-latex` | autoclose nbconvert `((*`/`(((`/`((=`; грамматика Jinja всё ещё только `{{`/`{%`/`{#` |
| `jinja-properties` | `jinja-host-ini` | `.conf.j2` **не** здесь — у Nginx |
| `jinja-nginx` | `jinja-host-nginx` | GitLab `joncoole/tree-sitter-nginx` |
| `jinja-terraform` | `jinja-host-hcl` | |
| `jinja-systemd` | `jinja-host-ini` | unit-суффиксы из `SYSTEMD_UNITS` |
| `jinja-cisco` | `jinja-host-cisco` | MIT `dgethings/tree-sitter-cisco-ios-jinja2` (не Alcarin — нет лицензии) |
| `jinja-cy` | `python` | Cython ≈ Python highlighting |
| `jinja-groovy` | `jinja-host-groovy` | |

- [x] Языки 3.3 добавлены, host-подсветка вшита (Cython через built-in Python)

---

## Этап 4 — Тесты и полировка

- [ ] Локально подтянуть `examples/` из samuelcolvin/jinjahtml-vscode
- [ ] Пройти examples: syntax tree, подсветка Jinja + host (включая `.sls`, `.xml.j2`, `.j2`)
- [x] Конфликты суффиксов задокументированы в README
      (голый `.j2` → Jinja HTML; `.sls` → Jinja YAML; `.conf.j2` → Nginx)
- [x] Inline-JS/CSS в HTML: upstream MIT `html-injections.scm` (`script`/`style`)
- [x] `textobjects.scm` для Vim-mode (`queries/textobjects.scm` → копии в языках)
- [x] `overrides.scm` (`comment.inclusive`, `string`) чтобы `not_in` работал
- [x] Статические проверки: generator idempotent, весь TOML парсится, все 16
      grammar keys snake_case и подтверждены по upstream `tree_sitter_*` exports
- [ ] Подтвердить injection names / host WASM после реального Install Dev Extension
- [x] Основная работа закоммичена, оба PR merged в `main`, старые ветки удалены.
- [ ] Текущие follow-up fixes закоммитить и push — **только по просьбе**.

---

## Этап 5 — Релиз и publish

- [x] `README.md`: scope vs `jinja2`/`html-jinja`, таблица ассоциаций, LICENSE
- [ ] Скриншот в README
- [x] `version` в `extension.toml` = `0.1.0` (тега ещё нет)
- [ ] Git-тег `v0.1.0`, push публичного репо
- [ ] **Локально** Install Dev Extension + реальные файлы — без этого PR закроют
- [ ] PR в [zed-industries/extensions](https://github.com/zed-industries/extensions)
      (**не** «положить один extension.toml»):
  1. Fork репо на **личный** GitHub-аккаунт (не org — так просят maintainers)
  2. `git submodule add https://github.com/<user>/<repo>.git extensions/<id>`
  3. В корневом `extensions.toml`:
     ```toml
     [<id>]
     submodule = "extensions/<id>"
     version = "0.1.0"
     ```
  4. `pnpm sort-extensions`
  5. В описании PR: отличие от `jinja2` / `html-jinja`, что протестировано dev-extension,
     что host-языки hidden и bundled; grammar keys совпадают с upstream symbols

---

## Риски / решения

| Риск | Решение | Статус |
|---|---|---|
| Дубликат marketplace (`jinja2`, `html-jinja`) | id `jinja2-sls` + multi-host + README | сделано |
| PR process | submodule + `extensions.toml` + `pnpm sort-extensions` | не начато |
| `block_comment` массивом | Только table-форма `{ start, prefix, end, tab_size }` | сделано |
| Fallback captures | Preferred **справа**: `@function @function.builtin` | сделано |
| Host «не встроен» | Вшить `jinja-host-*`, не обещать чужие extensions | сделано |
| injection name | Built-in = `yaml`/`python`/…; bundled = `jinja-host-xml` | в коде; ждать dev-тест |
| External scanner WASM | Проверка на этапе 1 dev-install | не подтверждено |
| Конфликт `.j2` | README: disable одно из Jinja-extensions | сделано |
| `commit` vs `rev` в grammar | Используем `rev` | сделано |
| Коллизия grammar names с host extensions | Имена hidden languages уникальны; grammar keys обязаны совпадать с C symbols, pins выровнены с официальными extensions | нужен coexistence dev-тест |
| SQL WASM / GitLab nginx | Возможны медленная/хрупкая сборка | риск остаётся |
| nbconvert LaTeX-делимитеры | Autoclose есть; парсер Jinja их не разбирает | задокументировано |
| Лицензии скопированных queries | `THIRD_PARTY_NOTICES.md` + MIT/Apache-2.0 тексты; HTML заменён upstream MIT queries | сделано |

---

## Чеклист минимального v0.1.0

- [x] Стратегия A или B выбрана (**B**)
- [x] id + LICENSE + полный `extension.toml` (включая bundled hosts)
- [x] Языки: raw Jinja + HTML + YAML/`.sls` + Markdown + Python **и** полный паритет
      Better Jinja 0.20.0 (C отдельно, 3.2/3.3 не откладывались)
- [x] Host-подсветка без чужих extensions (требование пользователя)
- [x] README с дифференциацией и таблицей ассоциаций
- [x] `AGENTS.md` с контекстом для агентов
- [ ] Грамматика собирается через Install Dev Extension
- [ ] Скриншот
- [ ] PR по официальному процессу (submodule)
