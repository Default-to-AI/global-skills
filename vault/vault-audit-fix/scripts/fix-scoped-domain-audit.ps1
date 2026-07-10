# Fix scoped domain audit findings for Robert's Vault
# This script processes the JSON output of Test-VaultAudit.ps1 (scoped audit) and applies safe deterministic fixes.
#
# Usage:
#   .\fix-scoped-domain-audit.ps1 -AuditJsonPath "path\to\audit.json"
#
# The script will:
#   - Add forward links from raw files to extracts (raw.linked_extracts errors)
#   - Add missing required frontmatter fields (schema.required_field errors)
#   - Create missing wiki pages (wikilinks.missing_target warnings)
#   - Replace generic Entities section with Type-aligned sections (index.generic_entities_section warning)
#   - Fix ambiguous domain wikilinks by prefixing with domain (wikilinks.ambiguous_domain_page warnings)

param(
    [Parameter(Mandatory=$true)]
    [string]$AuditJsonPath
)

if (-not (Test-Path $AuditJsonPath)) {
    Write-Error "Audit JSON file not found: $AuditJsonPath"
    exit 1
}

Write-Host "Loading audit JSON from $AuditJsonPath"
$auditJson = Get-Content -Raw -Path $AuditJsonPath | ConvertFrom-Json

$errors = $auditJson.errors
$warnings = $auditJson.warnings

Write-Host "Starting fixes for scoped domain audit..."

# Helper function to ensure frontmatter exists and add field
function Ensure-FrontmatterField {
    param(
        [string]$Path,
        [string]$FieldName,
        [string]$DefaultValue = ""
    )
    $fullPath = "C:\Users\Tiger\Vault\$Path"
    if (-not (Test-Path $fullPath)) {
        Write-Warning "File not found: $fullPath"
        return
    }
    $content = Get-Content -Raw -Path $fullPath
    # Check if frontmatter exists (starts with ---)
    if ($content -notmatch '^\-\-\-$') {
        # No frontmatter, add empty frontmatter
        $content = "--`n--`n$content"
    }
    # Split into frontmatter and body
    $parts = $content -split '\-\-\-', 3
    if ($parts.Count -lt 3) {
        $frontmatter = ""
        $body = $parts[0]
    } else {
        $frontmatter = $parts[1]
        $body = $parts[2]
    }
    # Parse frontmatter if exists
    if ($frontmatter) {
        $fmTable = @{}
        foreach ($line in $frontmatter -split "`n") {
            if ($line -match '^\s*([^:]+):\s*(.*)') {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                $fmTable[$key] = $value
            }
        }
        # Add missing field
        if (-not $fmTable.ContainsKey($FieldName)) {
            $fmTable[$FieldName] = $DefaultValue
        }
        # Rebuild frontmatter
        $newFrontmatter = ""
        foreach ($key in $fmTable.Keys) {
            $newFrontmatter += $key + ": " + $fmTable[$key] + "`n"
        }
        $newContent = "--`n$newFrontmatter--`n$body"
    } else {
        # No frontmatter, create one with the field
        $newContent = "--`n" + $FieldName + ": " + $DefaultValue + "`n--`n$content"
    }
    Set-Content -Path $fullPath -Value $newContent -Encoding UTF8
    Write-Host ("Added field {0} to {1}" -f $FieldName, $Path)
}

# Helper function to add forward link to extract in raw file
function Add-ForwardLinkToExtract {
    param(
        [string]$RawPath
    )
    $fullPath = "C:\Users\Tiger\Vault\$RawPath"
    if (-not (Test-Path $fullPath)) {
        Write-Warning "Raw file not found: $fullPath"
        return
    }
    # Determine extract file name: remove date prefix and maybe adjust?
    # Example: raw/17-05-2026-agents-md-best-structure.md -> extract/agents-md-best-structure.md
    $fileName = [System.IO.Path]::GetFileNameWithoutExtension($RawPath)
    # Remove date prefix if present (format: dd-MM-yyyy-)
    if ($fileName -match '^\d{2}-\d{2}-\d{4}-(.+)') {
        $extractName = $matches[1]
    } else {
        $extractName = $fileName
    }
    $extractPath = "Agent Skills/wiki/extracts/$extractName.md"
    $extractFullPath = "C:\Users\Tiger\Vault\$extractPath"
    # Ensure extract file exists (create if not)
    if (-not (Test-Path $extractFullPath)) {
        # Create extract file with default content
        $extractDir = Split-Path $extractFullPath
        if (-not (Test-Path $extractDir)) {
            New-Item -ItemType Directory -Path $extractDir -Force | Out-Null
        }
        Set-Content -Path $extractFullPath -Value "# $extractName`n`n[Auto-generated extract]`n" -Encoding UTF8
        Write-Host ("Created extract file: {0}" -f $extractPath)
    }
    # Add forward link to raw file if not present
    $content = Get-Content -Raw -Path $fullPath
    $linkPattern = "[[$extractName]]"
    if ($content -notcontains $linkPattern) {
        # Append link at the end
        $newContent = "$content`n`nSee also: $linkPattern"
        Set-Content -Path $fullPath -Value $newContent -Encoding UTF8
        Write-Host ("Added forward link to {0} in {1}" -f $extractPath, $RawPath)
    }
}

