#!/bin/bash

# Script to export the private key for public transparency after competition ends
# Usage: ./export_private_key.sh

set -e

echo "⚠️  WARNING: This will export your PRIVATE KEY for public transparency!"
echo "Only run this AFTER the competition has ended."
echo ""
read -p "Are you sure you want to export the private key? (yes/NO): " -r

if [[ ! "$REPLY" == "yes" ]]; then
    echo "Export cancelled."
    exit 1
fi

PRIVATE_KEY_FILE="kalendium_private.key"
KEY_EMAIL="kalendium@one.com"

echo ""
echo "Exporting private key for: $KEY_EMAIL"

# Export the private key
if gpg --armor --export-secret-keys "$KEY_EMAIL" > "$PRIVATE_KEY_FILE"; then
    echo ""
    echo "✅ Private key exported successfully!"
    echo "File: $PRIVATE_KEY_FILE"
    echo ""
    echo "🔐 Key fingerprint:"
    gpg --fingerprint "$KEY_EMAIL"
    echo ""
    echo "📋 Next steps:"
    echo "1. Commit this private key to your repository"
    echo "2. Share the verification instructions with participants"
    echo "3. Participants can now verify their submissions independently"
    echo ""
    echo "⚠️  SECURITY NOTE: This key should only be used for this competition."
    echo "Never reuse this key for other purposes since it's now public."
else
    echo "❌ Error: Failed to export private key"
    echo "Make sure the key exists and you have permission to export it"
    exit 1
fi