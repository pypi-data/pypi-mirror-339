# smollama-py

[![PyPI](https://img.shields.io/pypi/v/smollama-py.svg)](https://pypi.org/project/smollama-py/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/smollama-py?include_prereleases&label=changelog)](https://github.com/sukhbinder/smollama-py/releases)
[![Tests](https://github.com/sukhbinder/smollama-py/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/smollama-py/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/smollama-py/blob/master/LICENSE)

A python app to serve smOllama. Not everyone has npx so created this wrapper over excellent [smOllama](https://github.com/GUNNM-VR/smOllama) web page.

smOllama is lightweight web browser chatbot interface for Ollama models. smollama-py is a python app to ease serving `smOllama`

## Getting Started

### Prerequisites

- A running Ollama instance with at least one model installed
- A modern web browser

## Installation

Install this tool using `pip`:
```bash
pip install smollama-py
```
## Usage

For help, run:
```bash
smollama-py --help
```
You can also use:
```bash
python -m smollama-py --help
```
```
usage: smollama-py [-h] [-m {chrome,electron,edge,msie}]

A python app to serve smOllama

optional arguments:
  -h, --help            show this help message and exit
  -m {chrome,electron,edge,msie}, --mode {chrome,electron,edge,msie}

```

### Usage

1. Select your preferred Ollama model from the dropdown
2. Type your message in the input field
3. Press Enter or click the Send button
4. View the response with rendered Markdown and LaTeX

### Demo
![smollama-py](https://raw.githubusercontent.com/sukhbinder/smollama-py/main/smollama-py-demo.gif)

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd smollama-py
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