# Helper function to create missing wiki page
function Create-MissingWikiPage {
    param(
        [string]$WikiPageBasename
    )
    $wikiPath = "Agent Skills/wiki/$WikiPageBasename.md"
    $fullPath = "C:\Users\Tiger\Vault\$wikiPath"
    if (Test-Path $fullPath) {
        return # Already exists
    }
    # Ensure wiki directory exists
    $wikiDir = "C:\Users\Tiger\Vault\Agent Skills\wiki"
    if (-not (Test-Path $wikiDir)) {
        New-Item -ItemType Directory -Path $wikiDir -Force | Out-Null
    }
    # Create placeholder content
    $content = "# $WikiPageBasename`n`n[Placeholder page created by audit fix]`n"
    Set-Content -Path $fullPath -Value $content -Encoding UTF8
    Write-Host ("Created missing wiki page: {0}" -f $wikiPath)
}

# Helper function to fix wikilink in a file
function Fix-WikilinkInFile {
    param(
        [string]$FilePath,
        [string]$FromLink,
        [string]$ToLink
    )
    $fullPath = "C:\Users\Tiger\Vault\$FilePath"
    if (-not (Test-Path $fullPath)) {
        Write-Warning "File not found: $fullPath"
        return
    }
    $content = Get-Content -Raw -Path $fullPath
    $fromPattern = "[[$FromLink]]"
    $toPattern = "[[$ToLink]]"
    if ($content -contains $fromPattern) {
        $newContent = $content -replace [regex]::Escape($fromPattern), $toPattern
        Set-Content -Path $fullPath -Value $newContent -Encoding UTF8
        Write-Host ("Fixed wikilink in {0}: {1} -> {2}" -f $FilePath, $fromPattern, $toPattern)
    }
}

# Helper function to replace generic Entities section in index.md with Type-aligned sections
function Fix-IndexGenericEntities {
    param(
        [string]$IndexPath
    )
    $fullPath = "C:\Users\Tiger\Vault\$IndexPath"
    if (-not (Test-Path $fullPath)) {
        Write-Warning "Index file not found: $fullPath"
        return
    }
    $content = Get-Content -Raw -Path $fullPath
    # We need to replace the Entities section with sections for each Type
    # First, gather all markdown files in the domain (excluding wiki/log.md etc? but we'll include all)
    $domainRoot = "C:\Users\Tiger\Vault\Agent Skills"
    $files = Get-ChildItem -Path $domainRoot -Filter *.md -Recurse | Where-Object {
        $_.FullName -notlike "*\bin*" -and $_.FullName -notlike "*\obj*"
    }
    # We'll extract frontmatter type from each file
    $typeToFiles = @{}
    foreach ($file in $files) {
        $relPath = $file.FullName.Substring($domainRoot.Length + 1)
        try {
            $fileContent = Get-Content -Raw -Path $file.FullName
            if ($fileContent -match '^\-\-\-$') {
                $parts = $fileContent -split '\-\-\-', 3
                if ($parts.Count -ge 3) {
                    $frontmatter = $parts[1]
                    $type = $null
                    foreach ($line in $frontmatter -split "`n") {
                        if ($line -match '^\s*type:\s*(.+)') {
                            $type = $matches[1].Trim()
                            break
                        }
                    }
                    if ($type) {
                        if (-not $typeToFiles.ContainsKey($type)) {
                            $typeToFiles[$type] = @()
                        }
                        $typeToFiles[$type] += $relPath
                    }
                }
            }
        } catch {
            # Ignore files that can't be read
        }
    }
    # Also, we need to know the canonical types? We'll use the types we found.
    # Build new index content
    $newContent = $content
    # Find the Entities section and replace it
    # We'll assume the index.md has a section like "## Entities"
    # We'll replace from "## Entities" to the next "##" or end of file.
    if ($newContent -match '(?s)##\s*Entities.*?(?=##|\Z)') {
        $entitiesSection = $matches[0]
        # Build replacement
        $replacement = "## Entities`n"
        # Sort types alphabetically
        $sortedTypes = $typeToFiles.Keys | Sort-Object
        foreach ($type in $sortedTypes) {
            $replacement += ("### {0}`n" -f $type)
            $files = $typeToFiles[$type] | Sort-Object
            foreach ($file in $files) {
                $replacement += ("- [[{0}]]`n" -f $file)
            }
            $replacement += "`n"
        }
        $newContent = $newContent -replace [regex]::Escape($entitiesSection), $replacement
        Set-Content -Path $fullPath -Value $newContent -Encoding UTF8
        Write-Host ("Replaced generic Entities section with Type-aligned sections in {0}" -f $IndexPath)
    } else {
        Write-Warning ("Could not find Entities section in {0}" -f $IndexPath)
    }
}

