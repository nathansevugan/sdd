# Frontend — React

## Stack

| Concern | Choice |
|---------|--------|
| Framework | React 19 |
| Language | JavaScript (JSX) |
| State | `useState` / `useReducer` (local) |
| Styling | CSS files |
| HTTP | `fetch` |
| Linting | ESLint (flat config) |
| Build | Vite 8 |

---

## Project Structure

```
daily-wisdom-ui/
├── public/
│   ├── favicon.svg
│   └── icons.svg
├── src/
│   ├── assets/
│   │   ├── hero.png
│   │   ├── react.svg
│   │   └── vite.svg
│   ├── App.css
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
├── index.html
├── package.json
├── vite.config.js
└── eslint.config.js
```

---

## Component Structure

```jsx
// src/App.jsx
import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="app">
      <h1>Daily Wisdom</h1>
      <button onClick={() => setCount((count) => count + 1)}>
        Count is {count}
      </button>
    </div>
  )
}

export default App
```

---

## State Management

### Local State
```jsx
const [isOpen, setIsOpen] = useState(false)
const [state, dispatch] = useReducer(reducer, initialState)
```

---

## HTTP & API

```jsx
// Simple fetch wrapper
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001'

export async function apiFetch(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })
  
  if (!res.ok) {
    throw new Error(`API request failed: ${res.status}`)
  }
  
  return res.json()
}

// Usage example
export async function getDailyWisdom() {
  return apiFetch('/api/wisdom')
}
```

---

## Styling

- Global CSS files in `src/`
- Component-specific styles imported directly
- CSS custom properties for design tokens

```css
/* src/index.css */
:root {
  --color-primary: #0F62FE;
  --color-bg: #F4F4F4;
  --color-text: #161616;
  --space-md: 16px;
  --radius-md: 4px;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  background-color: var(--color-bg);
  color: var(--color-text);
}
```

---

## Accessibility

- All interactive elements keyboard-navigable
- Include `aria-label` on icon-only buttons
- Colour contrast ≥ 4.5:1
- Use semantic HTML elements
