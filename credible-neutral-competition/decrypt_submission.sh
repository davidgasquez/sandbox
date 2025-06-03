#!/bin/bash

# Script to decrypt CSV submission files
# Usage: ./decrypt_submission.sh <encrypted_file>

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <encrypted_file>"
    echo "Example: $0 test_submission.csv.gpg"
    exit 1
fi

ENCRYPTED_FILE="$1"
DECRYPTED_FILE="${ENCRYPTED_FILE%.gpg}"

# Check if encrypted file exists
if [ ! -f "$ENCRYPTED_FILE" ]; then
    echo "Error: Encrypted file '$ENCRYPTED_FILE' not found"
    exit 1
fi

# Check if the file has .gpg extension
if [[ "$ENCRYPTED_FILE" != *.gpg ]]; then
    echo "Error: File '$ENCRYPTED_FILE' does not appear to be a GPG encrypted file (.gpg extension expected)"
    exit 1
fi

# Check if decrypted file already exists
if [ -f "$DECRYPTED_FILE" ]; then
    echo "Warning: Decrypted file '$DECRYPTED_FILE' already exists"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Decryption cancelled"
        exit 1
    fi
fi

echo "Decrypting $ENCRYPTED_FILE..."

# Decrypt the file
if gpg --batch --quiet --decrypt --output "$DECRYPTED_FILE" "$ENCRYPTED_FILE"; then
    # Remove the encrypted file for security
    rm "$ENCRYPTED_FILE"
    
    echo "Decryption successful!"
    echo "Encrypted file: $ENCRYPTED_FILE (deleted)"
    echo "Decrypted file: $DECRYPTED_FILE"
    echo ""
    echo "CSV content preview:"
    echo "===================="
    head -5 "$DECRYPTED_FILE"
    echo ""
    echo "Total lines: $(wc -l < "$DECRYPTED_FILE")"
else
    echo "Error: Decryption failed"
    echo "Make sure you have the private key that corresponds to the public key used for encryption"
    exit 1
fi