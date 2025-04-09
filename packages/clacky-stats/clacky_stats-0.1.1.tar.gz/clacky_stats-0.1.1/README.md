# Clacky Stats

A command-line tool for analyzing code contributions in Git repositories.

## Features

- Analyze code contributions by date range or Git tags
- Generate statistics for individual repositories or multiple repositories
- Track AI vs human code contributions
- Weekly and monthly reports
- Export results to YAML format

## Installation

You can install Clacky Stats directly from PyPI:

```bash
pip install clacky-stats
```

## Usage

### Basic Commands

1. Analyze current repository:
```bash
clacky-stats blame
```

2. Analyze with date range:
```bash
clacky-stats blame --start-date 2024-01-01 --end-date 2024-12-31
```

3. Weekly report (since last Friday):
```bash
clacky-stats week
```

4. Monthly report:
```bash
clacky-stats month
```

### Advanced Usage

1. Analyze between specific tags:
```bash
clacky-stats blame --start-tag v1.0.0 --end-tag v2.0.0
```

2. Export results to file:
```bash
clacky-stats blame --output stats.yaml
```

3. Analyze all versions since a tag:
```bash
clacky-stats blame --start-tag v1.0.0 --all-since
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.