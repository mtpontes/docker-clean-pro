# Docker Clean Pro

**Professional Docker Cleanup & Disk Management Tool**

Docker Clean Pro is a high-performance CLI tool designed to keep your Docker environment lean and fast. Migrated from a robust PowerShell foundation to Python, it offers cross-platform stability and advanced resource analysis that goes far beyond standard `docker prune` commands.

## Key Features

- **Multi-Level Cleanup**: Three levels of cleaning (Basic, Advanced, Total) to fit your specific needs.
- **Smart Filtering**: Remove resources based on age (e.g., older than 10 days, 2 weeks) using `--older-than`.
- **Dry-Run Mode**: Safely preview exactly what will be deleted before taking any action.
- **Deep Disk Analysis**: Generates comprehensive reports comparing Docker resource usage with your total system disk space.
- **Professional Reporting**: Export your cleanup results and disk usage to **JSON** or **Markdown** for audit and automation.
- **Rich Terminal UI**: Beautifully formatted tables and progress indicators powered by `rich`.

---

## Installation

### Via PyPI (Recommended)
```bash
pip install docker-clean-pro
```

### From Source
Requires [Hatch](https://hatch.pypa.io/):
```bash
git clone https://github.com/mtpontes/docker-clean-pro.git
cd docker-clean-pro
hatch run docker-clean --help
```

---

## Quick Start

### 1. Check your current situation
Get a detailed report of how much space Docker is consuming:
```bash
docker-clean dr
```

### 2. Safely preview a basic cleanup
See what unused containers, networks, and dangling images would be removed:
```bash
docker-clean bc --dry-run
```

### 3. Run a deep cleanup
Clean basic resources plus volumes, unused images, and build cache:
```bash
docker-clean ac
```

---

## Command Reference

| Command | Alias | Description | Key Options |
|---------|-------|-------------|-------------|
| `bc` | `basic_cleanup` | Removes dangling images, stopped containers, and unused networks. | `--older-than`, `--dry-run` |
| `ac` | `advanced_cleanup` | Everything in Basic + all unused images, volumes, and build cache. | `--older-than`, `--dry-run` |
| `tc` | `total_cleanup` | **NUCLEAR OPTION**: Removes absolutely everything not currently in use. | `--older-than`, `--dry-run`, `-y` |
| `dr` | `disk_report` | Detailed usage report and system disk relation. | `--json`, `--md`, `--no-terminal` |

---

## Professional Reporting

Docker Clean Pro can generate artifacts for your CI/CD pipelines or monitoring systems:

```bash
# Generate a Markdown report for a GitHub Action summary
docker-clean dr --md report.md

# Generate a JSON report for external monitoring
docker-clean dr --json usage.json --no-terminal
```

## Contributing

This project uses **Hatch** for environment management and **Pytest** for testing.

1. **Install Development Environment**:
   ```bash
   hatch shell
   ```
2. **Run Tests**:
   ```bash
   hatch run test
   ```

---

## Support the Project

If this tool helped you reclaim precious disk space, consider leaving a **star** on GitHub!

<p align="center">
  Built with 🐍 by <a href="https://github.com/mtpontes">mtpontes</a>
</p>
