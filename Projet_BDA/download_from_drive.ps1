# PowerShell script to download and extract BDA project data from Google Drive
# Prerequisites: rclone must be installed and configured with 'gdrive' remote

$ARCHIVE = 'BDA-project-final-data.zip'
$REMOTE = 'gdrive'
$REMOTE_ROOT = 'bda-website-data'
$DEST_DIR = $PSScriptRoot

# Check if rclone is available
try {
    rclone --version > $null 2>&1
}
catch {
    Write-Error "rclone not found; install and configure rclone before running this script."
    exit 1
}

# Create destination directory if it doesn't exist
if (-not (Test-Path $DEST_DIR)) {
    New-Item -ItemType Directory -Force -Path $DEST_DIR | Out-Null
}

Write-Host "Fetching $ARCHIVE from $REMOTE`:$REMOTE_ROOT"
rclone copyto "$REMOTE`:$REMOTE_ROOT/$ARCHIVE" "$DEST_DIR\$ARCHIVE" --progress

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to fetch $ARCHIVE"
    exit 1
}

Write-Host "Unzipping $ARCHIVE into $DEST_DIR"
Expand-Archive -Path "$DEST_DIR\$ARCHIVE" -DestinationPath $DEST_DIR -Force

if ($LASTEXITCODE -ne 0) {
    Write-Error "Unzip failed"
    exit 1
}

Write-Host "Done."
