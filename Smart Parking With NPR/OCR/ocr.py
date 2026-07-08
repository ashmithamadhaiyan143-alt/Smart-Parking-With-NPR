import easyocr
reader = easyocr.Reader(['en'])

def detect_plate(path):
    result = reader.readtext(path)
    for (_, text, _) in result:
        if len(text) >= 6:
            return text
    return "NOT DETECTED"