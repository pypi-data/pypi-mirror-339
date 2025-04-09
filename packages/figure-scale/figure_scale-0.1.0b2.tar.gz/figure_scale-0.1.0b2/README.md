# Scale your matplotlib figures

<p align="center">
<a href="https://github.com/fschuch/figure-scale"><img src="docs/logo.png" alt="Figure scale logo" width="320"></a>
</p>
<p align="center">
    <em>Publication quality figures start here</em>
</p>

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| QA      | [![CI](https://github.com/fschuch/figure-scale/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/fschuch/figure-scale/actions/workflows/ci.yaml) [![CodeQL](https://github.com/fschuch/figure-scale/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/fschuch/figure-scale/actions/workflows/github-code-scanning/codeql) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/fschuch/figure-scale/main.svg)](https://results.pre-commit.ci/latest/github/fschuch/figure-scale/main)[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fschuch_figure-scale&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fschuch_figure-scale)[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fschuch_figure-scale&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fschuch_figure-scale) |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/figure-scale.svg?logo=pypi&label=PyPI)](https://pypi.org/project/figure-scale/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/figure-scale.svg?logo=python&label=Python)](https://pypi.org/project/figure-scale/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Meta    | [![Wizard Template](https://img.shields.io/badge/Wizard-Template-%23447CAA)](https://github.com/fschuch/wizard-template) [![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/) [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![PyPI - License](https://img.shields.io/pypi/l/figure-scale?color=blue)](https://github.com/fschuch/figure-scale/blob/master/LICENSE) [![EffVer Versioning](https://img.shields.io/badge/version_scheme-EffVer-0097a7)](https://jacobtomlinson.dev/effver)                                                                                                                                                          |

## Usage

```python
import matplotlib.pyplot as plt
import figure_scale as fs
figsize = fs.FigureScale(4.0, 2.0, units="in")
```

```python
plt.rcParams.update({'figure.figsize' : figsize})
```

```python
fig, ax = plt.subplots(figsize=figsize)
```

```python
with figsize():
    fig, ax = plt.subplots()
```

```python
@figsize()
def my_plot():
    ...
```

## Installation

```bash
pip install figure-scale
```

## Copyright and License

© 2023 [Felipe N. Schuch](https://github.com/fschuch).
All content is under [MIT License](https://github.com/fschuch/figure-scale/blob/main/LICENSE).
