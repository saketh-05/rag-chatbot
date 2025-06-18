#!/bin/bash

GEMINI_API_KEY=AIzaSyByMRT9v_5MAvXCP0hWkkP7zrSjbDZGuNA

# ==== Configuration ====
MODEL=gemini-2.0-flash

# ==== Functions ====
# Get repo name from directory
REPO_NAME=$(basename "$PWD")

# Extract info from Git
DESCRIPTION=$(git config --get remote.origin.url)
LAST_COMMIT=$(git log -1)

# Get file list & structure
FILE_STRUCTURE=$(find . -type f ! -path "*/.git/*" | sed 's|^\./||' | head -n 50)

# ======= COLLECT FILE CONTENTS =======
echo "📦 Gathering file contents..."

CONTENT=""

# Collect list of files
while IFS= read -r -d '' file; do
  # Check MIME type
  MIME_TYPE=$(file --mime-type -b "$file")
  if [[ "$MIME_TYPE" == text/* ]]; then
    REL_PATH="${file#./}"
    FILE_CONTENT=$(head -n 50 "$file")  # Limit to 200 lines per file
    CONTENT+="\n\n===== FILE: $REL_PATH =====\n$FILE_CONTENT"
  else
    echo "⚠️  Skipping binary file: $file"
  fi
done < <(git ls-files --cached --others --exclude-standard -z)

# ✅ Check if jq is installed
if ! command -v jq &> /dev/null; then
  echo "❌ 'jq' is required but not installed. Please install it and try again."
  exit 1
fi

PROMPT_TEXT=$(cat <<EOF
Generate a professional README.md file for a GitHub project with the following details:

Project Name: $REPO_NAME
Repository URL or remote: $DESCRIPTION
Recent commit: $LAST_COMMIT
File Structure: $FILE_STRUCTURE

Include the following sections in markdown:
- Project Title and Description
- What is this project about? and What are the key features?
- What are the technologies used in this project?
- Installation & setup instructions for each platform separately
- How to run the project?
- Usage with real executable examples
- Folder Structure

Source Files: $CONTENT
EOF
)

# Escape full prompt to JSON
ESCAPED_PROMPT=$(printf "%s" "$PROMPT_TEXT" | jq -Rs .)

# Now embed this into the JSON body
read -r -d '' PROMPT_body <<EOF
{
  "system_instruction": {
    "parts": [
      {
        "text": "You are an expert software engineer and technical writer. Based on the provided source code and files, generate a detailed, high-quality README.md file for the project."
      }
    ]
  },
  "contents": [
    {
      "parts": [
        {
          "text": $ESCAPED_PROMPT
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0.59
  }
}
EOF


echo "Sending request to Gemini API..."

# Call Gemini API
RESPONSE=$(curl -s https://generativelanguage.googleapis.com/v1beta/models/$MODEL:generateContent?key=$GEMINI_API_KEY \
  -H "Content-Type: application/json" \
  -d "$PROMPT_body")

# ✅ Debug the response
echo "Response: $RESPONSE"

# ✅ Extract using jq and check for error
ERROR_MSG=$(echo "$RESPONSE" | jq -r '.error.message // empty')

if [[ -n "$ERROR_MSG" ]]; then
  echo "❌ Error generating README: $ERROR_MSG"
  exit 1
else
  README_CONTENT=$(echo "$RESPONSE" | jq -r '.candidates[0].content.parts[0].text')

  new_content=$(echo "$README_CONTENT" | awk 'NR>1')
  # Write to README.md
  if find README.md -type f -print -quit | grep -q .; then
    echo "Creating READMEmore.md..."
    echo "$new_content" > READMEmore.md
  else
    echo "Creating new README.md..."
    echo "$new_content" > README.md
    echo -e "\n✅ README.md generated successfully!"
  fi
  echo "Work Done!"
fi
