param([string]$Dir = "D:\ai-playbooks\resources\tmp")

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding           = [System.Text.Encoding]::UTF8

function To-LongPath([string]$p) {
    if ($p.StartsWith("\\?\")) { return $p }
    return "\\?\$p"
}

foreach ($path in [System.IO.Directory]::EnumerateFiles((To-LongPath $Dir), "*.md")) {
    $name = [System.IO.Path]::GetFileName($path)
    $clean = ($name -replace "[^\x20-\x7E]", "") -replace "\s+", " "
    $clean = $clean.Trim()
    if (-not $clean) { continue }
    if ($clean -eq $name) { continue }

    $base = [System.IO.Path]::GetFileNameWithoutExtension($clean)
    $ext  = [System.IO.Path]::GetExtension($clean)
    $target = [System.IO.Path]::Combine($Dir, $clean)
    $i = 1
    while ([System.IO.File]::Exists((To-LongPath $target))) {
        $target = [System.IO.Path]::Combine($Dir, "$base-$i$ext")
        $i++
    }
    [System.IO.File]::Move((To-LongPath $path), (To-LongPath $target))
}
