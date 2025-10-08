#!/bin/bash
# Fixed version - step 2

input_json=$(cat)

# Extract file path
file_path=$(echo "$input_json" | jq -r '.tool_input.file_path // empty')

# FIX 2: Count actual changes using git diff
diff_output=$(git diff --numstat "$file_path" 2>/dev/null | head -1)
[[ -z "$diff_output" ]] && diff_output=$(git diff --cached --numstat "$file_path" 2>/dev/null | head -1)

if [[ -n "$diff_output" ]]; then
    added=$(echo "$diff_output" | awk '{print $1}')
    removed=$(echo "$diff_output" | awk '{print $2}')

    # Parse diff hunks to detect changed lines (adjacent -/+ pairs)
    if [[ "$added" != "-" && "$removed" != "-" ]]; then
        actual_changed=0
        actual_added=0
        actual_removed=0

        # Read diff and track consecutive removals followed by additions (= changes)
        removal_count=0

        while IFS= read -r line; do
            # Only match actual diff lines (not headers like ---, +++, @@)
            if [[ "$line" =~ ^-[^-] ]]; then
                # Line removed - just count it
                ((removal_count++))
            elif [[ "$line" =~ ^\+[^+] ]]; then
                # Line added (escape + since it's a regex special char)
                if [[ $removal_count -gt 0 ]]; then
                    # This is a change (removal followed by addition)
                    ((actual_changed++))
                    ((removal_count--))
                else
                    # Pure addition
                    ((actual_added++))
                fi
            elif [[ "$line" =~ ^\ |^@@ ]]; then
                # Context line or hunk header - flush remaining removals
                if [[ $removal_count -gt 0 ]]; then
                    actual_removed=$((actual_removed + removal_count))
                    removal_count=0
                fi
            fi
        done < <(git diff "$file_path" 2>/dev/null || git diff --cached "$file_path" 2>/dev/null)

        # Handle any trailing removals
        if [[ $removal_count -gt 0 ]]; then
            actual_removed=$((actual_removed + removal_count))
        fi

        # Build output string
        parts=()
        [[ $actual_changed -gt 0 ]] && parts+=("$actual_changed changed")
        [[ $actual_added -gt 0 ]] && parts+=("$actual_added added")
        [[ $actual_removed -gt 0 ]] && parts+=("$actual_removed removed")

        if [[ ${#parts[@]} -gt 0 ]]; then
            changes=$(IFS=', '; echo "${parts[*]}")
        else
            changes="no changes"
        fi
    else
        changes="+$added -$removed"
    fi
else
    # If not in git or no diff, just count total lines
    total_lines=$(wc -l < "$file_path" 2>/dev/null || echo "0")
    changes="$total_lines total"
fi

# ISSUE 3: Still no error checking
STATS_FILE="$HOME/.claude/logs/stats.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') | $file_path | $changes" >> "$STATS_FILE"

echo "📊 Logged: $changes"
exit 0