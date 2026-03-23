"""
jCodeMunch integration service for AI Lab.
Provides token-efficient code search and retrieval using AST indexing.
"""
import os
import logging
from pathlib import Path
from django.conf import settings

logger = logging.getLogger(__name__)

# Storage path for the index (inside project dir)
INDEX_PATH = str(Path(settings.BASE_DIR) / '.code-index')

os.environ.setdefault('CODE_INDEX_PATH', INDEX_PATH)


def _get_repo_name():
    """Dynamically find the indexed repo name from storage."""
    try:
        from jcodemunch_mcp.storage import IndexStore
        store = IndexStore(base_path=INDEX_PATH)
        repos = store.list_repos()
        if repos:
            # Return the most recently indexed repo
            return repos[-1]['repo']
    except Exception:
        pass
    return 'AL_ML_TECH_DASHBOARD'


def _get_tools():
    """Lazy import to avoid loading at startup."""
    from jcodemunch_mcp.tools.index_folder import index_folder
    from jcodemunch_mcp.tools.search_symbols import search_symbols
    from jcodemunch_mcp.tools.search_text import search_text
    from jcodemunch_mcp.tools.get_symbol import get_symbol
    from jcodemunch_mcp.tools.get_file_outline import get_file_outline
    from jcodemunch_mcp.tools.get_file_tree import get_file_tree
    from jcodemunch_mcp.tools.get_repo_outline import get_repo_outline
    return {
        'index_folder': index_folder,
        'search_symbols': search_symbols,
        'search_text': search_text,
        'get_symbol': get_symbol,
        'get_file_outline': get_file_outline,
        'get_file_tree': get_file_tree,
        'get_repo_outline': get_repo_outline,
    }


def index_project(force=False):
    """
    Index the AI Lab Django project source code.
    Returns: dict with indexing result and stats.
    """
    tools = _get_tools()
    project_path = str(settings.BASE_DIR)

    result = tools['index_folder'](
        path=project_path,
        use_ai_summaries=False,
        storage_path=INDEX_PATH,
        extra_ignore_patterns=['venv', '__pycache__', '*.pyc', 'migrations', '.git'],
    )
    return result


def search_code_symbols(query, kind=None, language='python', max_results=8):
    """
    Search for code symbols (functions, classes, methods) by name/description.
    Returns token-efficient results (only matching symbols, not full files).
    """
    tools = _get_tools()
    return tools['search_symbols'](
        repo=_get_repo_name(),
        query=query,
        kind=kind,
        language=language,
        max_results=max_results,
        storage_path=INDEX_PATH,
    )


def search_code_text(query, max_results=10, context_lines=2):
    """
    Full-text search across all indexed source files.
    Useful for finding string literals, comments, config values.
    """
    tools = _get_tools()
    return tools['search_text'](
        repo=_get_repo_name(),
        query=query,
        max_results=max_results,
        context_lines=context_lines,
        storage_path=INDEX_PATH,
    )


def get_code_symbol(symbol_id, context_lines=3):
    """
    Retrieve full source code of a specific symbol by ID.
    """
    tools = _get_tools()
    return tools['get_symbol'](
        repo=_get_repo_name(),
        symbol_id=symbol_id,
        context_lines=context_lines,
        storage_path=INDEX_PATH,
    )


def get_file_symbols(file_path):
    """
    Get all symbols (classes, functions, methods) in a specific file.
    """
    tools = _get_tools()
    return tools['get_file_outline'](
        repo=_get_repo_name(),
        file_path=file_path,
        storage_path=INDEX_PATH,
    )


def get_project_outline():
    """
    Get high-level outline of the entire project (all files + top-level symbols).
    """
    tools = _get_tools()
    return tools['get_repo_outline'](
        repo=_get_repo_name(),
        storage_path=INDEX_PATH,
    )


def is_indexed():
    """Check if the project has been indexed."""
    index_dir = Path(INDEX_PATH)
    return index_dir.exists() and any(index_dir.rglob('*.json'))


def format_symbols_for_ai(search_result):
    """
    Convert jCodeMunch search results into a compact string for AI context.
    Much smaller than sending full file contents.
    """
    if 'error' in search_result:
        return f"[Code search error: {search_result['error']}]"

    results = search_result.get('results', [])
    if not results:
        return "[No matching symbols found]"

    lines = [f"Found {len(results)} symbol(s):\n"]
    for sym in results:
        lines.append(f"• {sym['kind'].upper()} `{sym['name']}`")
        lines.append(f"  File: {sym['file']} (line {sym['line']})")
        if sym.get('signature'):
            lines.append(f"  Sig:  {sym['signature']}")
        if sym.get('summary'):
            lines.append(f"  Info: {sym['summary']}")
        lines.append(f"  ID:   {sym['id']}")
        lines.append("")

    meta = search_result.get('_meta', {})
    if meta.get('tokens_saved'):
        lines.append(f"[Token savings: {meta['tokens_saved']:,} tokens vs reading full files]")

    return "\n".join(lines)


def format_symbol_source_for_ai(symbol_result):
    """Format a single symbol's source code for AI context."""
    if 'error' in symbol_result:
        return f"[Symbol lookup error: {symbol_result['error']}]"

    name = symbol_result.get('name', 'unknown')
    kind = symbol_result.get('kind', 'symbol')
    file_path = symbol_result.get('file', '')
    line = symbol_result.get('line', 0)
    source = symbol_result.get('source', '')

    return f"```python\n# {kind}: {name} — {file_path}:{line}\n{source}\n```"
