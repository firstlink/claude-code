#!/bin/bash
# Lint with ESLint

input_json=$(cat)
file_path=$(echo "$input_json" | jq -r '.tool_input.file_path // empty')

# Only lint TypeScript files
if [[ "$file_path" =~ \.(js|jsx|ts|tsx)$ ]] && [[ -f "$file_path" ]]; then
    if command -v eslint &> /dev/null; then
        # Non-blocking: show warnings but continue
        if eslint "$file_path" 2>/dev/null; then
            echo "2️⃣ ✅ Lint passed: $(basename "$file_path")"
            exit 0
        else
            echo "2️⃣ ⚠️  Lint warnings: $(basename "$file_path")"
            exit 2
        fi
    fi
fi

exit 0  