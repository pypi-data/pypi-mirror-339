# Kotlin creator Tool

A command-line interface tool for Kotlin project management, providing templates for Clean Architecture and Flow-based projects.

## Installation

You can install the package using pip:

```bash
pip install kotlin-creator
```

Or with uv:

```bash
uv pip install kotlin-creator
```

## Usage

After installation, you can use the CLI tool with the following commands:

### Create a New Project

To create a new Kotlin Clean Architecture project:

```bash
kotlin create kotlin <project_name>
```

To create a new Kotlin Flow-based project:

```bash
kotlin create flow <project_name>
```

Replace `<project_name>` with the desired name for your project. This command will generate a project structure that includes:

- **Root Files**: Gradle configuration files including build scripts
- **App Structure**: Standard Android application structure with src, res, and test directories
- **Architecture Components**: Clean architecture layers organized into data, domain, and UI packages

### Check Version

To display the version of the Kotlin CLI tool:

```bash
kotlin version
```

## Project Structures

### Clean Architecture

The Clean Architecture project includes:

- **Data Layer**: Local and remote data sources, repositories
- **Domain Layer**: Use cases and business models
- **UI Layer**: Activities, fragments, adapters

### Flow-based Architecture

The Flow-based project extends the Clean Architecture with:

- **Kotlin Flow Components**: Data flow providers and flow-based use cases
- **State Management**: UI state handling with Loading/Success/Error patterns
- **Coroutines Integration**: Advanced asynchronous programming with Coroutines

## Features

- Create new Kotlin projects with a single command
- Choose between different architectural templates
- Ready-to-use project structure following best practices
- Gradle configuration with common Android dependencies
- Extensible architecture for modern Android development

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.