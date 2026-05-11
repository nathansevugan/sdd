# Coding Standards

## General

- Max file length: **400 lines** — split if exceeded.
- Max function length: **30 lines**.
- No magic numbers — use named constants.
- Delete dead code; don't comment it out.
- All public APIs must have docstrings / TSDoc.

---

## Python

| Rule | Detail |
|------|--------|
| Version | 3.12+ — use match/case, `TypeAlias`, `dataclass` |
| Type hints | Mandatory on all function signatures |
| `Any` | Banned — narrow types explicitly |
| Async | All I/O functions must be `async def` |
| Nulls | Use `X \| None` + explicit checks — never return bare `None` from public methods without annotation |
| Logging | Structured via `structlog` — no f-string concatenation in log calls |
| Formatter | Ruff format (enforced by CI) |
| Type checker | mypy strict mode |

```python
# ✅
logger.info("widget_created", widget_id=str(widget.id), name=widget.name)

# ❌
logger.info(f"Widget created: {widget.id}")
```

---

## React / JavaScript

| Rule | Detail |
|------|--------|
| Language | JavaScript (JSX) — no TypeScript |
| `var` | Banned — use `const` / `let` only |
| Prop types | Use JSDoc `@param` comments on shared components |
| Component exports | Named exports only — no default component exports |
| Hook naming | Always prefix with `use` |
| Side effects | Only in `useEffect` or route loaders — never at module top-level |
| Formatter | Prettier (enforced by CI) |
| Linter | ESLint flat config + `eslint-plugin-react-hooks` |

```jsx
// ✅ Named export, const, destructured props
export function WidgetCard({ widget, onSelect }) {
  const { name, price } = widget
  return <div onClick={() => onSelect(widget.id)}>{name}</div>
}

// ❌ Banned
export default function widgetCard(props) {
  var name = props.widget.name
}
```

---

## Git & PR Rules

- Branch: `feat/`, `fix/`, `chore/`, `docs/`
- Commits: Conventional Commits (`feat: add widget endpoint`)
- PR size: < 400 lines changed (excluding generated/migration files)
- Every PR needs: passing CI + 1 reviewer approval
