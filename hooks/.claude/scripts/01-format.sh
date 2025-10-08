#!/bin/bash
# Format with Prettier

input_json=$(cat)
file_path=$(echo "$input_json" | jq -r '.tool_input.file_path // empty')

# Only format TypeScript files
if [[ "$file_path" =~ \.(js|jsx|ts|tsx)$ ]] && [[ -f "$file_path" ]]; then
    if command -v prettier &> /dev/null; then
        prettier --write "$file_path" 2>/dev/null
        echo "1️⃣ ✨ Formatted: $(basename "$file_path")"
    fi
fi

exit 0