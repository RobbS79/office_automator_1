import pdfrw
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName
from pdf_manipulation.static.form_fields_mapper import form_fileds_mapper
import re

def extract_numeric(value):
    if isinstance(value, PdfDict):
        return float(value[0])  # If it's a PdfDict, extract the first value as a float
    return float(value)  # Otherwise, convert it to float directly

def check_the_checkbox(pdf_annotation,nm_substring):
    #from static.form_fields_mapper import form_fileds_mapper
    annotation = pdf_annotation
    checkboxes_to_map = form_fileds_mapper["checkboxes"]
    checkbox_field_name_composer = None
    nm_element = annotation.get('/NM')
    pattern = r"Group(\d)\[0\]\.#field\[(\d)\]"
    match = re.search(pattern, nm_element)
    if match:
        group_no = match.group(1)  # Captured first digit
        option = match.group(2)  # Captured second digit
        checkbox_field_name_composer = f"Group{group_no}[0].#field[{option}]"
    else:
        print("No match found.")

    if checkbox_field_name_composer is not None and checkbox_field_name_composer in checkboxes_to_map.keys():
        parent = annotation.get('/Parent')
        if "/AP" in annotation and checkbox_field_name_composer == nm_substring:
            ap_element = annotation.get('/AP')
            if isinstance(ap_element, PdfDict):
                ap_element.update(PdfDict(D="/0"))
                ap_element.update(PdfDict(N="/0"))
                #annotation.update(PdfDict(AP='/0'))
                annotation.update(PdfDict(AS=pdfrw.PdfName('Yes')))
            if not isinstance(ap_element, PdfDict):
                ap_element = PdfDict(D="/0", N="/0")
                annotation.update(ap_element)
            if parent and ("/T" not in annotation.keys() and parent.get(
                    '/FT') == '/Btn'):  # Check if the parent field is a button (checkbox or radio button)
                # Set the checkbox to checked
                annotation.update(PdfDict(V=pdfrw.PdfName('On')))

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
                    #print("Function run")
                    return checkbox_field_name_composer

text_fields_mapper = form_fileds_mapper["text_fields"]
checkbox_fields_mapper = form_fileds_mapper["checkboxes"]
# Variables for the data to fill
nazov_firmy = "ZENTAK s.r.o."
ico_firmy = "52328121"
sidlo_firmy_ulica = "Poštová 50/1"
sidlo_firmy_mesto = "Bardejov"
sidlo_firmy_psc = "085 01"
sidlo_firmy_stat = "Slovensko"
kontaktna_osoba_firmy = "Jozef Soroka"
zamestnanec_pohlavie_muz = True
zamestnanec_pohlavie_zena = False
uvazok_pracovna_zmluva = True
uvazok_dohoda = False
zamestnanec_poisteny_mesiac_spat_ano = False
zamestnanec_poisteny_mesiac_spat_nie = True
zamestnanec_vyslany_jak_kmenovi_ano = True
zamestnanec_vyslany_jak_kmenovi_nie = False
zamestnanec_vyslany_prideleny_inej_firme_ano = True
zamestnanec_vyslany_prideleny_inej_firme_nie = True
zamestnanec_subezny_uvazok_inej_firme_ano = False
zamestnanec_subezny_uvazok_inej_firme_nie = True
zamestnanec_odmena_od_kmenovej_firmy_ano = True
zamestnanec_odmena_od_kmenovej_firmy_nie = False
zamestnanec_zadanie_prace_kmenovou_firmou_ano = True
zamestnanec_zadanie_prace_kmenovou_firmou_nie = False
kmenova_firma_ADZ_ano = False
kmenova_firma_ADZ_nie = True


zamestnanec_titul_pred_menom = ""
zamestnanec_meno = "Robert"
zamestnanec_priezvisko = "Soroka"
zamestnanec_titul_za_menom = ""
zamestnanec_datum_narodenia = "20.01.1997"
zamestnanec_miesto_narodenia = "Bardejov"
zamestnanec_statna_prislusnost = "slovenská"
zamestnanec_rodne_priezvisko = "Soroka"
zamestnanec_rodne_cislo = "9701206361"
zamestnanec_adresa_ulica = "Krátka 3704/5"
zamestnanec_adresa_mesto = "Bardejov"
zamestnanec_adresa_psc = "08501"
zamestnanec_adresa_stat = "Slovensko"
zamestnanec_tel_cislo = "+420739392447"
zamestnanec_email = "soroka.robert8@gmail.com"
zamestnanec_cudzinec_doklad_pobyt = ""
zamestnanec_cudzinec_pracovne_povolenie = ""
zamestnanec_korespondencna_adresa = "Krátka 3704/5 Bardejov 08501, Slovensko"
andresa_na_dorucenie_pda1 = zamestnanec_korespondencna_adresa
pracovny_vztah_od = "1.1.2019"
pracovny_vztah_do = "neurčito"
zamestnanec_pracovna_napln_pred_vyslanim = "sales"
odmenujuca_firma_v_zahranici = ""
cielova_firma_v_zahranici = "" #PREMENOVAŤ PREMENNÚ NA - ODMENUJUCA_FIRMA_V_ZAHRANICI
nahradenie_zamestnanca_meno_priezvisko = ""

