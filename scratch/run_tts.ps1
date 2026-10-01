
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice("Microsoft Haruka Desktop")
$synth.SetOutputToWaveFile("scratch/sample_out.wav")
$text = [System.IO.File]::ReadAllText("scratch/sample_text.txt", [System.Text.Encoding]::UTF8)
$synth.Speak($text)
$synth.Dispose()
Write-Output "OK"
