from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import nbformat

import nbstore.pgf

from .content import get_mime_content

if TYPE_CHECKING:
    from nbformat import NotebookNode


class Store:
    notebook_dir: Path
    notebooks: dict[Path, NotebookNode]
    st_mtime: dict[Path, float]
    executed: set[Path]
    current_path: Path | None

    def __init__(self, notebook_dir: Path | str) -> None:
        self.notebook_dir = Path(notebook_dir)
        self.notebooks = {}
        self.st_mtime = {}
        self.executed = set()
        self.current_path = None

    def _read(self, abs_path: Path) -> NotebookNode:
        mtime = abs_path.stat().st_mtime

        if abs_path in self.notebooks and self.st_mtime[abs_path] == mtime:
            return self.notebooks[abs_path]

        nb: NotebookNode = nbformat.read(abs_path, as_version=4)  # type: ignore

        self.notebooks[abs_path] = nb
        self.st_mtime[abs_path] = mtime

        return nb

    def _write(self, abs_path: Path) -> None:
        if nb := self.notebooks.get(abs_path):
            nbformat.write(nb, abs_path)

    def get_abs_path(self, url: str) -> Path:
        if not url:
            if self.current_path:
                return self.current_path

            msg = "No active notebook."
            raise ValueError(msg)

        abs_path = (self.notebook_dir / url).absolute()

        if abs_path.exists():
            self.current_path = abs_path
            return abs_path

        msg = f"Notebook not found: {abs_path}."
        raise ValueError(msg)

    def get_notebook(self, url: str) -> NotebookNode:
        abs_path = self.get_abs_path(url)
        return self._read(abs_path)

    def get_cell(self, url: str, identifier: str) -> dict[str, Any]:
        nb = self.get_notebook(url)
        return get_cell(nb, identifier)

    def get_source(
        self,
        url: str,
        identifier: str,
        *,
        include_identifier: bool = False,
    ) -> str:
        nb = self.get_notebook(url)
        return get_source(nb, identifier, include_identifier=include_identifier)

    def get_outputs(self, url: str, identifier: str) -> list:
        nb = self.get_notebook(url)
        return get_outputs(nb, identifier)

    def get_stream(self, url: str, identifier: str) -> str | None:
        outputs = self.get_outputs(url, identifier)
        return get_stream(outputs)

    def get_data(self, url: str, identifier: str) -> dict[str, str]:
        outputs = self.get_outputs(url, identifier)
        data = get_data(outputs)
        return convert(data)

    def add_data(self, url: str, identifier: str, mime: str, data: str) -> None:
        outputs = self.get_outputs(url, identifier)
        if output := get_data_by_type(outputs, "display_data"):
            output[mime] = data

    def save_notebook(self, url: str) -> None:
        self._write(self.get_abs_path(url))

    def delete_data(self, url: str, identifier: str, mime: str) -> None:
        outputs = self.get_outputs(url, identifier)
        output = get_data_by_type(outputs, "display_data")
        if output and mime in output:
            del output[mime]

    def get_language(self, url: str) -> str:
        nb = self.get_notebook(url)
        return get_language(nb)

    def is_dirty(self, url: str) -> bool:
        abs_path = self.get_abs_path(url)

        if abs_path not in self.executed:
            return True

        mtime = abs_path.stat().st_mtime
        return abs_path not in self.st_mtime or self.st_mtime[abs_path] != mtime

    def execute(
        self,
        url: str,
        *,
        force: bool = False,
        timeout: int = 600,
    ) -> NotebookNode:
        nb = self.get_notebook(url)

        if not self.is_dirty(url) and not force:
            return nb

        try:
            from nbconvert.preprocessors import ExecutePreprocessor
        except ModuleNotFoundError:  # no cov
            msg = "nbconvert is not installed"
            raise ModuleNotFoundError(msg) from None

        ep = ExecutePreprocessor(timeout=timeout)
        ep.preprocess(nb)

        abs_path = self.get_abs_path(url)
        self.executed.add(abs_path)

        return nb

    def get_mime_content(
        self,
        url: str,
        identifier: str,
    ) -> tuple[str, str | bytes] | None:
        data = self.get_data(url, identifier)
        return get_mime_content(data)


def get_cell(nb: NotebookNode, identifier: str) -> dict[str, Any]:
    for cell in nb["cells"]:
        source: str = cell["source"]
        if source.startswith(f"# #{identifier}\n"):
            return cell

    msg = f"Unknown identifier: {identifier}"
    raise ValueError(msg)


def get_source(
    nb: NotebookNode,
    identifier: str,
    *,
    include_identifier: bool = False,
) -> str:
    if source := get_cell(nb, identifier).get("source", ""):
        if include_identifier:
            return source

        return source.split("\n", 1)[1]

    raise NotImplementedError


def get_outputs(nb: NotebookNode, identifier: str) -> list:
    return get_cell(nb, identifier).get("outputs", [])


def get_data_by_type(outputs: list, output_type: str) -> dict[str, str] | None:
    for output in outputs:
        if output["output_type"] == output_type:
            if output_type == "stream":
                return {"text/plain": output["text"]}

            return output["data"]

    return None


def get_stream(outputs: list) -> str | None:
    if data := get_data_by_type(outputs, "stream"):
        return data["text/plain"]

    return None


def get_data(outputs: list) -> dict[str, str]:
    for type_ in ["display_data", "execute_result", "stream"]:
        if data := get_data_by_type(outputs, type_):
            return data

    return {}


def get_language(nb: dict) -> str:
    return nb["metadata"]["kernelspec"]["language"]


def convert(data: dict[str, str]) -> dict[str, str]:
    text = data.get("text/plain")
    if text and text.startswith("%% Creator: Matplotlib, PGF backend"):
        data["text/plain"] = nbstore.pgf.convert(text)

    return data
