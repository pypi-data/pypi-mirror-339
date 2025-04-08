#!/bin/bash -e
# file: .github/scripts/create-pr.sh

DRY_RUN=false

COMMIT_MESSAGE=$(git log -1 --pretty=%B)
SOURCE_BRANCH=$(git rev-parse --abbrev-ref HEAD)

ISSUE_URI="https://iremote.atlassian.net/browse"
ISSUE_REGEX='(([0-9]+)-|(app|APP|dops|DOPS|web|WEB)-?[0-9]+)'
LABELS=("ready-for-review" "auto-pr")

generate_random_color() {
    printf '%02x%02x%02x\n' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256))
}

label_exists() {
    local label_to_check="$1"
    existing_labels=$(gh label list --json name --jq ".[].name")
    if echo "$existing_labels" | grep -q "$label_to_check"; then
        return 0  # Label exists
    else
        return 1  # Label does not exist
    fi
}

create_or_check_labels() {
    local labels=("$@")
    for label in "${labels[@]}"; do
        color=$(generate_random_color)
        # $(gh label list --search "$label") search is not working as expected, using jq instead
        existing_labels=$(gh label list --json name --jq ".[].name")
        matched_label=$(echo "$existing_labels" | grep -o "$label")
        if [ -z "$matched_label" ]; then
          if [ "$DRY_RUN" = true ]; then
            echo "Dry run: gh label create \"$label\" --description \"$label\" --color \"$color\""
          else
            echo "Label '$label' not found. Creating label with random color..."
            gh label create "$label" --description "$label" --color "$color"
          fi
        else
            echo "Label '$label' already exists."
        fi
    done
}

extract_issue_token() {
    local branch=$1
    if [[ "$branch" =~ $ISSUE_REGEX ]]; then
        echo "${BASH_REMATCH[1]/_/-}"
    else
        echo ""
    fi
}

create_pull_request() {
    local source_branch=$1
    local destination_branch=$2
    local pr_title=$3
    local pr_body=$4
    local labels=("${@:5}")

    local command="gh pr create \
          -B \"$destination_branch\" \
          -H \"$source_branch\" \
          --title \"$pr_title\" \
          --body \"$pr_body\""

    if [ "$DRY_RUN" = true ]; then
        for label in "${labels[@]}"; do
            command+=" --label \"$label\""
        done
        echo "$command"
    else
        echo "Creating pull request..."
        for label in "${labels[@]}"; do
            command+=" --label \"$label\""
        done
        eval "$command"
    fi
}

# Extract the owner of the source branch (not useful for now)
#OWNER=$(git log --format='%ae' -n 1)

ISSUE_OR_TOKEN=$(extract_issue_token "$SOURCE_BRANCH")
DESTINATION_BRANCH="main"
PR_BODY=$([ -n "${ISSUE_OR_TOKEN}" ] && echo "Issue: ${ISSUE_URI}/${ISSUE_OR_TOKEN}" || echo "$COMMIT_MESSAGE")
PR_TITLE="Merge ${SOURCE_BRANCH} into ${DESTINATION_BRANCH} - ${ISSUE_OR_TOKEN}"

create_or_check_labels "${LABELS[@]}"
create_pull_request "${SOURCE_BRANCH}" "${DESTINATION_BRANCH}" "$PR_TITLE" "$PR_BODY" "${LABELS[@]}"
