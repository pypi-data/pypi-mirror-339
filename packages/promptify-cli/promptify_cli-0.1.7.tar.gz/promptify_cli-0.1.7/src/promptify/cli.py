#!/usr/bin/env python3
import typer
import os
import json
from pathlib import Path
import mimetypes
import pyperclip
from gitignore_parser import parse_gitignore
import tiktoken
import nbformat
from nbconvert import MarkdownExporter
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style as PromptStyle
from prompt_toolkit.data_structures import Point
from appdirs import user_config_dir
import chardet
from collections import namedtuple, defaultdict
import re

APP_NAME = "PromptSelector"
CONFIG_DIR = Path(user_config_dir(APP_NAME, ""))
STATE_FILE = CONFIG_DIR / "state.json"
DEFAULT_DEPTH = 4
IGNORE_FILE_NAME = ".promptignore"
TIKTOKEN_ENCODING = "o200k_base"

try:
    encoding = tiktoken.get_encoding(TIKTOKEN_ENCODING)
except Exception as e:
    print(
        f"Warning: Could not load tiktoken encoding '{TIKTOKEN_ENCODING}'. Token count will be character count. Error: {e}"
    )
    encoding = None


def ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_state() -> set:
    ensure_config_dir()
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                return set(json.load(f))
        except (json.JSONDecodeError, IOError) as e:
            print(
                f"Warning: Could not load previous state from {STATE_FILE}. Starting fresh."
            )
            return set()
    return set()


def save_state(selected_paths: set, cwd: Path):
    ensure_config_dir()
    try:
        relative_paths = sorted([str(p.relative_to(cwd)) for p in selected_paths])
        with open(STATE_FILE, "w") as f:
            json.dump(relative_paths, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save state to {STATE_FILE}. Error: {e}")
    except ValueError as e:
        print(f"Warning: Could not save state due to path issue: {e}")


def get_ignore_matcher(start_dir: Path, clear_state: bool) -> callable:
    ignore_file = start_dir / IGNORE_FILE_NAME
    if ignore_file.is_file():
        try:
            return parse_gitignore(ignore_file)
        except Exception as e:
            print(
                f"Warning: Could not read {ignore_file}. Proceeding without ignore rules. Error: {e}"
            )
    else:
        ensure_config_dir()
        promptignore_state_file = CONFIG_DIR / "promptignore_offered.txt"
        if not promptignore_state_file.exists() or clear_state:
            answer = typer.confirm(
                f"No {typer.style(IGNORE_FILE_NAME, bold=True)} file found. Would you "
                "like to create one with default rules?",
                default=False,
            )
            try:
                with open(promptignore_state_file, "w") as f:
                    f.write("offered")
            except Exception:
                pass
            if answer:
                try:
                    default_ignore_content = """# Default .promptignore file
# Version control
.git/
.gitignore
.svn/
.hg/

# Dependencies
node_modules/
venv/
env/
.env/
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Build artifacts and logs
dist/
build/
*.o
*.so
*.dll
*.exe
*.out
*.log
logs/
log/

# Editor and IDE files
.vscode/
.idea/
*.swp
*~
.DS_Store

# Large data files
*.csv
*.tsv
*.pkl
*.h5
*.parquet
*.sqlite
*.db

# Add your own patterns here
"""
                    with open(start_dir / IGNORE_FILE_NAME, "w") as f:
                        f.write(default_ignore_content)
                    typer.echo(f"Created {IGNORE_FILE_NAME} with default rules.")
                    return parse_gitignore(start_dir / IGNORE_FILE_NAME)
                except Exception as e:
                    typer.echo(
                        f"Warning: Could not create {IGNORE_FILE_NAME}. Proceeding without ignore rules. Error: {e}"
                    )
    return lambda x: False


def is_likely_text_file(file_path: Path) -> bool:
    if not file_path.is_file():
        return False
    non_text_exts = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".tiff",
        ".webp",
        ".mp3",
        ".wav",
        ".ogg",
        ".flac",
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
        ".zip",
        ".gz",
        ".tar",
        ".rar",
        ".7z",
        ".exe",
        ".dll",
        ".so",
        ".dylib",
        ".app",
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".o",
        ".a",
        ".obj",
        ".lib",
        ".pyc",
        ".pyd",
        ".egg",
        ".whl",
        ".db",
        ".sqlite",
        ".sqlite3",
        ".dat",
        ".bin",
    }
    if file_path.suffix.lower() in non_text_exts:
        return False
    mime_type, _ = mimetypes.guess_type(file_path)
    if (
        mime_type
        and not mime_type.startswith("text/")
        and mime_type
        not in (
            "application/json",
            "application/xml",
            "application/javascript",
            "application/x-python",
            "application/x-sh",
        )
        and not mime_type.endswith("+xml")
        and mime_type != "application/octet-stream"
        and file_path.suffix != ".ipynb"
    ):
        return False
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            if b"\x00" in chunk:
                return False
            try:
                detected_encoding = chardet.detect(chunk)["encoding"]
                chunk.decode(detected_encoding or "utf-8")
            except (UnicodeDecodeError, TypeError):
                return False
    except IOError:
        return False
    return True


