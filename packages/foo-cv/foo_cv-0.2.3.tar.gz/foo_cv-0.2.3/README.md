# FOO CV

[![codecov](https://codecov.io/gh/drorata/foo-cv/branch/main/graph/badge.svg?token=N44MD6UJ3Z)](https://codecov.io/gh/drorata/foo-cv)
![PyPI](https://img.shields.io/pypi/v/foo-cv)
![GitHub](https://img.shields.io/github/license/drorata/foo-cv)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/foo-cv)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/drorata/foo-cv/test_code.yml)

> Separate content and design for CV

We provide two files:
- Content given as JSON and
- a Jinja2 LaTeX template.

The provided Python script merely connects the two and generates a TeX file that can then be processed using PDFLaTeX.

[`json_resume`](https://github.com/prat0318/json_resume) is the main source of inspiration for this.

## Try this out

You can easily try this out once you have [`task`](https://taskfile.dev/) and [`podman`](https://podman.io/) installed.
You will need to:
1. Get the environment ready; run `poetry install` for that.
1. Build a helper docker image: `task build-LaTeX-image` will take care of that. Next,
2. Run the full flow: `task build-cv` which will generate a PDF.

## The profile picture

The [picture](./profile-pic.jpg) was created using [Dalle](https://labs.openai.com/) given the description:

> Create a portrait of Elrond mixed with Worf
