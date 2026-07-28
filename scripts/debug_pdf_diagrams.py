import fitz

doc = fitz.open("Dictionary Book 2.pdf")
print("Total pages:", len(doc))

# Let's inspect pages 40 to 100 in detail
vector_drawings_pages = 0
bitmap_image_pages = 0

sample_pages_vector = []
sample_pages_bitmap = []

for page_num in range(40, 200):
    page = doc.load_page(page_num)
    
    # Check drawings (vector shapes: lines, curves, diagrams drawn as vector paths)
    drawings = page.get_drawings()
    # Check images (bitmaps)
    images = page.get_images(full=True)
    
    if len(drawings) > 15: # page has substantial vector graphics
        vector_drawings_pages += 1
        if len(sample_pages_vector) < 10:
            sample_pages_vector.append((page_num + 1, len(drawings)))
            
    if images:
        bitmap_image_pages += 1
        if len(sample_pages_bitmap) < 10:
            sample_pages_bitmap.append((page_num + 1, len(images)))

print(f"Pages 40-200 with vector drawings (>15 paths): {vector_drawings_pages}")
print(f"Sample vector pages: {sample_pages_vector}")
print(f"Pages 40-200 with bitmap images: {bitmap_image_pages}")
print(f"Sample bitmap pages: {sample_pages_bitmap}")