# Update mapper values based on the variables
for key, value in text_fields_mapper.items():
    if value == "nazov_firmy":
        text_fields_mapper[key] = nazov_firmy
    elif value == "ico_firmy":
        text_fields_mapper[key] = ico_firmy
    elif value == "sidlo_firmy_ulica":
        text_fields_mapper[key] = sidlo_firmy_ulica
    elif value == "sidlo_firmy_mesto":
        text_fields_mapper[key] = sidlo_firmy_mesto
    elif value == "sidlo_firmy_psc":
        text_fields_mapper[key] = sidlo_firmy_psc
    elif value == "sidlo_firmy_stat":
        text_fields_mapper[key] = sidlo_firmy_stat
    elif value == "kontaktna_osoba_firmy":
        text_fields_mapper[key] = kontaktna_osoba_firmy
    elif value == "zamestnanec_titul_pred_menom":
        text_fields_mapper[key] = zamestnanec_titul_pred_menom
    elif value == "zamestnanec_meno":
        text_fields_mapper[key] = zamestnanec_meno
    elif value == "zamestnanec_priezvisko":
        text_fields_mapper[key] = zamestnanec_priezvisko
    elif value == "zamestnanec_titul_za_menom":
        text_fields_mapper[key] = zamestnanec_titul_za_menom
    elif value == "zamestnanec_datum_narodenia":
        text_fields_mapper[key] = zamestnanec_datum_narodenia
    elif value == "zamestnanec_statna_prislusnost":
        text_fields_mapper[key] = zamestnanec_statna_prislusnost
    elif value == "zamestnanec_rodne_priezvisko":
        text_fields_mapper[key] = zamestnanec_rodne_priezvisko
    elif value == "zamestnanec_rodne_cislo":
        text_fields_mapper[key] = zamestnanec_rodne_cislo
    elif value == "zamestnanec_adresa_ulica":
        text_fields_mapper[key] = zamestnanec_adresa_ulica
    elif value == "zamestnanec_adresa_mesto":
        text_fields_mapper[key] = zamestnanec_adresa_mesto
    elif value == "zamestnanec_adresa_psc":
        text_fields_mapper[key] = zamestnanec_adresa_psc
    elif value == "zamestnanec_adresa_stat":
        text_fields_mapper[key] = zamestnanec_adresa_stat
    elif value == "zamestnanec_tel_cislo":
        text_fields_mapper[key] = zamestnanec_tel_cislo
    elif value == "zamestnanec_email":
        text_fields_mapper[key] = zamestnanec_email
    elif value == "zamestnanec_cudzinec_doklad_pobyt":
        text_fields_mapper[key] = zamestnanec_cudzinec_doklad_pobyt
    elif value == "zamestnanec_cudzinec_pracovne_povolenie":
        text_fields_mapper[key] = zamestnanec_cudzinec_pracovne_povolenie
    elif value == "zamestnanec_korespondencna_adresa":
        text_fields_mapper[key] = zamestnanec_korespondencna_adresa
    elif value == "andresa_na_dorucenie_pda1":
        text_fields_mapper[key] = andresa_na_dorucenie_pda1
    elif value == "pracovny_vztah_od":
        text_fields_mapper[key] = pracovny_vztah_od
    elif value == "pracovny_vztah_do":
        text_fields_mapper[key] = pracovny_vztah_do
    elif value == "zamestnanec_pracovna_napln_pred_vyslanim":
        text_fields_mapper[key] = zamestnanec_pracovna_napln_pred_vyslanim
    elif value == "odmenujuca_firma_v_zahranici":
        text_fields_mapper[key] = odmenujuca_firma_v_zahranici
    elif value == "cielova_firma_v_zahranici":
        text_fields_mapper[key] = cielova_firma_v_zahranici
    elif value == "nahradenie_zamestnanca_meno_priezvisko":
        text_fields_mapper[key] = nahradenie_zamestnanca_meno_priezvisko

