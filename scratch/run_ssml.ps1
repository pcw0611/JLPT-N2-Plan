
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice("Microsoft Haruka Desktop")
$synth.SetOutputToWaveFile("scratch/sample_ssml.wav")
$ssml = [System.IO.File]::ReadAllText("scratch/sample_ssml.xml", [System.Text.Encoding]::UTF8)
$synth.SpeakSsml($ssml)
$synth.Dispose()
Write-Output "SSML_OK"
