# Submission Verification Instructions

After the competition ends, participants can independently verify their submissions using the published private key.

## What You'll Need

1. Your original encrypted submission file (`.csv.gpg`)
2. The published private key (`kalendium_private.key`)
3. GPG installed on your system

## Step-by-Step Verification

### 1. Install GPG (if not already installed)

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install gnupg
```

**macOS:**
```bash
brew install gnupg
```

**Windows:**
Download from https://gpg4win.org/

### 2. Import the Private Key

```bash
# Import the published private key
gpg --import kalendium_private.key

# Verify the key was imported
gpg --list-secret-keys kalendium@one.com
```

### 3. Decrypt Your Submission

```bash
# Decrypt your submission file
gpg --decrypt your_submission.csv.gpg > your_submission_decrypted.csv

# View the decrypted content
cat your_submission_decrypted.csv
```

### 4. Verify Against Published Results

Compare your decrypted submission with the published competition results to ensure:
- Your submission was included
- The data matches exactly what you submitted
- No modifications were made during processing

## Key Verification

To verify you're using the correct private key, check the fingerprint:

```bash
gpg --fingerprint kalendium@one.com
```

The fingerprint should match what's published in the competition repository.

## Alternative: Use the Provided Script

If you're in the competition repository directory, you can use:

```bash
# Make sure the private key is imported first
gpg --import kalendium_private.key

# Use the decryption script
./decrypt_submission.sh your_submission.csv.gpg
```

## Troubleshooting

**"No secret key" error:**
- Ensure you imported the private key correctly
- Check that the key email matches: `kalendium@one.com`

**"Bad signature" or "integrity check failed":**
- Your file may be corrupted
- Verify you have the exact file you submitted

**Permission denied:**
- Make sure the script is executable: `chmod +x decrypt_submission.sh`

## Security Note

The private key is published only for transparency and verification purposes. This key should never be used for future competitions or any other cryptographic purposes.

## Questions?

If you encounter issues during verification, please open an issue in the competition repository with:
1. The error message you received
2. The GPG version you're using (`gpg --version`)
3. Your operating system