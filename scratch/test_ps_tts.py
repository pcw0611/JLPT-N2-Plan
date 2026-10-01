import os
import subprocess

text = "会社で上司と女性社員が話しています。女の人はこのあと、何をしなければなりませんか。来週の大阪出張、先方の都合で打ち合わせが翌日にも入ることになったんだ。"
with open("scratch/sample_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

ps_code = """
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice("Microsoft Haruka Desktop")
$synth.SetOutputToWaveFile("scratch/sample_out.wav")
$text = [System.IO.File]::ReadAllText("scratch/sample_text.txt", [System.Text.Encoding]::UTF8)
$synth.Speak($text)
$synth.Dispose()
Write-Output "OK"
"""

with open("scratch/run_tts.ps1", "w", encoding="utf-8") as f:
    f.write(ps_code)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "scratch/run_tts.ps1"], capture_output=True, text=True)
print("Returncode:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
print("Exists wav:", os.path.exists("scratch/sample_out.wav"))
if os.path.exists("scratch/sample_out.wav"):
    print("Wav size:", os.path.getsize("scratch/sample_out.wav"))
