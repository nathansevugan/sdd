# Frontend — Angular

## Stack

| Concern | Choice |
|---------|--------|
| Framework | Angular 17+ (standalone components) |
| State | NgRx Signal Store |
| Styling | SCSS + design tokens |
| UI Kit | Angular Material (customised) |
| HTTP | `HttpClient` with interceptors |
| Forms | Reactive Forms only |
| i18n | `@angular/localize` |
| Testing | Jest + Angular Testing Library |
| Linting | ESLint + `@angular-eslint` |

---

## Project Structure

```
src/
├── app/
│   ├── core/                  # Singleton services, guards, interceptors
│   │   ├── auth/
│   │   ├── http/
│   │   └── logging/
│   ├── shared/                # Dumb components, pipes, directives
│   │   ├── components/
│   │   ├── pipes/
│   │   └── directives/
│   ├── features/              # Feature modules (lazy-loaded)
│   │   └── [feature]/
│   │       ├── data/          # Store, effects, selectors
│   │       ├── ui/            # Smart components
│   │       └── [feature].routes.ts
│   └── app.routes.ts
├── assets/
├── environments/
└── styles/
    ├── _tokens.scss
    ├── _typography.scss
    └── global.scss
```

---

## Component Rules

### Standalone + OnPush Always

```typescript
@Component({
  selector: 'sk-example',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './example.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExampleComponent {
  readonly label = input<string>('');
  readonly clicked = output<void>();
}
```

- `OnPush` on **every** component — no exceptions.
- Use `input()` / `output()` signals, not `@Input()` / `@Output()`.
- Zero business logic in templates.

### Smart vs Dumb

| Smart (Container) | Dumb (Presentational) |
|-------------------|-----------------------|
| Injects store/services | Props in, events out |
| Lives in `features/ui/` | Lives in `shared/components/` |
| No direct styling opinions | Fully self-contained styles |

---

## State — NgRx Signal Store

```typescript
export const WidgetStore = signalStore(
  withState<WidgetState>(initialState),
  withComputed(({ items }) => ({
    count: computed(() => items().length),
  })),
  withMethods((store, svc = inject(WidgetService)) => ({
    load: rxMethod<void>(pipe(
      switchMap(() => svc.getAll()),
      tapResponse({
        next: (items) => patchState(store, { items }),
        error: (err) => patchState(store, { error: err }),
      })
    )),
  }))
);
```

- One store per feature.
- No store in `shared/` — shared state goes in `core/`.

---

## HTTP & Interceptors

All HTTP goes through `core/http/`. Two mandatory interceptors:

```typescript
// 1. Auth — attaches JWT
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthStore).token();
  return next(token ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }) : req);
};

// 2. Error — maps to domain errors
export const errorInterceptor: HttpInterceptorFn = (req, next) =>
  next(req).pipe(catchError((err: HttpErrorResponse) => throwError(() => mapError(err))));
```

---

## Routing

- All feature routes are **lazy-loaded**.
- Guards use functional style (`CanActivateFn`).
- Route data carries breadcrumb/title metadata.

```typescript
export const routes: Routes = [
  {
    path: 'widgets',
    canActivate: [authGuard],
    loadChildren: () => import('./features/widgets/widgets.routes'),
    data: { title: 'Widgets' },
  },
];
```

---

## Forms

- Reactive Forms only — no `ngModel`.
- Validators extracted to `shared/validators/`.
- Error messages via a shared `sk-field-error` component.

---

## Styling Rules

- SCSS only; no inline styles.
- Import tokens from `styles/_tokens.scss`.
- BEM naming: `.sk-card__header--active`.
- No global overrides of Angular Material internals — use theme API.
- Dark mode via `prefers-color-scheme` media query on `:root`.
