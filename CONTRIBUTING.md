# Contributing to TaskFlowAPI

Thank you for your interest in contributing to TaskFlowAPI! We appreciate all contributions, whether they're bug fixes, feature additions, documentation improvements, or suggestions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

Please be respectful and considerate of others in all interactions. We are committed to providing a welcoming and inclusive environment for all contributors.

## How to Contribute

### 1. Fork the Repository

Click the "Fork" button on the GitHub repository page to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/TaskFlowAPI.git
cd TaskFlowAPI
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/add-user-authentication`
- `bugfix/fix-migration-issue`
- `docs/update-readme`
- `refactor/improve-database-layer`

### 4. Setup Development Environment

```bash
# Using make (recommended)
make venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

make install
```

Or manually:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
docker-compose up -d
alembic upgrade head
```

## Development Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start PostgreSQL

```bash
docker-compose up -d
```

### Run Migrations

```bash
alembic upgrade head
```

### Start Development Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Making Changes

### Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards.

#### Format Code

```bash
# Using make
make format

# Or manually
black app/ --line-length 127
isort app/
```

#### Check Linting

```bash
# Using make
make lint

# Or manually
flake8 app/
pylint app/
```

### Database Changes

When modifying models:

1. Update your model file in `app/model/`
2. Create a migration:
   ```bash
   make migration
   # Or: alembic revision --autogenerate -m "description"
   ```
3. Review the generated migration file
4. Test the migration:
   ```bash
   alembic upgrade head
   ```
5. Commit both model and migration files

### Testing

Add tests for new functionality in the `tests/` directory:

```bash
# Run tests
make test

# Or manually
pytest --cov=app tests/ -v
```

## Commit Guidelines

Follow the Conventional Commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (no functional changes)
- `refactor`: Code refactoring without changing functionality
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependency updates
- `ci`: CI/CD related changes

### Examples

```
feat(auth): add JWT token refresh endpoint

- Implement refresh token functionality
- Update authentication middleware
- Add request/response schemas

Closes #123
```

```
fix(database): resolve async connection pool issue

Previously, the connection pool would exhaust connections
under high load. This commit fixes the issue by properly
managing connection lifecycle.

Fixes #456
```

### Scope

The scope should specify what part of the codebase is affected:
- `auth` - Authentication related
- `database` - Database models and migrations
- `api` - API endpoints
- `schema` - Pydantic schemas
- `config` - Configuration
- `docs` - Documentation

### Subject

- Use imperative mood ("add" not "adds" or "added")
- Don't capitalize first letter
- Don't end with a period
- Limit to 50 characters

### Body

- Wrap at 72 characters
- Explain what and why, not how
- Separate from subject with a blank line
- Each paragraph separated by a blank line

### Footer

- Reference issues: `Closes #123`
- Breaking changes: `BREAKING CHANGE: description`

## Pull Request Process

### Before Submitting

1. **Update your branch**: Sync with the latest main branch
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Run tests and linting**:
   ```bash
   make test
   make lint
   ```

3. **Format your code**:
   ```bash
   make format
   ```

4. **Run migrations** (if applicable):
   ```bash
   alembic upgrade head
   alembic downgrade base
   alembic upgrade head
   ```

### Submitting a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Go to the original repository on GitHub

3. Click "New Pull Request"

4. Select your branch and provide a clear description:
   ```
   ## Description
   Brief description of what this PR does

   ## Related Issues
   Closes #123

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Breaking change

   ## Changes Made
   - Change 1
   - Change 2

   ## Testing
   Describe how you tested the changes

   ## Screenshots (if applicable)
   Add screenshots for UI changes
   ```

5. Wait for review and address feedback

### PR Review Guidelines

- All tests must pass
- Code must be formatted (black, isort)
- No linting warnings (flake8, pylint)
- Documentation should be updated
- Commit history should be clean
- No merge conflicts

## Reporting Issues

### Bug Reports

Provide:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Error messages and stack traces
- Relevant code snippets

### Feature Requests

Include:
- Clear description of the feature
- Use case and motivation
- Possible implementation approach
- Examples if applicable

### Example Issue

```
## Title
[BUG] Database migration fails on PostgreSQL 12

## Description
When running `alembic upgrade head`, the migration fails with...

## Steps to Reproduce
1. Set up with PostgreSQL 12
2. Run `alembic upgrade head`
3. See error...

## Expected Behavior
Migrations should run successfully

## Actual Behavior
Error message: ...

## Environment
- Python 3.11
- PostgreSQL 12
- FastAPI 0.104.1

## Stack Trace
...
```

## Questions?

- Check existing [Issues](../../issues) and [Discussions](../../discussions)
- Create a new discussion for questions
- Ask in the issue tracker if unsure

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to TaskFlowAPI! 🚀