def convert_ipynb_to_markdown(file_path: Path) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)
        md_exporter = MarkdownExporter(exclude_output_prompt=True, exclude_raw=True)
        (body, resources) = md_exporter.from_notebook_node(notebook)
        header = f"--- Content from {file_path.name} ---\n\n"
        return header + body
    except Exception as e:
        return f"Error converting notebook {file_path.name}: {e}"


def get_file_content(file_path: Path) -> str:
    if not file_path.is_file():
        return f"Error: {file_path.name} is not a file."
    if file_path.suffix == ".ipynb":
        return convert_ipynb_to_markdown(file_path)
    else:
        try:
            with open(file_path, "rb") as f:
                raw_data = f.read()
            detected_encoding = chardet.detect(raw_data)["encoding"]
            with open(
                file_path, "r", encoding=detected_encoding or "utf-8", errors="replace"
            ) as f:
                return f.read()
        except Exception as e:
            return f"Error reading file {file_path.name}: {e}"


def count_tokens(text: str) -> int:
    if encoding:
        try:
            return len(encoding.encode(text))
        except Exception as e:
            return len(text)
    else:
        return len(text)


def count_lines(text: str) -> int:
    """Counts the number of lines in a string."""
    return text.count("\n") + 1 if text else 0


def fence_code_block(content: str, lang: str = "") -> str:
    """
    Wraps content in a code block using a fence that adapts if the content
    already contains triple backticks.
    """
    fence = "```"
    if "```" in content:
        matches = re.findall(r"(`+)", content)
        if matches:
            max_len = max(len(match) for match in matches)
            fence = "`" * (max(max_len + 1, 3))
    return f"{fence}{lang}\n{content}\n{fence}"


def generate_pretty_tree_for_markdown(all_paths: set[Path], cwd: Path) -> str:
    tree_lines = []
    parent_map = defaultdict(list)

    for p in all_paths:
        if p == cwd or p.name in IGNORE_FILE_NAME:
            continue
        parent_map[p.parent].append(p)

    def sort_key_local(p: Path):
        name = p.name.lower()
        is_dir = p.is_dir()
        is_dotfile = not is_dir and name.startswith(".")
        type_priority = 0 if is_dir else (2 if is_dotfile else 1)
        return (type_priority, name)

    for parent_path in parent_map:
        parent_map[parent_path].sort(key=sort_key_local)

    def dfs_build_tree(dir_path: Path, prefix: str = ""):
        children = parent_map.get(dir_path, [])
        for i, child_path in enumerate(children):
            is_last = i == len(children) - 1
            connector = "└─ " if is_last else "├─ "
            line = prefix + connector + child_path.name
            if child_path.is_dir():
                line += "/"
            tree_lines.append(line)
            if child_path.is_dir():
                new_prefix = prefix + ("   " if is_last else "│  ")
                dfs_build_tree(child_path, new_prefix)

    tree_lines.append(cwd.name + "/")
    dfs_build_tree(cwd)
    return "\n".join(tree_lines)


