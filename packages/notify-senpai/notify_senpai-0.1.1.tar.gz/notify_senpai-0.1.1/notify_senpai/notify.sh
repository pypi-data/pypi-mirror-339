#!/bin/bash

# Default message with emoji
MESSAGE=${1:-"execution done"}

# Fallback to osascript for macOS notifications
if [[ "$OSTYPE" == "darwin"* ]]; then
    osascript -e "display notification \"$MESSAGE 🫡\" with title \"Jupyter ✅\""

else
    echo "Notification: $MESSAGE"
fi

