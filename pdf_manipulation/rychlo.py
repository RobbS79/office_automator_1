from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName


# Helper function to extract a numeric value from a PdfObject
def extract_numeric(value):
    if isinstance(value, PdfDict):
        return float(value[0])  # If it's a PdfDict, extract the first value as a float
    return float(value)  # Otherwise, convert it to float directly


# Load the template PDF
template_path = "/Users/robertsoroka/Downloads/23092021-VP-3+-+Žiadosť+o+vystavenie+prenosného+dokumentu+A1+z+dôvodu+vyslania+zamestnanca+na+územie+iného+členského+štátu+EÚ.pdf"
output_path = "output.pdf"
template_pdf = PdfReader(template_path)

for page in template_pdf.pages:
    annotations = page.get('/Annots')  # Direct access to annotations
    if annotations:
        print("Annotations exist!")
        for annotation in annotations:
            parent = annotation.get('/Parent')
            if "/AP" in annotation:
                ap_element = annotation.get('/AP')
                ap_element.update(PdfDict(D="/0"))
                ap_element.update(PdfDict(N="/0"))
                annotation.update(PdfDict(AP='/0'))
                annotation.update(PdfDict(AS='/On'))

            if parent and ("/T" not in annotation.keys() and parent.get(
                    '/FT') == '/Btn'):  # Check if the parent field is a button (checkbox or radio button)
                print("Annotation keys:", annotation.keys())
                print("Parent keys:", parent.keys())

                # Set the checkbox to checked
                annotation.update(PdfDict(V='/Yes'))

                # Optionally, resize the annotation by updating its /Rect (bounding box)
                # Here we reduce the size by modifying the /Rect (bounding box of the checkbox/radio button)
                rect = annotation.get('/Rect')
                if rect:
                    # Extract numeric values from the PdfObjects
                    x0 = extract_numeric(rect[0])
                    y0 = extract_numeric(rect[1])
                    x1 = extract_numeric(rect[2])
                    y1 = extract_numeric(rect[3])

                    # Calculate new width and height
                    new_width = x1 - x0
                    new_height = y1 - y0
                    scale_factor = 0.8  # Adjust the scale factor to make the circle smaller
                    new_width *= scale_factor
                    new_height *= scale_factor

                    # Update the Rect with the new size
                    annotation.update(PdfDict(Rect=[x0, y0, x0 + new_width, y0 + new_height]))

# Write the modified PDF to output
PdfWriter(output_path, trailer=template_pdf).write()

print(f"Modified PDF saved to {output_path}")