def generate_markdown_output(
    all_scanned_paths: set[Path], selected_paths: set[Path], cwd: Path, max_depth: int
) -> tuple[str, int]:
    """Generates the final markdown string and calculates total tokens."""
    tree_str = generate_pretty_tree_for_markdown(all_scanned_paths, cwd)
    content_blocks = []
    total_content_for_tokens = ""
    sorted_selected_paths = sorted(
        list(selected_paths), key=lambda p: p.relative_to(cwd).parts
    )

    for file_path in sorted_selected_paths:
        relative_path_str = str(file_path.relative_to(cwd))
        content = get_file_content(file_path)
        file_block_for_tokens = (
            f"\n\n---\n\nFile: {relative_path_str}\n\n{fence_code_block(content)}\n\n"
        )
        total_content_for_tokens += file_block_for_tokens
        lang = file_path.suffix.lstrip(".").lower()
        lang_map = {
            "py": "python",
            "js": "javascript",
            "ts": "typescript",
            "md": "markdown",
            "sh": "bash",
            "ipynb": "markdown",
            "yaml": "yaml",
            "yml": "yaml",
            "json": "json",
            "html": "html",
            "css": "css",
            "xml": "xml",
        }
        md_lang = lang_map.get(lang, "")
        content_blocks.append(
            f"## File: `{relative_path_str}`\n\n{fence_code_block(content, md_lang)}"
        )

    markdown_string = (
        f"Project Structure (Depth: {max_depth}):\n\n```\n{tree_str}\n```\n\n"
        + "---\n\n"
        + "\n\n---\n\n".join(content_blocks)
    )
    token_text = tree_str + total_content_for_tokens
    total_tokens = count_tokens(token_text)
    return markdown_string, total_tokens


DisplayItem = namedtuple("DisplayItem", ["path", "is_dir", "depth"])


