# Quantum

**Quantum** is a command-line tool developed by QuantumDatalytica LLC for building, running, testing, and managing modular "Quantum Machines" in a distributed data analytics pipeline.

Note: quantum-core-engine is a private dependency and must be manually installed.
Please contact the QuantumDatalytica team or refer to internal docs for installation instructions.

---

## 🚀 Features

- 🧱 Initialize new Quantum Machines with starter templates
- 🧪 Test and lint your machine logic
- 🐳 Build Docker images for machine deployment
- ▶️ Run machines locally or in containers
- 🔎 Validate `project.json` and dependencies

---

## 📦 Installation

```bash
pip install quantum
```

---

## 📖 Usage

```bash
quantum --help
```

### Available Commands

| Command           | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `init machine`    | Initialize a new Quantum Machine project with boilerplate files             |
| `run machine`     | Run a machine and observe its behavior locally                              |
| `build machine`   | Build a Docker image for the specified machine                              |
| `test machine`    | Run unit tests defined for the machine                                      |
| `lint machine`    | Check the machine's code for linting/style issues                           |
| `validate machine`| Validate the machine's `project.json` and required structure                |

---

## 🧪 Example Commands

### 🔧 Initialize a machine

```bash
quantum init machine HelloWorld
```

Creates:
- `HelloWorld/main.py`
- `HelloWorld/project.json`
- `HelloWorld/requirements.txt`
- `HelloWorld/Dockerfile`

---

### ▶️ Run the machine

```bash
quantum run machine HelloWorld
```

---

### 🐳 Build the machine as Docker Image

```bash
quantum build machine HelloWorld
```

Builds a Docker image with dependencies for the machine.

---

### 🧪 Test your machine

```bash
quantum test machine HelloWorld
```

Runs the test suite defined under the machine's directory.

---

### 🎯 Lint your machine

```bash
quantum lint machine HelloWorld
```

Applies flake8 or equivalent linting tools to maintain code standards.

---

### 🛡 Validate machine structure

```bash
quantum validate machine HelloWorld\<file_name>
```

Ensures the machine has the correct `project.json`, required fields, and structure.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🧠 About QuantumDatalytica LLC

QuantumDatalytica is a data automation platform that enables developers to create, test, and publish modular analytics logic ("Quantum Machines") for enterprise data pipelines.
