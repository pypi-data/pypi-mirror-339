# llm-hacker-news

[![PyPI](https://img.shields.io/pypi/v/llm-hacker-news.svg)](https://pypi.org/project/llm-hacker-news/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-hacker-news?include_prereleases&label=changelog)](https://github.com/simonw/llm-hacker-news/releases)
[![Tests](https://github.com/simonw/llm-hacker-news/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-hacker-news/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-hacker-news/blob/main/LICENSE)

LLM plugin for pulling content from Hacker News

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-hacker-news
```
## Usage

You can feed a full conversation thread from [Hacker News](https://news.ycombinator.com/) into LLM using the `hn:` [fragment](https://llm.datasette.io/en/stable/fragments.html) with the ID of the conversation. For example:

```bash
llm -f hn:43615912 'summary with illustrative direct quotes'
```
Item IDs can be found in the URL of the conversation thread.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-hacker-news
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
