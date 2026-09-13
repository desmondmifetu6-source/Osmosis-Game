Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asmn = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime].Assembly.GetName().FullName
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation.UniversalApiContract, ContentType = WindowsRuntime]

async function Get-OcrText($imgPath) {
    $file = await [Windows.Storage.StorageFile]::GetFileFromPathAsync($imgPath)
    $stream = await $file.OpenAsync([Windows.Storage.FileAccessMode]::Read)
    $decoder = await [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
    $bmp = await $decoder.GetSoftwareBitmapAsync()
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new("en-US"))
    $result = await $engine.RecognizeAsync($bmp)
    return $result.Text
}

# Simple PowerShell wrapper using Async
$file = [Windows.Storage.StorageFile]::GetFileFromPathAsync("C:\Users\Desmond\Desktop\final_osmosis\section a-b images\Screenshot 2026-08-03 162733.png").GetAwaiter().GetResult()
$stream = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read).GetAwaiter().GetResult()
$decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
$bmp = $decoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new("en-US"))
$result = $engine.RecognizeAsync($bmp).GetAwaiter().GetResult()
Write-Output "OCR Result:"
Write-Output $result.Text
