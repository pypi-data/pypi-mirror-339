# py-commiter

> A command-line tool to generate commit messages following the Conventional Commits standard, with support for types, scopes, and Gitmoji emojis.

---

## 🌟 Features

- Interactive selection of commit types (`feat`, `fix`, `docs`, etc.)
- Support for **custom scopes**
- Inclusion of **Gitmoji emojis**
- **Multiline input** with advanced editing (prompt-toolkit)
- Message rendering inside an ASCII box
- Git integration: checks git status, allows `git add .`, and performs final commit

---

## ⚙️ Installation

```bash
pip install py-commiter
```


## ⚡ Quick usage

```bash
py-commiter
```

Follow the step-by-step prompts to build your commit message.

---

## 🎨 Example commit message

```text
✨ feat(auth): add login endpoint

Added support for JWT authentication and login error handling.
```

---

## ✏️ License

MIT License. Made with ❤️ by Matias Tillerias Ley.