class FileSelectorTUI:
    def __init__(self, all_paths: list[Path], initial_selection: set[Path], cwd: Path):
        self.all_paths = all_paths
        self.selected_paths = initial_selection
        self.cwd = cwd
        self.current_index = 0
        self.message = ""
        self.token_count = 0
        self.loc_count = 0
        self.running = True
        self.collapsed_dirs = set()

        self.display_items = self._build_display_items_dfs_with_root()
        self._set_initial_collapse_state(initial_selection)
        self._rebuild_visible_items()
        self._recalculate_counts()

        self.style = PromptStyle.from_dict(
            {
                "file": "#ffffff",
                "file-dot": "#bbbbbb",
                "dir": "#aaaaaa",
                "dir-root": "#dddddd bold",
                "selected-file": "fg:ansigreen",
                "selected-file-dot": "fg:ansigreen",
                "highlight": "bg:#444444 #ffffff bold",
                "highlight-root": "bg:#444444 #dddddd bold",
                "highlight-sel-file": "bg:#444444 fg:ansigreen bold",
                "highlight-sel-dot": "bg:#444444 fg:ansigreen bold",
                "ignored": "#666666",
                "header": "bg:#005f87 #ffffff bold",
                "status": "bg:#222222 #ffffff",
                "token": "#00ff00 bold",
                "loc": "#ffff00 bold",
                "collapse-marker": "fg:#ffcc00",
                "tree-line": "fg:#555555",
                "count-indicator": "fg:ansicyan",
            }
        )

        kb = KeyBindings()

        @kb.add("up")
        def _(event):
            if self.current_index > 0:
                self.current_index -= 1
                self.message = ""
                event.app.invalidate()

        @kb.add("down")
        def _(event):
            max_index = len(self.visible_items) - 1
            if self.current_index < max_index:
                self.current_index += 1
                self.message = ""
                event.app.invalidate()

        @kb.add("enter")
        def _(event):
            if not self.visible_items:
                return
            current_item = self.visible_items[self.current_index]
            if current_item.path == self.cwd:
                self.message = "Root directory cannot be collapsed/selected."
                return
            if current_item.is_dir:
                if current_item.path in self.collapsed_dirs:
                    self.collapsed_dirs.remove(current_item.path)
                    self.message = (
                        f"Expanded: {current_item.path.relative_to(self.cwd)}"
                    )
                else:
                    self.collapsed_dirs.add(current_item.path)
                    self.message = (
                        f"Collapsed: {current_item.path.relative_to(self.cwd)}"
                    )
                self._rebuild_visible_items()
            else:
                if current_item.path in self.selected_paths:
                    self.selected_paths.remove(current_item.path)
                    self.message = (
                        f"Deselected: {current_item.path.relative_to(self.cwd)}"
                    )
                else:
                    self.selected_paths.add(current_item.path)
                    self.message = (
                        f"Selected: {current_item.path.relative_to(self.cwd)}"
                    )
                self._recalculate_counts()

        @kb.add("a")
        def _(event):
            if not self.visible_items:
                return
            current_item = self.visible_items[self.current_index]
            target_dir = None
            if current_item.path == self.cwd:
                target_dir = self.cwd
                dir_name = "root directory"
            elif current_item.is_dir:
                target_dir = current_item.path
                dir_name = str(current_item.path.relative_to(self.cwd))
            else:
                self.message = "Press 'a' on a directory to select all within it."
                return
            if target_dir:
                files_to_select = self._get_selectable_files_in_dir(target_dir)
                added_count = len(files_to_select - self.selected_paths)
                self.selected_paths.update(files_to_select)
                self.message = f"Selected {added_count} file(s) in {dir_name}"
                self._recalculate_counts()

        @kb.add("r")
        def _(event):
            if not self.visible_items:
                return
            current_item = self.visible_items[self.current_index]
            target_dir = None
            if current_item.path == self.cwd:
                target_dir = self.cwd
                dir_name = "root directory"
            elif current_item.is_dir:
                target_dir = current_item.path
                dir_name = str(current_item.path.relative_to(self.cwd))
            else:
                self.message = "Press 'r' on a directory to deselect all within it."
                return
            if target_dir:
                files_to_deselect = self._get_selectable_files_in_dir(target_dir)
                removed_count = len(self.selected_paths.intersection(files_to_deselect))
                self.selected_paths.difference_update(files_to_deselect)
                self.message = f"Deselected {removed_count} file(s) in {dir_name}"
                self._recalculate_counts()

        @kb.add("c-c")
        @kb.add("escape")
        def _(event):
            self.selected_paths = None
            self.running = False
            event.app.exit()

        @kb.add("s")
        def _(event):
            self.running = False
            event.app.exit()

        header_text = FormattedText(
            [
                ("class:header", " Prompt Selector "),
                (
                    "",
                    " | Arrows: Nav | Enter: Toggle | a/r: Select/Deselect Dir | s: Confirm & Copy | Esc/Ctrl+C: Quit",
                ),
            ]
        )
        self.text_area_control = FormattedTextControl(
            text=self._get_formatted_text,
            focusable=True,
            key_bindings=kb,
            get_cursor_position=lambda: Point(x=0, y=self.current_index),
        )
        self.status_bar = FormattedTextControl(text=self._get_status_text)
        self.main_window = Window(content=self.text_area_control)
        layout = Layout(
            HSplit(
                [
                    Window(
                        FormattedTextControl(header_text),
                        height=1,
                        style="class:header",
                    ),
                    self.main_window,
                    Window(self.status_bar, height=1, style="class:status"),
                ]
            ),
            focused_element=self.text_area_control,
        )
        self.app = Application(
            layout=layout,
            full_screen=True,
            key_bindings=kb,
            style=self.style,
            mouse_support=True,
        )

    def _get_selectable_files_in_dir(self, dir_path: Path) -> set[Path]:
        selectable_files = set()
        for item in self.display_items:
            if item.path == self.cwd:
                continue
            if not item.is_dir:
                try:
                    if dir_path == self.cwd or item.path.is_relative_to(dir_path):
                        selectable_files.add(item.path)
                except ValueError:
                    pass
        return selectable_files

    def _get_selected_count_in_dir(self, dir_path: Path) -> int:
        count = 0
        for selected_file_path in self.selected_paths:
            try:
                if dir_path == self.cwd:
                    if selected_file_path != self.cwd:
                        count += 1
                elif selected_file_path.is_relative_to(dir_path):
                    count += 1
            except ValueError:
                pass
        return count

    def _build_display_items_dfs_with_root(self) -> list[DisplayItem]:
        items_map = {}
        parent_map = {self.cwd: []}
        all_present_paths = set(self.all_paths)
        required_dirs = set()
        for p in self.all_paths:
            parent = p.parent
            while parent != self.cwd.parent:
                if parent == self.cwd:
                    break
                required_dirs.add(parent)
                parent = parent.parent
        all_present_paths.update(required_dirs)
        for p in all_present_paths:
            if p == self.cwd or p.name == IGNORE_FILE_NAME:
                continue
            try:
                relative_path = p.relative_to(self.cwd)
                depth = len(relative_path.parts) - 1
                is_dir = p in required_dirs or p.is_dir()
                item = DisplayItem(p, is_dir=is_dir, depth=depth)
                items_map[p] = item
                parent_path = p.parent
                if parent_path not in parent_map:
                    parent_map[parent_path] = []
                if item not in parent_map[parent_path]:
                    parent_map[parent_path].append(item)
            except ValueError:
                pass

        def sort_key_local(item: DisplayItem):
            name = item.path.name.lower()
            is_dir = item.is_dir
            is_dotfile = not is_dir and name.startswith(".")
            type_priority = 0 if is_dir else (2 if is_dotfile else 1)
            return (type_priority, name)

        for parent_path in parent_map:
            parent_map[parent_path].sort(key=sort_key_local)
        ordered_children = []
        visited_items = set()

        def dfs_flatten(dir_path):
            children = parent_map.get(dir_path, [])
            for item in children:
                if item.path not in visited_items:
                    ordered_children.append(item)
                    visited_items.add(item.path)
                    if item.is_dir:
                        dfs_flatten(item.path)

        dfs_flatten(self.cwd)
        root_item = DisplayItem(path=self.cwd, is_dir=True, depth=-1)
        final_ordered_list = [root_item] + ordered_children
        return final_ordered_list

    def _set_initial_collapse_state(self, initial_selection: set[Path]):
        self.collapsed_dirs.clear()
        selected_parents = set()
        for sel_path in initial_selection:
            parent = sel_path.parent
            while parent != self.cwd.parent:
                if parent == self.cwd:
                    break
                selected_parents.add(parent)
                parent = parent.parent
        for item in self.display_items:
            if item.path == self.cwd:
                continue
            if item.is_dir and item.path not in selected_parents:
                self.collapsed_dirs.add(item.path)

    def _rebuild_visible_items(self):
        self.visible_items = []
        for item in self.display_items:
            if item.path == self.cwd:
                self.visible_items.append(item)
                continue
            is_child_of_collapsed = False
            parent = item.path.parent
            while parent != self.cwd.parent:
                if parent == self.cwd:
                    break
                if parent in self.collapsed_dirs:
                    is_child_of_collapsed = True
                    break
                parent = parent.parent
            if not is_child_of_collapsed:
                self.visible_items.append(item)
        if self.current_index >= len(self.visible_items):
            self.current_index = max(0, len(self.visible_items) - 1)
        elif self.current_index < 0:
            self.current_index = 0

    def _recalculate_counts(self):
        content_to_count = ""
        total_loc = 0
        sorted_selection = sorted(list(self.selected_paths), key=lambda p: p.parts)
        for path in sorted_selection:
            if path == self.cwd:
                continue
            content = get_file_content(path)
            total_loc += count_lines(content)
            relative_path_str = str(path.relative_to(self.cwd))
            content_to_count += (
                f"\n---\nFile: {relative_path_str}\n```\n{content}\n```\n"
            )
        self.token_count = count_tokens(content_to_count)
        self.loc_count = total_loc

    def _get_status_text(self) -> FormattedText:
        token_str = f"{self.token_count:,}"
        token_unit = "tokens" if encoding else "chars"
        loc_str = f"{self.loc_count:,}"
        user_visible_total = max(0, len(self.display_items) - 1)
        user_visible_current = max(0, len(self.visible_items) - 1)
        return FormattedText(
            [
                (
                    "class:status",
                    f" Items: {user_visible_current}/{user_visible_total} | Sel Files: {len(self.selected_paths)} | ",
                ),
                ("class:loc", f"{loc_str} LOC"),
                ("class:status", " | "),
                ("class:token", f"{token_str} {token_unit}"),
                ("class:status", f" | {self.message}"),
            ]
        )

    def _get_formatted_text(self) -> FormattedText:
        result_fragments = []
        if not self.visible_items:
            return FormattedText([("class:ignored", " No items to display.")])
        last_visible_in_parent = set()
        parent_map_visible = {}
        for item in self.visible_items:
            if item.path == self.cwd:
                continue
            parent = item.path.parent
            if parent not in parent_map_visible:
                parent_map_visible[parent] = []
            parent_map_visible[parent].append(item.path)
        for parent, children in parent_map_visible.items():
            if children:
                last_visible_in_parent.add(children[-1])
        for i, item in enumerate(self.visible_items):
            is_current = i == self.current_index
            path = item.path
            current_depth = item.depth
            item_name_style = ""
            highlight_style_class = "class:highlight"
            is_dotfile = not item.is_dir and path.name.startswith(".")
            is_selected_file = not item.is_dir and path in self.selected_paths
            if path == self.cwd:
                item_name_style = "class:dir-root"
            elif item.is_dir:
                item_name_style = "class:dir"
            elif is_selected_file:
                item_name_style = (
                    "class:selected-file-dot" if is_dotfile else "class:selected-file"
                )
            else:
                item_name_style = "class:file-dot" if is_dotfile else "class:file"
            if is_current:
                if path == self.cwd:
                    highlight_style_class = "class:highlight-root"
                elif is_selected_file:
                    highlight_style_class = (
                        "class:highlight-sel-dot"
                        if is_dotfile
                        else "class:highlight-sel-file"
                    )
                item_name_style = highlight_style_class
            prefix_fragments = []
            prefix_fragments.append(
                (item_name_style if is_current else "", "> " if is_current else "  ")
            )
            if path == self.cwd:
                cwd_display_name = self.cwd.name + "/"
                result_fragments.extend(prefix_fragments)
                result_fragments.append((item_name_style, cwd_display_name + "\n"))
                continue
            relative_parts = item.path.relative_to(self.cwd).parts
            for d in range(current_depth):
                ancestor_path = self.cwd.joinpath(*relative_parts[: d + 1])
                is_last_sibling_at_level = ancestor_path in last_visible_in_parent
                tree_style = (
                    f"class:tree-line {highlight_style_class}"
                    if is_current
                    else "class:tree-line"
                )
                prefix_fragments.append(
                    (tree_style, "   " if is_last_sibling_at_level else "│  ")
                )
            is_last_child = path in last_visible_in_parent
            connector = "└─ " if is_last_child else "├─ "
            connector_style = (
                f"class:tree-line {highlight_style_class}"
                if is_current
                else "class:tree-line"
            )
            prefix_fragments.append((connector_style, connector))
            item_name = path.name
            count_indicator = ""
            if item.is_dir:
                is_collapsed = path in self.collapsed_dirs
                collapse_marker = "[+]" if is_collapsed else "[-]"
                if is_collapsed:
                    count = self._get_selected_count_in_dir(path)
                    if count > 0:
                        count_indicator = f" ({count})"
                marker_style = (
                    f"class:collapse-marker {highlight_style_class}"
                    if is_current
                    else "class:collapse-marker"
                )
                count_style = (
                    f"class:count-indicator {highlight_style_class}"
                    if is_current
                    else "class:count-indicator"
                )
                space_style = highlight_style_class if is_current else ""
                prefix_fragments.append((marker_style, collapse_marker))
                if count_indicator:
                    prefix_fragments.append((count_style, count_indicator))
                prefix_fragments.append((space_style, " "))
                item_name += "/"
            result_fragments.extend(prefix_fragments)
            result_fragments.append((item_name_style, item_name + "\n"))
        return FormattedText(result_fragments)

    def run(self) -> set | None:
        try:
            self.app.run()
        except Exception as e:
            print(f"\nError running TUI: {e}")
            return self.selected_paths
        finally:
            pass
        return self.selected_paths


