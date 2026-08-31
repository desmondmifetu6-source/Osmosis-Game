import asyncio

async def test():
    try:
        import winsdk.windows.media.ocr as ocr
        import winsdk.windows.graphics.imaging as imaging
        import winsdk.windows.storage as storage
        print("winsdk available!")
    except Exception as e:
        print("winsdk error:", e)

asyncio.run(test())
