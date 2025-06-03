#!/bin/bash

# Script to encrypt CSV submission with public key
# Usage: ./encrypt_submission.sh <csv_file>

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <csv_file>"
    echo "Example: $0 test_submission.csv"
    exit 1
fi

CSV_FILE="$1"
PUBLIC_KEY="kalendium_public.key"
ENCRYPTED_FILE="${CSV_FILE%.csv}.csv.gpg"

# Check if CSV file exists
if [ ! -f "$CSV_FILE" ]; then
    echo "Error: CSV file '$CSV_FILE' not found"
    exit 1
fi

# Check if public key exists
if [ ! -f "$PUBLIC_KEY" ]; then
    echo "Error: Public key '$PUBLIC_KEY' not found"
    exit 1
fi

echo "Encrypting $CSV_FILE with $PUBLIC_KEY..."

# Create temporary keyring to avoid conflicts with existing keys
TEMP_KEYRING=$(mktemp -d)
export GNUPGHOME="$TEMP_KEYRING"

# Import the public key to temporary keyring
gpg --batch --quiet --import "$PUBLIC_KEY"

# Encrypt the CSV file using the key fingerprint
gpg --batch --trust-model always --armor --encrypt --recipient kalendium@one.com --output "$ENCRYPTED_FILE" "$CSV_FILE"

# Clean up temporary keyring
rm -rf "$TEMP_KEYRING"

# Remove the original CSV file for security
rm "$CSV_FILE"

echo "Encryption complete!"
echo "Original file: $CSV_FILE (deleted)"
echo "Encrypted file: $ENCRYPTED_FILE"
echo ""
echo "You can now submit the encrypted file: $ENCRYPTED_FILE"