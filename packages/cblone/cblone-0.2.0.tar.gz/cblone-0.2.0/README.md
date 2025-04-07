# cblone

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

A CLI to back up all your [Codeberg](https://codeberg.org/) repositories.

- [Source code](https://codeberg.org/joaopalmeiro/cblone)
- [PyPI package](https://pypi.org/project/cblone/)
- [Snyk Advisor](https://snyk.io/advisor/python/cblone)

## Usage

### Via [pipx](https://github.com/pypa/pipx)

```bash
pipx run cblone --help
```

```bash
pipx run cblone
```

## Development

Install [pyenv](https://github.com/pyenv/pyenv) (if necessary).

```bash
pyenv install && pyenv versions
```

```bash
pip install hatch==1.14.0 && hatch --version
```

```bash
hatch config set dirs.env.virtual .hatch
```

```bash
hatch config show
```

```bash
hatch env create
```

```bash
hatch status
```

```bash
hatch env show
```

```bash
hatch dep show table
```

```bash
hatch run cblone --help
```

```bash
hatch run cblone
```

```bash
hatch run lint
```

```bash
hatch run format
```

## Deployment

```bash
hatch version micro
```

```bash
hatch version minor
```

```bash
hatch version major
```

```bash
hatch build --clean
```

```bash
echo "v$(hatch version)" | pbcopy
```

- Commit and push changes.
- Create a tag on [GitHub Desktop](https://github.blog/2020-05-12-create-and-push-tags-in-the-latest-github-desktop-2-5-release/).
- Check [Codeberg](https://codeberg.org/joaopalmeiro/cblone/tags).

```bash
hatch publish
```

- Check [PyPI](https://pypi.org/project/cblone/).
