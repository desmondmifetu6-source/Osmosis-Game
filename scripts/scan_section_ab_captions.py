import os
import subprocess
import glob
import json

ps_script = r"""
param([string]$dirPath)

$code = @"
using System;
using System.IO;
using System.Threading.Tasks;
using Windows.Graphics.Imaging;
using Windows.Media.Ocr;
using Windows.Storage;

public class WinOCR {
    public static async Task<string> Recognize(string path) {
        try {
            StorageFile file = await StorageFile.GetFileFromPathAsync(path);
            using (var stream = await file.OpenAsync(FileAccessMode.Read)) {
                BitmapDecoder decoder = await BitmapDecoder.CreateAsync(stream);
                SoftwareBitmap bitmap = await decoder.GetSoftwareBitmapAsync();
                OcrEngine engine = OcrEngine.TryCreateFromLanguage(new Windows.Globalization.Language("en-US"));
                OcrResult result = await engine.RecognizeAsync(bitmap);
                return result.Text;
            }
        } catch (Exception ex) {
            return "ERROR: " + ex.Message;
        }
    }
}
"@

Add-Type -TypeDefinition $code -Language CSharp -CompilerOptions "/reference:`"C:\Program Files (x86)\Windows Kits\10\UnionMetadata\10.0.19041.0\Windows.winmd`""

$files = Get-ChildItem -Path $dirPath -Filter "*.png"
foreach ($f in $files) {
    $text = [WinOCR]::Recognize($f.FullName).GetAwaiter().GetResult()
    $cleanText = $text -replace "`r`n", " " -replace "`n", " "
    Write-Output "$($f.Name)|||$cleanText"
}
"""

with open("scripts/run_ocr_batch.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

print("Running OCR on section a-b images...")
cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", "scripts/run_ocr_batch.ps1", "-dirPath", r"c:\Users\Desmond\Desktop\final_osmosis\section a-b images"]
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")

results = {}
for line in res.stdout.splitlines():
    if "|||" in line:
        filename, text = line.split("|||", 1)
        results[filename] = text.strip()

with open("scripts/section_ab_ocr_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Scanned {len(results)} images from section a-b images!")
for k, v in list(results.items())[:20]:
    print(f"{k} => {v[:80]}")
