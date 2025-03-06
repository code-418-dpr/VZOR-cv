# VZOR-cv

[![license](https://img.shields.io/github/license/code-418-dpr/VZOR-cv)](https://opensource.org/licenses/MIT)
[![release](https://img.shields.io/github/v/release/code-418-dpr/VZOR-cv?include_prereleases)](https://github.com/code-418-dpr/VZOR-cv/releases)
[![downloads](https://img.shields.io/github/downloads/code-418-dpr/VZOR-cv/total)](https://github.com/code-418-dpr/VZOR-cv/releases)
[![code size](https://img.shields.io/github/languages/code-size/code-418-dpr/VZOR-cv.svg)](https://github.com/code-418-dpr/VZOR-cv)

[![Linter](https://github.com/code-418-dpr/VZOR-cv/actions/workflows/linter.yaml/badge.svg)](https://github.com/code-418-dpr/VZOR-cv/actions/workflows/linter.yaml)
[![CodeQL (Python, GH Actions)](https://github.com/code-418-dpr/VZOR-cv/actions/workflows/codeql.yaml/badge.svg)](https://github.com/code-418-dpr/VZOR-cv/actions/workflows/codeql.yaml)

Сервис распознавания образов для проекта [VZOR](https://github.com/code-418-dpr/VZOR)

## Особенности реализации

- [x] отсутствие функционала

## Стек

- **Python** — язык программирования
- **uv** — самый быстрый пакетный менеджер для Python
- **Ruff** — быстрый линтер с большим количеством правил
- **Docker** — платформа для контейнеризации

## Установка и запуск

0. Клонируйте репозиторий и перейдите в его папку.

### Посредством Docker

1. Установите Docker.
2. Создайте файл `.env` на основе [.env.template](.env.template) и настройте все описанные там параметры.
3. Запустите сборку образа:

```shell
docker build -t vzor-cv .
```

4. Теперь запускать образ можно командой:

```shell
docker run -d --name vzor-cv-standalone vzor-cv
```

### Без использования Docker

1. Установите пакетный менеджер uv одним из способов. Например, для Windows:

```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Установите зависимости:

```shell
uv sync --frozen --no-dev
```

3. Создайте файл `.env` на основе [.env.template](.env.template) и настройте все описанные там параметры.

4. Теперь запускать проект можно командой:

```shell
uv run -m src
```

## Модификация

Если вы планируете модифицировать проект, установите все зависимости:

```shell
uv sync
```

Запустить линтинг кода (и автоисправление некоторых ошибок) можно через Ruff:

```shell
uv run ruff check --fix .
```
