---
description: Complete feature development workflow from planning to testing
argument-hint: [feature-name] [--plan|--implement|--test|--complete]
allowed-tools: Bash(git:*), Bash(python:*), Bash(pytest:*), Bash(ls:*), Bash(grep:*), Bash(find:*)
---

# Feature Development Workflow

Complete workflow for developing new features including planning, implementation, testing, and integration.

## Usage Examples

**Start new feature development:**
```
/feature-dev user-authentication
/feature-dev expense-categories --plan
```

**Implement planned feature:**
```
/feature-dev user-authentication --implement
```

**Run feature tests:**
```
/feature-dev user-authentication --test
```

**Complete feature (implement + test + integrate):**
```
/feature-dev user-authentication --complete
```

**Help:**
```
/feature-dev --help
```

## Implementation

If $ARGUMENTS contains "help" or "--help":
Display this usage information and exit.

Extract feature name from $ARGUMENTS (first non-flag argument).
Parse operation flags: --plan, --implement, --test, --complete

If no feature name provided:
```
Error: Feature name required
Usage: /feature-dev <feature-name> [--plan|--implement|--test|--complete]
```

## 1. Feature Planning Phase

If "--plan" flag or no operation flag:

### Analyse Existing Codebase
!find . -name "*.py" -type f | grep -E "(model|view|controller|service)" | head -10
!ls -la | grep -E "^d"

### Check Project Structure
!find . -name "requirements.txt" -o -name "pyproject.toml" -o -name "setup.py"
!test -f "tests/" && echo "Tests directory exists" || echo "No tests directory"

### Feature Planning Template
Create feature planning documentation:

```
FEATURE: {feature_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━

## Requirements Analysis
- [ ] Define user stories
- [ ] Identify affected components
- [ ] Document API changes
- [ ] Plan database schema changes

## Technical Design
- [ ] Architecture overview
- [ ] Component interactions
- [ ] Data flow design
- [ ] Error handling strategy

## Implementation Plan
- [ ] Core functionality
- [ ] Database models (if needed)
- [ ] API endpoints (if needed)
- [ ] Frontend components (if needed)
- [ ] Error handling
- [ ] Input validation

## Testing Strategy
- [ ] Unit tests
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Performance tests

## Files to Create/Modify
Based on codebase analysis:
[List specific files that need changes]

## Dependencies
Check if new dependencies needed:
[List any new packages required]

## Acceptance Criteria
- [ ] Feature works as specified
- [ ] All tests pass
- [ ] Code follows project conventions
- [ ] Documentation updated
```

## 2. Implementation Phase

If "--implement" flag:

### Create Feature Branch
!git checkout -b feature/{feature_name} 2>/dev/null || git checkout feature/{feature_name}

### Analyse Implementation Needs
Check existing similar features:
!grep -r "class.*Model" . --include="*.py" | head -5
!grep -r "@app.route\|@router" . --include="*.py" | head -5

### Implementation Checklist
```
IMPLEMENTING: {feature_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Core Implementation
- [ ] Create/modify models
- [ ] Implement business logic
- [ ] Add API endpoints
- [ ] Create database migrations
- [ ] Add input validation
- [ ] Implement error handling

## Code Quality
- [ ] Follow PEP 8 standards
- [ ] Add type hints
- [ ] Write docstrings
- [ ] Handle edge cases
- [ ] Add logging where appropriate

## Integration
- [ ] Update configuration
- [ ] Modify existing workflows
- [ ] Update dependencies if needed
```

### Check Code Standards
!python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics 2>/dev/null || echo "flake8 not available"
!python -m black --check . 2>/dev/null || echo "black not available"

## 3. Testing Phase

If "--test" flag:

### Run Existing Tests
!python -m pytest -v 2>/dev/null || echo "pytest not available - checking for other test runners"
!python -m unittest discover -v 2>/dev/null || echo "unittest discover failed"

### Test Implementation Checklist
```
TESTING: {feature_name}
━━━━━━━━━━━━━━━━━━━━━━━━━

## Unit Tests
- [ ] Test core functionality
- [ ] Test edge cases
- [ ] Test error conditions
- [ ] Test input validation

## Integration Tests
- [ ] Test API endpoints
- [ ] Test database operations
- [ ] Test component interactions

## Manual Testing
- [ ] Test user workflows
- [ ] Test error scenarios
- [ ] Test performance
- [ ] Test security aspects

## Test Coverage
Check test coverage for new code
```

### Generate Test Report
!python -m pytest --cov=. --cov-report=term-missing 2>/dev/null || echo "Coverage tools not available"

## 4. Complete Feature Development

If "--complete" flag or no specific flag:

Execute full workflow:

### Phase 1: Planning
Run planning phase (as above)

### Phase 2: Implementation
Run implementation phase (as above)

### Phase 3: Testing
Run testing phase (as above)

### Phase 4: Integration & Cleanup
```
FEATURE COMPLETION: {feature_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Final Checks
- [ ] All tests pass
- [ ] Code review complete
- [ ] Documentation updated
- [ ] Migration scripts tested
- [ ] Performance acceptable

## Integration
- [ ] Merge feature branch
- [ ] Update main documentation
- [ ] Deploy to staging
- [ ] Update changelog

## Post-Implementation
- [ ] Monitor for issues
- [ ] Gather user feedback
- [ ] Plan follow-up improvements
```

### Git Operations
!git status
!git add .
!git status

Suggest commit message:
```
Suggested commit message:
feat: implement {feature_name}

- Add core functionality for {feature_name}
- Include comprehensive tests
- Update documentation
- Follow project conventions
```

## 5. Feature Status Summary

Always show current feature development status:

```
FEATURE DEVELOPMENT STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: {feature_name}
Current Branch: {current_branch}
Files Modified: {modified_count}
Tests Status: {test_status}
Code Quality: {quality_status}

NEXT STEPS
─────────
{specific_next_actions_based_on_current_state}

QUICK COMMANDS
─────────────
/feature-dev {feature_name} --plan      - Plan feature development
/feature-dev {feature_name} --implement - Implement feature
/feature-dev {feature_name} --test      - Test feature
/feature-dev {feature_name} --complete  - Complete full workflow
```

Think step by step about feature development needs and provide specific guidance based on the current project structure and feature requirements.