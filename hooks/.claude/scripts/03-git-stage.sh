#!/bin/bash
# Auto-stage in Git

input_json=$(cat)
file_path=$(echo "$input_json" | jq -r '.tool_input.file_path // empty')

# Check if file exists
if [[ ! -f "$file_path" ]]; then
    exit 0
fi

# Find the git repo for this specific file (handles nested repos)
file_dir=$(dirname "$file_path")
git_root=$(git -C "$file_dir" rev-parse --show-toplevel 2>/dev/null)

if [[ -n "$git_root" ]]; then
    # Get absolute path of file
    abs_file_path=$(cd "$file_dir" && pwd)/$(basename "$file_path")
    
    # Get relative path from git root
    rel_path=$(realpath --relative-to="$git_root" "$abs_file_path" 2>/dev/null || echo "$file_path")
    
    # Stage the file in its git repo
    (cd "$git_root" && git add "$rel_path" 2>/dev/null)
    status=$(cd "$git_root" && git status --short "$rel_path" 2>/dev/null)
    
    echo "3️⃣ 📋 Git staged: $(basename "$file_path")"
    if [[ -n "$status" ]]; then
        echo "   Status: $status"
    fi
fi

exit 0