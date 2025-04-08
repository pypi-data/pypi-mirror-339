import json
from pathlib import Path

import jinja2
import typer

from foo_cv import utils

app = typer.Typer()
app = typer.Typer(rich_markup_mode="rich")


def get_latex_jinja_env(template_base_path: Path) -> jinja2.Environment:
    return jinja2.Environment(
        block_start_string="\\BLOCK{",
        block_end_string="}",
        variable_start_string="\\VAR{",
        variable_end_string="}",
        comment_start_string="\\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(template_base_path),
    )


@app.command(help="Generate a LaTeX file from a Jinja2 template and a JSON file")
def generate_text(
    template: Path = typer.Argument(
        ..., help="Path to the the Jinja2 template that will be used"
    ),
    content: Path = typer.Argument(
        ..., help="Path to the JSON with the content of the CV"
    ),
    output: Path = typer.Argument(
        None, help="Where to save and how to name the resulting TeX file"
    ),
):
    with open(content, "r") as f:
        content = json.load(f)

    latex_jinja_env = get_latex_jinja_env(template.parents[0])

    template = latex_jinja_env.get_template(template.name)

    content = utils.latex_render_content(content)
    rendered_content = template.render(**content)

    if output is None:
        print(rendered_content)
        exit(0)

    with open(output, "w") as f:
        f.write(rendered_content)


def main():  # pragma: no cover
    app()
