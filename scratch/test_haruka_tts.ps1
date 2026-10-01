Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice("Microsoft Haruka Desktop")
$synth.SetOutputToWaveFile("scratch/test_haruka.wav")
$synth.Speak("会社で上司と女性社員が話しています。女の人はこのあと、何をしなければなりませんか。")
$synth.Dispose()

Write-Output "Generated scratch/test_haruka.wav successfully"
