"""Utilities for persisting tab content to JSON files.

Function: persist_tab_content(tab_id, tab_content, tabs_data)
Behavior:
  - Ensures folder dash_app/tabs/{tab_id}/ exists.
  - If folder is missing or empty, creates it and writes {tab_id}_data.json.
  - If folder already exists (regardless of contents), overwrites {tab_id}_data.json with new content.
  - Attempts to JSON-serialize `tab_content`; if not directly serializable (e.g. Dash component), stores a repr.
  - Returns the (unmodified) tabs_data for convenience so it can be used in Dash callback chains.

Note:
Dash (Mantine) component objects are not inherently JSON serializable. This utility falls back to a string representation
so the file write does not fail. If you later need to reconstruct the component, you should instead persist the raw
parameters used to build it rather than the component instance itself.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Sequence, List
import shutil


def _get_tab_base_dir() -> Path:
    """Return the base directory where tab folders are stored (dash_app/tabs)."""
    # This file lives at dash_app/components/tab_components/tab_storage.py
    # parents[0] -> tab_components
    # parents[1] -> components
    # parents[2] -> dash_app
    return Path(__file__).parents[2] / "tabs"


def persist_tab_content(tab_id: str, tab_content: Any, tabs_data: Dict[str, Any]) -> Dict[str, Any]:
    """Persist a tab's content into dash_app/tabs/{tab_id}/{tab_id}_data.json.

    Parameters
    ----------
    tab_id : str
        Unique identifier of the tab.
    tab_content : Any
        The content to store. If not JSON-serializable, a repr() will be stored instead.
    tabs_data : Dict[str, Any]
        Existing tabs data structure (returned unchanged for chaining).

    Returns
    -------
    Dict[str, Any]
        The original `tabs_data` (unmodified).
    """
    base_dir = _get_tab_base_dir() / tab_id
    base_dir.mkdir(parents=True, exist_ok=True)

    data_file = base_dir / f"{tab_id}_data.json"

    # Decide what to serialize
    serializable = tab_content
    try:
        json.dumps(serializable)
    except TypeError:
        # Fallback for non-serializable objects (e.g. Dash components)
        serializable = {"repr": repr(tab_content)}

    payload = {
        "tab_id": tab_id,
        "content": serializable,
    }

    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    return tabs_data


__all__ = ["persist_tab_content"]


def list_tab_directories() -> List[str]:
    """Return the list of existing tab directory names under dash_app/tabs.

    If the base directory doesn't exist yet, returns an empty list.
    """
    base = _get_tab_base_dir()
    if not base.exists():
        return []
    return [p.name for p in base.iterdir() if p.is_dir()]


def cleanup_tabs_not_in(tab_id_list: Sequence[str]) -> List[str]:
    """Delete any tab directories not present in `tab_id_list`.

    Parameters
    ----------
    tab_id_list : Sequence[str]
        The set of tab IDs to keep.

    Returns
    -------
    List[str]
        The list of tab IDs (folder names) that were removed.
    """
    base = _get_tab_base_dir()
    if not base.exists():
        return []

    keep: set[str] = set(tab_id_list)
    removed: List[str] = []

    for path in base.iterdir():
        if path.is_dir() and path.name not in keep:
            try:
                shutil.rmtree(path)
                removed.append(path.name)
            except Exception:
                # Best-effort cleanup; skip failures silently or log if desired
                pass

    return removed


__all__.extend(["list_tab_directories", "cleanup_tabs_not_in"])
