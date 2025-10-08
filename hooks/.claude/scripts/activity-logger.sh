#!/bin/bash
# Activity logging hook - tracks all Claude Code operations

# Read JSON input
input_json=$(cat)

# Extract relevant information
tool_name=$(echo "$input_json" | jq -r '.tool_name // "unknown"')
file_path=$(echo "$input_json" | jq -r '.tool_input.file_path // "no-file"')
project_dir=$(echo "$input_json" | jq -r '.cwd // "unknown"')
timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# Log to daily file
log_file="$HOME/.claude/logs/$(date '+%Y-%m-%d').log"
echo "[$timestamp] TOOL: $tool_name | FILE: $file_path | PROJECT: $project_dir" >> "$log_file"

# Provide user feedback
echo "📝 Logged: $tool_name operation"

exit 0