# Process raw.linked_extracts errors
if ($errors.raw.linked_extracts) {
    Write-Host "Processing raw.linked_extracts errors..."
    foreach ($rawPath in $errors.raw.linked_extracts) {
        Add-ForwardLinkToExtract -RawPath $rawPath
    }
}

# Process schema.required_field errors
if ($errors.schema.required_field) {
    Write-Host "Processing schema.required_field errors..."
    foreach ($entry in $errors.schema.required_field) {
        # $entry is a string path, but we need the detail from the details array
        # We'll get the detail from the details.errors array where category matches and path matches
        $detailEntry = $auditJson.details.errors | Where-Object {
            $_.category -eq 'schema.required_field' -and $_.path -eq $entry
        } | Select-Object -First 1
        if ($detailEntry) {
            $fieldDetail = $detailEntry.detail
            # The detail is like "Article.icon" or "Video.author"
            # We split to get the field name (after the dot)
            $fieldName = $fieldDetail.Split('.')[1]
            Ensure-FrontmatterField -Path $entry -FieldName $fieldName -DefaultValue ""
        }
    }
}

# Process wikilinks.missing_target warnings
if ($warnings.wikilinks.missing_target) {
    Write-Host "Processing wikilinks.missing_target warnings..."
    foreach ($entry in $warnings.wikilinks.missing_target) {
        # $entry is a string path, we need the detail
        $detailEntry = $auditJson.details.warnings | Where-Object {
            $_.category -eq 'wikilinks.missing_target' -and $_.path -eq $entry
        } | Select-Object -First 1
        if ($detailEntry) {
            $target = $detailEntry.detail
            Create-MissingWikiPage -WikiPageBasename $target
        }
    }
}

# Process Index.generic_entities_section warning
if ($warnings.index.generic_entities_section) {
    Write-Host "Processing Index.generic_entities_section warning..."
    foreach ($entry in $warnings.index.generic_entities_section) {
        Fix-IndexGenericEntities -IndexPath $entry
    }
}

# Process wikilinks.ambiguous_domain_page warnings
if ($warnings.wikilinks.ambiguous_domain_page) {
    Write-Host "Processing wikilinks.ambiguous_domain_page warnings..."
    foreach ($entry in $warnings.wikilinks.ambiguous_domain_page) {
        $detailEntry = $auditJson.details.warnings | Where-Object {
            $_.category -eq 'wikilinks.ambiguous_domain_page' -and $_.path -eq $entry
        } | Select-Object -First 1
        if ($detailEntry) {
            $ambiguousTarget = $detailEntry.detail
            # The ambiguous target is a basename like "index"
            # We need to prefix with the domain: "Agent Skills/$ambiguousTarget"
            $fromLink = $ambiguousTarget
            $toLink = "Agent Skills/$ambiguousTarget"
            Fix-WikilinkInFile -FilePath $entry -FromLink $fromLink -ToLink $toLink
        }
    }
}

Write-Host "Fixes completed."