for key, value in checkbox_fields_mapper.items():
    if value == "zamestnanec_pohlavie_muz":
        checkbox_fields_mapper[key] = zamestnanec_pohlavie_muz
    elif value == "zamestnanec_pohlavie_zena":
        checkbox_fields_mapper[key] = zamestnanec_pohlavie_zena
    elif value == "uvazok_pracovna_zmluva":
        checkbox_fields_mapper[key] = uvazok_pracovna_zmluva
    elif value == "uvazok_dohoda":
        checkbox_fields_mapper[key] = uvazok_dohoda
    elif value == "zamestnanec_poisteny_mesiac_spat_ano":
        checkbox_fields_mapper[key] = zamestnanec_poisteny_mesiac_spat_ano
    elif value == "zamestnanec_poisteny_mesiac_spat_nie":
        checkbox_fields_mapper[key] = zamestnanec_poisteny_mesiac_spat_nie
    elif value == "zamestnanec_vyslany_jak_kmenovi_ano":
        checkbox_fields_mapper[key] = zamestnanec_vyslany_jak_kmenovi_ano
    elif value == "zamestnanec_vyslany_jak_kmenovi_nie":
        checkbox_fields_mapper[key] = zamestnanec_vyslany_jak_kmenovi_nie
    elif value == "zamestnanec_vyslany_prideleny_inej_firme_ano":
        checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_ano
    elif value == "zamestnanec_vyslany_prideleny_inej_firme_nie":
        checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie


#for index, key, value in enumerate(mapper["checkboxes"].items()):

# Path to the existing PDF form (the one with fillable fields)
input_pdf_path = "/Users/robertsoroka/Downloads/23092021-VP-3+-+Žiadosť+o+vystavenie+prenosného+dokumentu+A1+z+dôvodu+vyslania+zamestnanca+na+územie+iného+členského+štátu+EÚ.pdf"
output_pdf_path = "filled_form.pdf"

# Read the existing PDF
template_pdf = pdfrw.PdfReader(input_pdf_path)
print(checkbox_fields_mapper)
# Process each page in the PDF
for page in template_pdf.pages:
    # Update form fields on the current page
    annotations = page['/Annots']
    if annotations:
        for annotation in annotations:
            field = annotation.get('/T')  # Field name
            #print(f"P annotation: {annotation.get('/P')}\n")
            if field:
                field_name = field[1:-1]  # Remove surrounding parentheses
                if field_name in text_fields_mapper.keys():
                    annotation.update(
                        pdfrw.PdfDict(V=text_fields_mapper[field_name]))

            elif "Group" in annotation.get("/NM"):

                if "Group1[0].#field[0]" in annotation.get("/NM") and zamestnanec_pohlavie_muz == True:
                    #print(f"Current annotation is: {annotation.get('/NM')}")
                    current_checkbox_field_name_composer = check_the_checkbox(annotation,"Group1[0].#field[0]")

                if "Group1[0].#field[1]" in annotation.get("/NM") and zamestnanec_pohlavie_zena == True:
                    print(zamestnanec_pohlavie_zena == True)
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group1[0].#field[1]")

                if "Group2[0].#field[0]" in annotation.get("/NM") and uvazok_pracovna_zmluva == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    current_checkbox_field_name_composer = check_the_checkbox(annotation,"Group2[0].#field[0]")

                if "Group2[0].#field[1]" in annotation.get("/NM") and uvazok_dohoda == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group2[0].#field[1]")

                if zamestnanec_poisteny_mesiac_spat_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group3[0].#field[0]")

                if zamestnanec_poisteny_mesiac_spat_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_poisteny_mesiac_spat_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group3[0].#field[1]")

                if zamestnanec_vyslany_jak_kmenovi_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_jak_kmenovi_ano
                    current_checkbox_field_name_composer = check_the_checkbox(annotation,"Group4[0].#field[0]")

                if zamestnanec_vyslany_jak_kmenovi_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_poisteny_mesiac_spat_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation,"Group4[0].#field[1]")

                if zamestnanec_vyslany_prideleny_inej_firme_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_ano
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group5[0].#field[0]")

                if zamestnanec_vyslany_prideleny_inej_firme_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group5[0].#field[1]")

                if zamestnanec_subezny_uvazok_inej_firme_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group6[0].#field[0]")

                if zamestnanec_subezny_uvazok_inej_firme_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group6[0].#field[1]")

                if zamestnanec_odmena_od_kmenovej_firmy_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group7[0].#field[0]")

                if zamestnanec_odmena_od_kmenovej_firmy_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group7[0].#field[1]")

                if zamestnanec_zadanie_prace_kmenovou_firmou_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group8[0].#field[0]")

                if zamestnanec_zadanie_prace_kmenovou_firmou_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group8[0].#field[1]")

                if kmenova_firma_ADZ_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group9[0].#field[0]")

                if kmenova_firma_ADZ_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group9[0].#field[1]")

# Save the updated PDF
pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

#print(f"Updated PDF saved to {output_pdf_path}")