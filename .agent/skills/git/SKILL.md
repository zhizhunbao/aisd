---
name: git
description: Git 版本控制操作与最佳实践。Use when (1) 初始化或配置 Git 仓库, (2) 执行 commit/push/pull 等操作, (3) 处理分支和合并冲突, (4) 配置 .gitignore, (5) 解决 Git 相关问题
---

# Git Version Control

## Objectives

- Initialize and configure Git repositories
- Execute common Git operations (commit, push, pull, branch, merge)
- Handle merge conflicts and resolve issues
- Configure .gitignore and Git workflows
- Follow Git best practices and conventions

## Initial Setup

### Check Git Status

Before any Git operation, check the current state:

```bash
git status                    # Check working directory status
git remote -v                 # List remote repositories
git branch -a                 # List all branches
git log --oneline -10         # View recent commits
```

### Initialize Repository

```bash
# Initialize new repository
git init

# Add remote origin
git remote add origin <repository-url>

# Verify remote
git remote -v
```

### Clone Existing Repository

```bash
# Clone with HTTPS
git clone https://github.com/user/repo.git

# Clone with SSH
git clone git@github.com:user/repo.git

# Clone specific branch
git clone -b branch-name https://github.com/user/repo.git
```

## Configuration

### User Identity

```bash
# Global configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Repository-specific configuration
git config user.name "Your Name"
git config user.email "your.email@example.com"

# View configuration
git config --list
```

### Common Settings

```bash
# Default branch name
git config --global init.defaultBranch main

# Line ending handling
git config --global core.autocrlf true    # Windows
git config --global core.autocrlf input   # Mac/Linux

# Editor
git config --global core.editor "code --wait"

# Credential caching
git config --global credential.helper cache
```

## Basic Workflow

### 1. Check Status

```bash
git status
```

### 2. Stage Changes

```bash
# Stage specific files
git add file1.py file2.py

# Stage all changes
git add .

# Stage by pattern
git add *.py

# Interactive staging
git add -p
```

### 3. Commit Changes

```bash
# Commit with message
git commit -m "feat: add user authentication"

# Commit with detailed message
git commit -m "feat: add user authentication" -m "- Implement JWT token generation
- Add login/logout endpoints
- Create user session management"

# Amend last commit
git commit --amend -m "Updated message"

# Stage and commit in one step
git commit -am "fix: resolve login bug"
```

### 4. Push Changes

```bash
# Push to remote
git push origin main

# Push new branch
git push -u origin feature-branch

# Force push (use with caution)
git push --force-with-lease origin main
```

### 5. Pull Changes

```bash
# Pull from remote
git pull origin main

# Pull with rebase
git pull --rebase origin main

# Fetch without merging
git fetch origin
```

## Branch Management

### Create and Switch Branches

```bash
# Create new branch
git branch feature-name

# Switch to branch
git checkout feature-name

# Create and switch in one command
git checkout -b feature-name

# Modern syntax (Git 2.23+)
git switch feature-name
git switch -c feature-name
```

### List and Delete Branches

```bash
# List local branches
git branch

# List all branches (including remote)
git branch -a

# Delete local branch
git branch -d feature-name

# Force delete
git branch -D feature-name

# Delete remote branch
git push origin --delete feature-name
```

### Merge Branches

```bash
# Merge feature into current branch
git merge feature-name

# Merge with no fast-forward
git merge --no-ff feature-name

# Abort merge
git merge --abort
```

### Rebase

```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase (last 3 commits)
git rebase -i HEAD~3

# Continue after resolving conflicts
git rebase --continue

# Abort rebase
git rebase --abort
```

## Commit Message Conventions

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks (dependencies, config)
- **perf**: Performance improvements

### Examples

```bash
git commit -m "feat(auth): add JWT authentication"
git commit -m "fix(api): resolve null pointer in user endpoint"
git commit -m "docs: update installation instructions"
git commit -m "refactor(utils): simplify date formatting logic"
```

<!-- Detailed content moved to references/git_advanced.md -->

> 📖 See [references/git_advanced.md](references/git_advanced.md) for detailed content on the following topics:
> - ## Conflict Resolution
> - ## Undoing Changes
> - ## .gitignore Configuration
> - ## Common Issues
> - ## Git Workflows
> - ## Inspection and History
> - ## Stashing Changes

## Validation Checklist

Before pushing:

- [ ] Check `git status` for untracked or modified files
- [ ] Review changes with `git diff`
- [ ] Ensure commit messages follow conventions
- [ ] Verify correct branch with `git branch`
- [ ] Pull latest changes if working with others
- [ ] Run tests if applicable
- [ ] Check .gitignore excludes sensitive files

## Best Practices

1. **Commit often**: Small, focused commits are easier to review and revert
2. **Write clear messages**: Follow commit message conventions
3. **Pull before push**: Avoid conflicts by staying up-to-date
4. **Use branches**: Keep main branch stable
5. **Review before commit**: Use `git diff` to verify changes
6. **Don't commit secrets**: Use .gitignore and environment variables
7. **Keep history clean**: Use rebase for local branches, merge for shared branches
8. **Tag releases**: Use `git tag v1.0.0` for version markers

## Quick Reference

```bash
# Status and info
git status                    # Check status
git log --oneline -10         # Recent commits
git diff                      # View changes

# Basic operations
git add .                     # Stage all
git commit -m "message"       # Commit
git push origin main          # Push
git pull origin main          # Pull

# Branching
git checkout -b feature       # Create branch
git merge feature             # Merge branch
git branch -d feature         # Delete branch

# Undo
git reset HEAD file           # Unstage
git checkout -- file          # Discard changes
git revert HEAD               # Revert commit

# Remote
git remote -v                 # List remotes
git fetch origin              # Fetch updates
git push -u origin branch     # Push new branch
```