app = typer.Typer(
    help="Interactive CLI to select files, generate markdown, and copy to clipboard."
)


@app.command()
def main(
    depth: int = typer.Option(
        DEFAULT_DEPTH,
        "--depth",
        "-d",
        help="Maximum directory depth to scan relative to start path (0=root only).",
    ),
    path: Path = typer.Option(
        Path.cwd(),
        "--path",
        "-p",
        help="Starting directory path.",
        exists=True,
        file_okay=False,
        resolve_path=True,
    ),
    clear_state: bool = typer.Option(
        False, "--clear-state", help="Clear previous selections before starting."
    ),
):
    """
    Scans directories respecting .promptignore, allows interactive file selection
    (with collapsible folders sorted dirs>files>dotfiles), and copies formatted
    markdown of selected files to the clipboard.
    """
    typer.echo(f"Scanning directory: {path} (max depth: {depth})")

    try:
        ignore_matcher = get_ignore_matcher(path, clear_state)
    except Exception as e:
        typer.secho(f"Error loading .promptignore: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    initial_selection_rel_paths = load_state() if not clear_state else set()
    initial_selection_abs = set()
    if initial_selection_rel_paths:
        for rel_path_str in initial_selection_rel_paths:
            abs_path = (path / rel_path_str).resolve()
            if abs_path.is_file():
                initial_selection_abs.add(abs_path)

    all_scanned_paths = set()
    all_found_files = []

    for root, dirs, files in os.walk(path, topdown=True, followlinks=False):
        root_path = Path(root).resolve()
        try:
            relative_root = root_path.relative_to(path)
            current_depth = len(relative_root.parts)
        except ValueError:
            dirs[:] = []
            continue

        if current_depth > depth:
            dirs[:] = []
            files[:] = []
            continue
        elif root_path != path:
            if ignore_matcher(str(root_path)) or root_path.name == IGNORE_FILE_NAME:
                dirs[:] = []
                files[:] = []
                continue
            else:
                all_scanned_paths.add(root_path)

        original_dirs = list(dirs)
        dirs[:] = []
        for d in original_dirs:
            dir_abs_path = root_path / d
            dir_rel_path = dir_abs_path.relative_to(path)
            if len(dir_rel_path.parts) <= depth:
                if (
                    not ignore_matcher(str(dir_abs_path))
                    and dir_abs_path.name != IGNORE_FILE_NAME
                ):
                    dirs.append(d)
                    all_scanned_paths.add(dir_abs_path)

        for f in files:
            file_abs_path = root_path / f
            file_rel_path = file_abs_path.relative_to(path)
            if file_abs_path.name == IGNORE_FILE_NAME:
                continue
            if len(file_rel_path.parts) > depth:
                continue
            if ignore_matcher(str(file_abs_path)):
                continue
            all_scanned_paths.add(file_abs_path)
            if is_likely_text_file(file_abs_path):
                all_found_files.append(file_abs_path)

    if not all_found_files:
        typer.echo(
            f"No suitable text files found within depth {depth} respecting ignore rules."
        )
        raise typer.Exit()

    typer.echo(
        f"Found {len(all_found_files)} text files ({len(all_scanned_paths)} total items). Launching selector..."
    )

    selector_tui = FileSelectorTUI(all_found_files, initial_selection_abs, path)
    final_selected_paths = selector_tui.run()

    if final_selected_paths is None:
        typer.echo("Operation cancelled by user.")
        raise typer.Exit()
    final_selected_paths = final_selected_paths or set()
    if not final_selected_paths:
        typer.echo("No files were selected.")
        save_state(set(), path)
        raise typer.Exit()

    typer.echo(f"Processing {len(final_selected_paths)} selected files...")

    try:
        markdown_output, final_token_count = generate_markdown_output(
            all_scanned_paths=all_scanned_paths,
            selected_paths=final_selected_paths,
            cwd=path,
            max_depth=depth,
        )
        token_unit = "tokens" if encoding else "characters"
    except Exception as e:
        typer.echo(f"Error: Could not generate final markdown content: {e}", err=True)
        raise typer.Exit(code=1)

    try:
        pyperclip.copy(markdown_output)
    except Exception as e:
        if "clipboard mechanism not found" in str(e).lower():
            typer.echo(
                f"Error: Pyperclip couldn't find a copy/paste mechanism.", err=True
            )
            typer.echo(
                "Install xclip/xsel (Linux) or check system integration.", err=True
            )
        else:
            typer.echo(f"Error: Could not copy to clipboard: {e}", err=True)
        typer.echo("\n--- Generated Markdown Content (showing here as fallback) ---")
        typer.echo(markdown_output)
        typer.echo("--- End Content ---")
        raise typer.Exit(code=1)

    save_state(final_selected_paths, path)

    typer.secho(
        f"\nSuccess! Formatted content for {len(final_selected_paths)} files ({final_token_count} {token_unit}) copied to clipboard.",
        fg=typer.colors.GREEN,
        bold=True,
    )


if __name__ == "__main__":
    app()
