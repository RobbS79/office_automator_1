import pdfrw
from pdf_manipulation.static.form_fields_mapper import form_fileds_mapper

mapper = form_fileds_mapper
# Variables for the data to fill
nazov_firmy = "ZENTAK s.r.o."
ico_firmy = "52328121"
sidlo_firmy_ulica = "Poštová 50/1"
sidlo_firmy_mesto = "Bardejov"
sidlo_firmy_psc = "085 01"
sidlo_firmy_stat = "Slovensko"
kontaktna_osoba_firmy = "Jozef Soroka"
zamestnanec_pohlavie_muz = "ano"
zamestnanec_pohlavie_zena = "nie"

# Update mapper values based on the variables
for key, value in mapper.items():
    if value == "nazov_firmy":
        form_fileds_mapper[key] = nazov_firmy
    elif value == "ico_firmy":
        form_fileds_mapper[key] = ico_firmy
    elif value == "sidlo_firmy_ulica":
        form_fileds_mapper[key] = sidlo_firmy_ulica
    elif value == "sidlo_firmy_mesto":
        form_fileds_mapper[key] = sidlo_firmy_mesto
    elif value == "sidlo_firmy_psc":
        form_fileds_mapper[key] = sidlo_firmy_psc
    elif value == "sidlo_firmy_stat":
        form_fileds_mapper[key] = sidlo_firmy_stat
    elif value == "kontaktna_osoba_firmy":
        form_fileds_mapper[key] = kontaktna_osoba_firmy

# Path to the existing PDF form (the one with fillable fields)
input_pdf_path = "/Users/robertsoroka/Downloads/23092021-VP-3+-+Žiadosť+o+vystavenie+prenosného+dokumentu+A1+z+dôvodu+vyslania+zamestnanca+na+územie+iného+členského+štátu+EÚ.pdf"
output_pdf_path = "filled_form.pdf"

# Read the existing PDF
template_pdf = pdfrw.PdfReader(input_pdf_path)
# Process each page in the PDF
for page in template_pdf.pages:
    # Update form fields on the current page
    annotations = page['/Annots']
    if annotations:
        for annotation in annotations:
            field = annotation.get('/T')  # Field name
            if field is None:
                annotation.update(
                    pdfrw.PdfDict(V='/Yes' if zamestnanec_pohlavie_muz == "ano" else '/Off',
                                  AS='/Yes' if zamestnanec_pohlavie_muz == "ano" else '/Off')
                )
            if field:
                field_name = field[1:-1]  # Remove surrounding parentheses
                if field_name in mapper:

                    # Update the field value
                    annotation.update(
                        pdfrw.PdfDict(V=mapper[field_name])
                    )



# Save the updated PDF
pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

print(f"Updated PDF saved to {output_pdf_path}")