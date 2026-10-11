# Fix: MCPClient silently drops empty [] and {} tool arguments

**Issue:** #8045

## The Bug

`MCPClient._clean_tool_arguments` used `if nested_cleaned:` to decide whether to include a dict argument, and `if cleaned_list:` for list arguments. Both conditions evaluate to `False` for empty containers, so `{"tags": []}` and `{"filter": {}}` were silently dropped before reaching the MCP server.

```mermaid
flowchart TD
    A["LLM emits: {query: 'cats', tags: []}"] --> B[_clean_tool_arguments]
    B --> C["cleaned_list = []"]
    C --> D{"if cleaned_list:  ← False for empty list"}
    D -- False --> E["tags key NOT added to cleaned"]
    E --> F["MCP server receives: {query: 'cats'}"]
    F --> G["Server error or wrong behavior"]
```

## The Fix

Remove the truthiness guards. Empty `[]` and `{}` are valid, intentional values — only `None` should be skipped (already handled at the top of the loop).

```mermaid
flowchart TD
    A["LLM emits: {query: 'cats', tags: []}"] --> B[_clean_tool_arguments]
    B --> C["cleaned_list = []"]
    C --> D["cleaned[key] = []  ← always included"]
    D --> E["MCP server receives: {query: 'cats', tags: []}"]
    E --> F["Server handles empty list correctly"]
```

## PR Description

`MCPClient._clean_tool_arguments` silently discarded tool arguments whose value was an empty list `[]` or empty dict `{}`. The `if nested_cleaned:` and `if cleaned_list:` guards evaluated to `False` for empty containers, so the MCP server never received them — breaking tools with optional array/object parameters where the agent intentionally passes an empty value.

Remove the truthiness guards; only `None` values are skipped (handled at the top of the loop). Empty containers are now forwarded as-is.

Fixes #8045
