# Session 5 — Git and GitHub

## Student Details

- **Name:** Shifa
- **Enrollment Number:** 24BCS10354
- **Email:** shifa.24bcs10354@sst.scaler.com

---

## Homework Tasks

| Task | Description |
|---|---|
| 1 | `git commit -a -m` vs `git commit -m` |
| 2 | Git Cherry-Pick |

---

## Task 1: `git commit -a -m`

Practiced both `git commit -m` and `git commit -a -m` and observed the difference between them.

### Difference

| Command | Behavior |
|---|---|
| `git commit -m "message"` | Commits only files already staged with `git add` |
| `git commit -a -m "message"` | Automatically stages **modified/deleted tracked files** and commits — no `git add` needed |

> **Note:** `git commit -a -m` does **not** include newly created untracked files. New files must still be added using `git add` first.

### Commands

```bash
# Standard commit (requires git add first)
git add file.txt
git commit -m "Add file"

# Commit with auto-staging of modified tracked files
git commit -a -m "Update file"
```

### Screenshot

![Git commit](github.png)

---

## Task 2: Git Cherry-Pick

Created multiple commits in the `main` branch, then created a separate branch with additional commits. Used `git cherry-pick` to apply a specific commit from the new branch into `main`.

### What I understood

`git cherry-pick` applies a specific commit from one branch to another without merging the entire branch. It is useful when you want to bring in a single fix or feature from another branch.

### Commands

```bash
# Step 1: Create commits in main
git commit -m "Commit 1"
git commit -m "Commit 2"
git commit -m "Commit 3"

# Step 2: View commit log
git log --oneline

# Step 3: Create new branch and make commits
git checkout -b new-branch
git commit -m "Feature A"
git commit -m "Feature B"
git commit -m "Feature C"

# Step 4: View log to find specific commit hash
git log --oneline

# Step 5: Switch back to main and cherry-pick
git checkout main
git cherry-pick <commit-hash>

# Step 6: Verify the commit is now in main
git log --oneline
```

### Screenshots

![Git commit -a](github2.png)

![Cherry-pick commit history](github3.png)

![Cherry-pick result](github4.png)

---

## Conclusion

Through this task, I learned:
- The difference between `git commit -m` and `git commit -a -m`
- How to use `git cherry-pick` to apply a specific commit from one branch to another

---

## Resources

- [Git Documentation](https://git-scm.com/docs)
- Session 5 Git and GitHub Notes
