# Contributing to YouTube Video Downloader

Thank you for your interest in contributing to this project! This document provides guidelines for contributors.

## 🤝 How to Contribute

### Reporting Bugs

1. **Search existing issues** before creating a new one
2. **Use the bug report template** when creating new issues
3. **Provide detailed information** including:
   - Operating system and Python version
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Error messages (if any)

### Suggesting Features

1. **Check existing feature requests** first
2. **Use the feature request template**
3. **Provide clear description** of the proposed feature
4. **Explain the use case** and benefits

### Code Contributions

#### Setup Development Environment

1. **Fork the repository**
2. **Clone your fork locally**
   ```bash
   git clone https://github.com/yourusername/youtube-video-downloader.git
   cd youtube-video-downloader
   ```
3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

#### Making Changes

1. **Create a new branch** for your feature/bugfix
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** following the coding standards
3. **Test your changes** thoroughly
4. **Commit your changes** with descriptive messages
   ```bash
   git commit -m "Add feature: Description of your changes"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request**

#### Coding Standards

- **Follow PEP 8** for Python code style
- **Use meaningful variable and function names**
- **Add docstrings** to functions and classes
- **Write tests** for new features
- **Keep commits small and focused**

#### Pull Request Guidelines

1. **Fill out the PR template** completely
2. **Link related issues** in the description
3. **Ensure all tests pass**
4. **Request code reviews** from maintainers
5. **Respond to feedback** promptly

## 📋 Development Areas

### High Priority Areas

- **GUI Improvements**: Enhanced user interface
- **Error Handling**: Better error messages and recovery
- **Performance**: Faster video processing
- **Testing**: Unit tests and integration tests

### Feature Ideas

- **Batch URL validation** before processing
- **Preview mode** to see video details before download
- **Custom speed settings** (user-configurable speed increase)
- **Subtitle downloading** and processing
- **Audio-only extraction** option
- **Download history** and resume capability
- **Multiple language support**

### Bug Areas to Monitor

- **FFmpeg compatibility** across different systems
- **YouTube API changes** affecting video downloads
- **Memory usage** with large video files
- **Network timeout** handling

## 🏆 Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for their contributions
- **Special badges** for significant contributions

## 📞 Getting Help

- **Create an issue** for questions or problems
- **Check existing documentation** first
- **Join discussions** in issues and pull requests

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License as the project.

---

Thank you for contributing to YouTube Video Downloader! 🚀
