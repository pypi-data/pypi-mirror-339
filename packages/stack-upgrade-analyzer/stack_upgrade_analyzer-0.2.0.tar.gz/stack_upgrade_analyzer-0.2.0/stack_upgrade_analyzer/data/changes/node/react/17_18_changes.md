# Breaking Changes: react 17 → 18
> Generated on: 2025-04-09T14:55:08.118012
> Stack: react
> Current Version: 17
> Upgrade Version: 18

# Comprehensive Guide to Breaking Changes, Deprecations, and API Modifications: React 17 to React 18

## 1. Summary of Major Changes
React 18 introduces significant updates, including:
- A new concurrent rendering architecture.
- Automatic batching of state updates.
- New APIs like `createRoot` and `hydrateRoot`.
- New hooks such as `useTransition`, `useDeferredValue`, and `useId`.
- Stricter hydration error handling.
- Deprecation of `ReactDOM.render` and `ReactDOM.hydrate`.
- Dropped support for Internet Explorer.

These changes aim to improve performance, developer experience, and compatibility with modern web standards.

---

## 2. Breaking Changes Organized by Version

### **React 18 Breaking Changes**
React 18 introduces several breaking changes and deprecations that require updates to existing codebases.

---

## 3. Detailed List of Breaking Changes

### **1. Deprecation of `ReactDOM.render`**
- **Affected API**: `ReactDOM.render`
- **What Changed**: The `ReactDOM.render` method is deprecated and replaced by `ReactDOM.createRoot` for client rendering.
- **Why**: The new `createRoot` API enables concurrent rendering features introduced in React 18.
- **Migration**:
  - Replace `ReactDOM.render` with `ReactDOM.createRoot`.
  - Example:
    ```javascript
    // Before (React 17)
    import ReactDOM from 'react-dom';
    ReactDOM.render(<App />, document.getElementById('root'));

    // After (React 18)
    import { createRoot } from 'react-dom/client';
    const root = createRoot(document.getElementById('root'));
    root.render(<App />);
    ```

---

### **2. Deprecation of `ReactDOM.hydrate`**
- **Affected API**: `ReactDOM.hydrate`
- **What Changed**: The `ReactDOM.hydrate` method is replaced by `ReactDOM.hydrateRoot` for server-side rendering with hydration.
- **Why**: To support concurrent rendering and improve hydration performance.
- **Migration**:
  - Replace `ReactDOM.hydrate` with `ReactDOM.hydrateRoot`.
  - Example:
    ```javascript
    // Before (React 17)
    ReactDOM.hydrate(<App />, document.getElementById('root'));

    // After (React 18)
    import { hydrateRoot } from 'react-dom/client';
    hydrateRoot(document.getElementById('root'), <App />);
    ```

---

### **3. Automatic Batching of State Updates**
- **Affected Feature**: State updates outside React event handlers.
- **What Changed**: React now batches state updates automatically, even outside React event handlers (e.g., in `setTimeout` or Promises).
- **Why**: To reduce unnecessary re-renders and improve performance.
- **Migration**:
  - No action is required unless you rely on the old behavior. Use `flushSync` to disable batching if needed.
  - Example:
    ```javascript
    // Before (React 17)
    setTimeout(() => {
      setState1(value1);
      setState2(value2); // Causes two renders
    });

    // After (React 18)
    setTimeout(() => {
      setState1(value1);
      setState2(value2); // Causes one render
    });

    // To disable batching
    import { flushSync } from 'react-dom';
    setTimeout(() => {
      flushSync(() => setState1(value1));
      flushSync(() => setState2(value2)); // Causes two renders
    });
    ```

---

### **4. Stricter Hydration Errors**
- **Affected Feature**: Hydration mismatches.
- **What Changed**: Hydration mismatches are now treated as errors instead of warnings. React will revert to client rendering up to the nearest `<Suspense>` boundary.
- **Why**: To ensure consistency between server-rendered and client-rendered content.
- **Migration**:
  - Fix hydration mismatches in your application.
  - Use `<Suspense>` boundaries to isolate problematic areas.

---

### **5. New Strict Mode Behavior**
- **Affected Feature**: Development-only Strict Mode.
- **What Changed**: React 18's Strict Mode now double-invokes components' lifecycle methods and effects to help identify side effects.
- **Why**: To make applications more resilient to future updates.
- **Migration**:
  - Ensure components are idempotent and can handle multiple invocations of lifecycle methods.

---

### **6. Dropped Support for Internet Explorer**
- **Affected Browsers**: Internet Explorer.
- **What Changed**: React 18 no longer supports Internet Explorer.
- **Why**: React 18 relies on modern browser features like microtasks, which cannot be polyfilled in IE.
- **Migration**:
  - Use React 17 if IE support is required.
  - Alternatively, use polyfills or modernize your application.

---

### **7. New Server Rendering APIs**
- **Affected APIs**: `renderToString`, `renderToStaticMarkup`.
- **What Changed**: These APIs are now limited in functionality. New APIs like `renderToPipeableStream` and `renderToReadableStream` are introduced for streaming server rendering.
- **Why**: To support Suspense on the server and improve performance.
- **Migration**:
  - Use the new streaming APIs for server rendering.
  - Example:
    ```javascript
    import { renderToPipeableStream } from 'react-dom/server';
    const stream = renderToPipeableStream(<App />);
    ```

---

### **8. New Hooks**
- **Affected APIs**: `useTransition`, `useDeferredValue`, `useId`.
- **What Changed**: New hooks are introduced to support concurrent rendering and improve performance.
- **Why**: To provide better control over rendering priorities and deferred updates.
- **Migration**:
  - Use these hooks as needed in your application.
  - Example:
    ```javascript
    const [isPending, startTransition] = useTransition();
    startTransition(() => {
      setState(value);
    });
    ```

---

### **9. Event Delegation Changes**
- **Affected Feature**: Event delegation.
- **What Changed**: React now attaches event handlers to the root container instead of the `document`.
- **Why**: To improve compatibility with non-React code.
- **Migration**:
  - Test your application for any event-related issues and update as needed.

---

### **10. Deprecation of Legacy APIs**
- **Affected APIs**: `ReactTestUtils.SimulateNative`, `ReactDOM.flushSync` (with warnings).
- **What Changed**: These APIs are deprecated or modified.
- **Why**: To align with modern React practices.
- **Migration**:
  - Replace deprecated APIs with recommended alternatives.

---

## Conclusion
Upgrading from React 17 to React 18 involves adopting new APIs, handling stricter error checks, and leveraging concurrent rendering features. While the changes are significant, they are designed to improve performance and developer experience. By following the migration steps outlined above, you can ensure a smooth transition to React 18.