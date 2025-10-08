#!/bin/bash
# Production-ready safety hook with configurable rules

input_json=$(cat)
tool_name=$(echo "$input_json" | jq -r '.tool_name // ""')

# Load safety configuration if it exists
SAFETY_CONFIG=".claude/safety-rules.json"
if [[ -f "$SAFETY_CONFIG" ]]; then
    # Custom safety rules per project
    blocked_commands=$(jq -r '.blocked_commands[]? // empty' "$SAFETY_CONFIG" 2>/dev/null)
    sensitive_files=$(jq -r '.sensitive_files[]? // empty' "$SAFETY_CONFIG" 2>/dev/null)
else
    # Default safety rules
    blocked_commands=("rm -rf" "git reset --hard" "sudo rm" "dd if=" "mkfs" "fdisk")
    sensitive_files=(".env" ".env.*" "*.key" "*.pem" "id_rsa" "id_ed25519")
fi

case "$tool_name" in
    "Bash")
        command=$(echo "$input_json" | jq -r '.tool_input.command // ""')

        # Check against blocked commands
        for pattern in "${blocked_commands[@]}"; do
            if [[ "$command" == *"$pattern"* ]]; then
                echo "🚫 BLOCKED: Dangerous command pattern detected: $pattern"
                echo "Command: $command"
                echo "Run manually if you're certain this is safe."
                exit 2
            fi
        done

        # Special checks for file operations
        if [[ "$command" == *"chmod 777"* ]] || [[ "$command" == *"chmod -R 777"* ]]; then
            echo "🚫 BLOCKED: Overly permissive chmod detected"
            exit 2
        fi
        ;;

    "Write"|"Edit"|"MultiEdit")
        file_path=$(echo "$input_json" | jq -r '.tool_input.file_path // ""')

        # Check against sensitive files
        for pattern in "${sensitive_files[@]}"; do
            if [[ "$file_path" == $pattern ]] || [[ "$(basename "$file_path")" == $pattern ]]; then
                echo "🔒 BLOCKED: Attempting to modify sensitive file: $file_path"
                echo "Pattern matched: $pattern"
                echo "Please handle sensitive files manually."
                exit 2
            fi
        done

        # Block operations outside project directory
        project_dir=$(pwd)
        if [[ "$file_path" == /* ]] && [[ ! "$file_path" == "$project_dir"* ]]; then
            echo "🚫 BLOCKED: Attempting to write outside project directory"
            echo "File: $file_path"
            echo "Project: $project_dir"
            exit 2
        fi
        ;;
esac

echo "✅ Safety check passed for: $tool_name"
exit 0