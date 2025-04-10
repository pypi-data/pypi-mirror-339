# 🛠️ PyRTK - Python REST Toolkit CLI

PyRTK is a modern CLI tool to scaffold and manage clean, modular FastAPI projects and microservices — with style 😎

---

## 🚀 Installation (Recommended via pipx)

Make sure you have [pipx](https://pypa.github.io/pipx/) installed:

```bash
brew install pipx && pipx ensurepath
# or
python3 -m pip install --user pipx && python3 -m pipx ensurepath
```

Then install PyRTK globally:

```bash
pipx install dist/pyrtk-0.1.0-py3-none-any.whl
```

Now you can use the `pyrtk` command from anywhere 🎉

---

## 📦 Commands

### `pyrtk create <project-name> --type api|ms`

Scaffolds a complete API or Microservice:

- `api`: simple FastAPI project with routers, schemas, middleware, and main.py
- `ms`: full microservice architecture (core, models, services, routers, etc.)

Example:

```bash
pyrtk create panaderia --type ms
```

✅ This will also:
- Create a virtual environment inside the project
- Install dependencies
- Show you how to activate the environment manually

---

### `pyrtk run`

Runs your FastAPI project automatically using the environment created.

```bash
cd panaderia
pyrtk run
```

This will launch the Uvicorn server using the right Python environment automatically 🚀

---

## 🔜 Coming Soon

- `pyrtk generate <type> <name>` → Auto-generate routers, schemas, models, etc.
- Plugin system
- Custom project templates
- Docker & deployment helpers

---

## 🧡 Made with love by Andrés Mardones
