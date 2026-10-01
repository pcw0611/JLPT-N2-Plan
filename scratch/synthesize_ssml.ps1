
param(
    [string]$ssmlPath,
    [string]$wavPath
)
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice("Microsoft Haruka Desktop")
$synth.SetOutputToWaveFile($wavPath)
$ssml = [System.IO.File]::ReadAllText($ssmlPath, [System.Text.Encoding]::UTF8)
$synth.SpeakSsml($ssml)
$synth.Dispose()
Write-Output "SUCCESS"
