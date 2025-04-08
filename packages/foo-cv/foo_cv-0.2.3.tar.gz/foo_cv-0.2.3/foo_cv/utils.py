from typing import Any, Dict

from loguru import logger
from mistletoe import Document, span_token
from mistletoe.latex_renderer import LaTeXRenderer

SUPPORTED_TOKENS = (
    span_token.Emphasis,
    span_token.Link,
    span_token.RawText,
    span_token.Strikethrough,
    span_token.Strong,
    span_token.Strong,
    # TODO: Add support of inline code in LaTeX
    # mistletoe.span_token.InlineCode,
)


def render_latex(text: str, minimal: bool = True) -> str:
    """Minimal parse of Markdown string to LaTeX

    Expected single paragraph without any images, lists, tables etc.

    Parameters
    ----------
    text : str
        Provided Markdown string

    minimal : bool, optional
        Determines whether to return a complete LaTeX document or merely the "body",
        by default True


    Returns
    -------
    str
        LaTeX rendered string. Please note that some packages would be needed
        (e.g. `hyperref` when links are used). If `minimal` is True, make sure
        you manually include the needed LaTeX dependencies.

    Raises
    ------
    ValueError
        When the provided string is "too" complex.
    """
    logger.debug(f"Rendering LaTeX - {text}")
    with LaTeXRenderer() as rendered:
        ast = Document(text)
        if len(ast.children) != 1:
            raise ValueError("Number of children of provided text is not 1")
        for child in ast.children[0].children:
            if not isinstance(child, SUPPORTED_TOKENS):
                raise ValueError(f"Child type {type(child)} is not supported")
        res: str = rendered.render(ast)
    if not minimal:
        return res
    BEGIN_DOC = "\\begin{document}"
    END_DOC = "\\end{document}"
    return res[res.find(BEGIN_DOC) + len(BEGIN_DOC) : res.find(END_DOC)].strip("\n")


def latex_render_content(content: Dict[str, Any]) -> Dict[str, Any]:
    """Render LaTeX snippet in text values in the content dictionary

    Parameters
    ----------
    content : Dict[str, Any]
        Content dictionary to be prepared. All values should be either
        `dict`, `list` (in these cases) triggering a recursive scan or `str`/`int`.

    Returns
    -------
    Dict[str, Any]
        Dictionary with the same key. All values that are strings should be replaced
        with LaTeX snippets.

    Raises
    ------
    ValueError
        Raised when content contains unsupported value types.
    """
    transformed_content = dict()
    for key in content.keys():
        if not isinstance(content[key], (dict, str, list, int)):
            raise ValueError(
                f"Non supported type ({type(content[key])}) of a value {content[key]}"
            )
        if isinstance(content[key], dict):
            transformed_content[key] = latex_render_content(content[key])
        if isinstance(content[key], str):
            transformed_content[key] = render_latex(content[key], minimal=True)
        if isinstance(content[key], list):
            latex_list = list()
            for item in content[key]:
                if isinstance(item, dict):
                    latex_list.append(latex_render_content(item))
                if isinstance(item, (str, int)):
                    latex_list.append(render_latex(str(item), minimal=True))
            transformed_content[key] = latex_list

    return transformed_content
