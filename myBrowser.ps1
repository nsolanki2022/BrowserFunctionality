# Command line parameters
# .\myBrowser.ps1 -BrowsingMode incognito  # Open in incognito mode
# .\myBrowser.ps1  # Open in normal mode
# .\open_urls.ps1 -BrowsingMode incognito  # Open in incognito mode using default file
# .\open_urls.ps1 -BrowsingMode normal -URLsFile custom_urls.txt  # Open in normal mode using custom file
# Get-Help .\open_urls.ps1


<#
.SYNOPSIS
    Open URLs in Chrome or Firefox browsers with different browsing modes.

.DESCRIPTION
    This script opens URLs in Chrome or Firefox browsers. You can specify the browser, browsing mode (normal or incognito),
    and provide a custom URLs file.

.PARAMETER Browser
    Specifies the browser to use. Use "chrome" for Chrome and "firefox" for Firefox.
    Default is "chrome".

.PARAMETER BrowsingMode
    Specifies the browsing mode. Use "normal" to open in normal mode and "incognito" to open in incognito mode.
    Default is "normal".

.PARAMETER URLsFile
    Specifies the file containing URLs. Default is "urls.txt".

.EXAMPLE
    .\open_urls.ps1 -Browser chrome -BrowsingMode incognito
    Opens URLs in incognito mode using the default URLs file in Chrome.

.EXAMPLE
    .\open_urls.ps1 -Browser firefox -BrowsingMode normal -URLsFile custom_urls.txt
    Opens URLs in normal mode using a custom URLs file in Firefox.

#>

param (
    [string]$Browser = "chrome",
    [string]$BrowsingMode = "normal",
    [string]$URLsFile = "urls.txt",

    [string]$PassPhrase = "test"
)

if ($Browser -eq "chrome") {
    $browserArgument = "--incognito"
} elseif ($Browser -eq "firefox") {
    $browserArgument = "--private-window"
} else {
    Write-Host "Error: Unsupported browser specified. Supported values: chrome, firefox."
    Exit 1
}

# if (-not (Test-Path $URLsFile)) {
#     Write-Host "Error: The specified URLs file '$URLsFile' does not exist."
#     Exit 1
# }

$pythonExePath = "python"
$pythonScriptPath = "file_crypto.py"
$decrypt = "-d"
$encrypt = "-e"
# Decrypt file before reading the file content.
$pythonCommand = "$pythonExePath $pythonScriptPath $URLsFile $PassPhrase $decrypt"

# Run the Python script
Invoke-Expression $pythonCommand

# $URLs = Get-Content "cattlerider_tickets_Urls.txt"
$URLs = Get-Content $URLsFile

# Encrypt the file back after reading the file content
$pythonCommand = "$pythonExePath $pythonScriptPath $URLsFile $PassPhrase $encrypt"

# Run the Python script
Invoke-Expression $pythonCommand

$windowUrls = @()

foreach ($url in $URLs) {
    if ($url -eq "") {
        # Start-Process "chrome" -ArgumentList "--new-window", "--incognito", ($windowUrls -join " ")
        # $windowUrls = @()
        if ($BrowsingMode -eq "incognito") {
            # Start-Process "chrome" -ArgumentList "--new-window", "--incognito", ($windowUrls -join " ")
            Start-Process $Browser -ArgumentList "--new-window", $browserArgument, ($windowUrls -join " ")

        } else {
            # Start-Process "chrome" -ArgumentList "--new-window", ($windowUrls -join " ")
            Start-Process $Browser -ArgumentList "--new-window", ($windowUrls -join " ")
        }
        $windowUrls = @()
    } else {
        $windowUrls += $url
    }
}

# Open the last set of URLs, if any
if ($windowUrls.Count -gt 0) {
    # Start-Process "chrome" -ArgumentList "--new-window", "--incognito", ($windowUrls -join " ")
    if ($BrowsingMode -eq "incognito") {
        # Start-Process "chrome" -ArgumentList "--new-window", "--incognito", ($windowUrls -join " ")
        Start-Process $Browser -ArgumentList "--new-window", $browserArgument, ($windowUrls -join " ")
    } else {
        # Start-Process "chrome" -ArgumentList "--new-window", ($windowUrls -join " ")
        Start-Process $Browser -ArgumentList "--new-window", ($windowUrls -join " ")
    }    
}