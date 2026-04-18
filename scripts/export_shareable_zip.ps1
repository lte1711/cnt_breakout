$source = "."
$dest = "cnt-shareable.zip"

$exclude = @(
    ".git",
    ".env",
    "runtime.log",
    "state.json",
    "docs.zip",
    "src.zip",
    "__pycache__"
)

if (Test-Path $dest) {
    Remove-Item $dest -Force
}

$items = Get-ChildItem $source -Force | Where-Object {
    $exclude -notcontains $_.Name
}

Compress-Archive -Path $items.FullName -DestinationPath $dest
Write-Host "Created $dest"
