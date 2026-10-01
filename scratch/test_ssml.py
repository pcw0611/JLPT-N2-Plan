import os, subprocess

ssml = """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>会社で上司と女性社員が話しています。女の人はこのあと、何をしなければなりませんか。</s>
  <break time="800ms"/>
  <prosody pitch="-15%" rate="-5%">
    来週の大阪出張、先方の都合で打ち合わせが翌日にも入ることになったんだ。
  </prosody>
  <break time="600ms"/>
  <prosody pitch="+15%" rate="0%">
    分かりました。では新幹線はそのままですね。
  </prosody>
  <break time="600ms"/>
  <prosody pitch="-15%" rate="-5%">
    うん。ただ、ホテルの予約を一日延ばして、もう一泊できるように変更手続きをしてくれるかい？
  </prosody>
  <break time="600ms"/>
  <prosody pitch="+15%" rate="0%">
    かしこまりました。すぐに旅行会社に電話して変更いたします。
  </prosody>
</speak>"""

with open("scratch/sample_ssml.xml", "w", encoding="utf-8") as f:
    f.write(ssml)

ps_code = """
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice("Microsoft Haruka Desktop")
$synth.SetOutputToWaveFile("scratch/sample_ssml.wav")
$ssml = [System.IO.File]::ReadAllText("scratch/sample_ssml.xml", [System.Text.Encoding]::UTF8)
$synth.SpeakSsml($ssml)
$synth.Dispose()
Write-Output "SSML_OK"
"""

with open("scratch/run_ssml.ps1", "w", encoding="utf-8") as f:
    f.write(ps_code)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "scratch/run_ssml.ps1"], capture_output=True, text=True)
print("Returncode:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
if os.path.exists("scratch/sample_ssml.wav"):
    print("Wav size:", os.path.getsize("scratch/sample_ssml.wav"))
    subprocess.run(["ffmpeg", "-y", "-i", "scratch/sample_ssml.wav", "-b:a", "128k", "scratch/sample_ssml.mp3"], capture_output=True)
    print("Mp3 size:", os.path.getsize("scratch/sample_ssml.mp3"))
