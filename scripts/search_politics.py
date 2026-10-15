import pypdf

def search_pdf(path, name):
    reader = pypdf.PdfReader(path)
    print(f"=== {name} ===")
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        for line in text.splitlines():
            l = line.lower()
            if "politics" in l or "newly" in l or "native" in l or ("dt" in l and "tm" in l and "na" in l):
                print(f"P{i+1}: {line}")

search_pdf("T2510616_IEEE_Paper.pdf", "IEEE")
search_pdf("T2510616.pdf", "THESIS")
