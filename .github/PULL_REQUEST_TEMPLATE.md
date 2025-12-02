<!-- PR template for workspace-system -->

## Summary
Provide a short description of the change and why it is needed.

## Type of change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Performance
- [ ] Chore

## Checklist
- [ ] I have run the test suite locally: `python3 run_tests.py`
- [ ] I have run `./ws check` and addressed findings
- [ ] I added/updated tests where applicable
- [ ] I updated documentation where applicable (`README.md`, `.github/*`, `docs/`)
- [ ] I ran linter/formatters where applicable (ruff/black)

## Related issues
Link any related issues or discussions: e.g. `#12` or `https://github.com/.../discussions/5`

## Breaking changes
Describe any breaking changes and migration notes (if none, write "None").

## Implementation notes / Testing steps
Provide instructions to test the change locally (commands, expected outputs):

```bash
# Typical checks for PRs
python3 run_tests.py
./ws check
# Optional: run specific scripts or commands
```

## Reviewer notes
Anything the reviewer should pay special attention to (performance, prevention rules, compatibility)

**Quality gate reminder**: If changes affect prevention or quality systems, ensure prevention checks remain lightweight (< 5ms) and include `quality_gate` expectations in the PR description.
