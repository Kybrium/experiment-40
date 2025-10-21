# ⚡ Experiment-40 Frontend

Welcome to the **frontend** of **Experiment-40** — a futuristic, 3D-powered web interface built with **Next.js**, **React 19**, and **Three.js**.  
This layer handles the client-side experience, visuals, and UI logic for the entire project.

---

## 🧩 Tech Stack

### ⚙️ Core

* **[Next.js 15](https://nextjs.org/)** – App Router + Server Components
* **[React 19](https://react.dev/)** – modern concurrent rendering
* **[React DOM 19](https://react.dev/reference/react-dom)** – concurrent UI rendering
* **[Three.js](https://threejs.org/)** – 3D graphics engine
* **[@react-three/fiber](https://docs.pmnd.rs/react-three-fiber)** – React renderer for Three.js
* **[@react-three/drei](https://github.com/pmndrs/drei)** – helpers, cameras, loaders
* **[@react-three/rapier](https://github.com/pmndrs/react-three-rapier)** – real-time 3D physics engine
* **[TailwindCSS 4](https://tailwindcss.com/)** – design system, theming, and utility styling

---

### 🧰 Tooling

* **[TypeScript 5](https://www.typescriptlang.org/)** – full static typing
* **[ESLint 9](https://eslint.org/)** – advanced linting

  * **eslint-config-next** – Next.js-specific linting rules
  * **eslint-plugin-testing-library** & **eslint-plugin-jest-dom** – testing best practices
  * **@eslint/eslintrc** – ESLint configuration helpers
* **[PostCSS](https://postcss.org/)** (via `@tailwindcss/postcss`) – CSS processing and optimization
* **[Node.js 20+](https://nodejs.org/)** – runtime environment

---

### 🧩 UI & Form Handling

* **[React Hook Form](https://react-hook-form.com/)** – performant, type-safe form validation and management
* **[@tanstack/react-query](https://tanstack.com/query/latest)** – server state management, caching, and async data synchronization
* **[React Icons](https://react-icons.github.io/react-icons/)** – unified icon library wrapper for Font Awesome, Material, and more

---

### 🧪 Testing

* **[Jest 30](https://jestjs.io/)** – unit and integration testing framework

  * **jest-environment-jsdom** – browser-like test environment
  * **ts-jest** – TypeScript support for Jest
* **[Testing Library](https://testing-library.com/docs/react-testing-library/intro/)** – React component testing utilities

  * **@testing-library/react** – component rendering & queries
  * **@testing-library/user-event** – simulate user interactions
  * **@testing-library/jest-dom** – custom matchers for DOM assertions

---