import urllib.parse
import subprocess
import sys
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def download_namu_doc(doc_name, out_file):
    encoded = urllib.parse.quote(doc_name)
    url = f"https://namu.wiki/w/{encoded}"
    cmd = [
        "curl.exe", "-s", "-L", url,
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "-o", str(out_file)
    ]
    subprocess.run(cmd, check=True)
    size = Path(out_file).stat().st_size
    print(f"Downloaded {doc_name} -> {out_file} ({size} bytes)")
    return size

if __name__ == "__main__":
    download_namu_doc("春日影", "scratch/namu_haruhikage.html")
    download_namu_doc("壱雫空", "scratch/namu_hitoshizuku.html")
    download_namu_doc("碧天伴走", "scratch/namu_hekitenbansou.html")
    download_namu_doc("詩超絆", "scratch/namu_utakotoba.html")
