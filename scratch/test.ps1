Add-Type -AssemblyName System.Speech
 = New-Object System.Speech.Synthesis.SpeechSynthesizer
.SelectVoice('Microsoft Haruka Desktop')
.SetOutputToWaveFile('scratch/test_haruka.wav')
.Speak('こんにちは。テストです。')
.Dispose()
