# Git — Advanced Operations Reference

## Conflict Resolution

### When Conflicts Occur

1. **Identify conflicted files**:
   ```bash
   git status
   ```

2. **Open conflicted files** and look for conflict markers:
   ```
   <<<<<<< HEAD
   Your changes
   =======
   Incoming changes
   >>>>>>> branch-name
   ```

3. **Resolve conflicts** by editing the file

4. **Stage resolved files**:
   ```bash
   git add resolved-file.py
   ```

5. **Complete the merge/rebase**:
   ```bash
   git commit              # For merge
   git rebase --continue   # For rebase
   ```


## Undoing Changes

### Discard Local Changes

```bash
# Discard changes in specific file
git checkout -- file.py

# Discard all local changes
git reset --hard HEAD

# Discard untracked files
git clean -fd
```

### Unstage Files

```bash
# Unstage specific file
git reset HEAD file.py

# Unstage all files
git reset HEAD
```

### Revert Commits

```bash
# Revert last commit (creates new commit)
git revert HEAD

# Revert specific commit
git revert <commit-hash>

# Reset to previous commit (destructive)
git reset --hard HEAD~1

# Reset but keep changes staged
git reset --soft HEAD~1
```


## .gitignore Configuration

### Common Patterns

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
*.log

# Dependencies
node_modules/
package-lock.json

# Build outputs
dist/
build/
*.min.js
*.min.css
```

### Apply .gitignore to Existing Files

```bash
# Remove cached files
git rm -r --cached .

# Re-add all files
git add .

# Commit
git commit -m "chore: apply .gitignore rules"
```


## Common Issues and Solutions

### Issue: Not a Git Repository

```bash
# Error: fatal: not a git repository
# Solution: Initialize repository
git init
```

### Issue: Remote Already Exists

```bash
# Error: remote origin already exists
# Solution: Remove and re-add
git remote remove origin
git remote add origin <new-url>
```

### Issue: Diverged Branches

```bash
# Error: Your branch and 'origin/main' have diverged
# Solution 1: Merge
git pull origin main

# Solution 2: Rebase
git pull --rebase origin main
```

### Issue: Detached HEAD

```bash
# Solution: Create branch from current state
git checkout -b recovery-branch

# Or return to main branch
git checkout main
```

### Issue: Large Files

```bash
# Error: file too large
# Solution: Use Git LFS
git lfs install
git lfs track "*.psd"
git add .gitattributes
```


## Git Workflows

### Feature Branch Workflow

1. Create feature branch from main
2. Make changes and commit
3. Push feature branch
4. Create pull request
5. Review and merge
6. Delete feature branch

```bash
git checkout main
git pull origin main
git checkout -b feature/new-feature
# ... make changes ...
git add .
git commit -m "feat: implement new feature"
git push -u origin feature/new-feature
```

### Gitflow Workflow

Branches:

- **main**: Production-ready code
- **develop**: Integration branch
- **feature/\***: New features
- **release/\***: Release preparation
- **hotfix/\***: Emergency fixes

### Trunk-Based Development

- Single main branch
- Short-lived feature branches
- Frequent integration
- Feature flags for incomplete features


## Inspection and History

### View History

```bash
# View commit history
git log

# Compact view
git log --oneline

# Graph view
git log --graph --oneline --all

# View changes in commit
git show <commit-hash>

# View file history
git log --follow file.py
```

### Compare Changes

```bash
# Compare working directory with staging
git diff

# Compare staging with last commit
git diff --staged

# Compare branches
git diff main..feature-branch

# Compare specific files
git diff main feature-branch -- file.py
```

### Search History

```bash
# Search commits by message
git log --grep="bug fix"

# Search commits by author
git log --author="John"

# Search commits by content
git log -S "function_name"
```


## Stashing Changes

```bash
# Stash current changes
git stash

# Stash with message
git stash save "work in progress"

# List stashes
git stash list

# Apply latest stash
git stash apply

# Apply and remove stash
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Drop stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

