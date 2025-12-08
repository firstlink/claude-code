# API Review and Commit Workflow

You are tasked with orchestrating a complete API review and git commit workflow.

## Workflow Steps:

### Step 1: Launch API Reviewer Agent
- Use the Task tool with the following parameters:
  - `subagent_type`: "api-reviewer"
  - `description`: "Review expense tracker API"
  - `prompt`: "Review all API endpoints, request/response schemas, and API documentation in the expense-tracker application. Analyse for best practices, security vulnerabilities, usability issues, and design patterns. Provide specific, actionable recommendations for improvements with code examples where applicable."

### Step 2: Process and Present Findings
- Wait for the api-reviewer agent to complete
- Analyse the findings and categorise them:
  - Critical security issues
  - Design/architecture concerns
  - Best practice violations
  - Usability improvements
- Present a clear summary to the user with:
  - Number of issues found by category
  - Specific file locations affected
  - Priority recommendations

### Step 3: User Confirmation
- Ask the user if they want to proceed with the git commit workflow
- If critical issues are found, recommend addressing them first
- Wait for user approval before proceeding

### Step 4: Execute Git Commit
- Once approved, use the SlashCommand tool to execute: `/expense-tracker-git-commit`
- Allow the git commit workflow to complete
- Confirm final status to the user

## Important Guidelines:
- Always wait for each step to fully complete before proceeding
- Never skip the user confirmation step
- If the api-reviewer agent fails, do not proceed to git commit
- Provide clear, actionable feedback at each stage
