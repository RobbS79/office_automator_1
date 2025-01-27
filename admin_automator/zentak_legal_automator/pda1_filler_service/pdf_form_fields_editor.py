import pdfrw
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName
from .form_fields_mapper import form_fileds_mapper
import re


class PDFFormFiller:
    from .form_fields_mapper import form_fileds_mapper
    def __init__(self, db_employee_json_object):
        #self.pda1_data_dict = pda1_data_dict
        self.db_employee_json_object = db_employee_json_object
        self.pda1_form_input_path = "~/office_automator_1/admin_automator/zentak_legal_automator/pda1_filler_service/pdf_forms/pda1_form.pdf"
        self.pda1_form_output_path = "~/office_automator_1/admin_automator/zentak_legal_automator/pda1_filler_service/pdf_forms/filled_form.pdf"
        self.form_fileds_mapper = form_fileds_mapper


    def extract_numeric(self, value):
        if isinstance(value, PdfDict):
            return float(value[0])  # If it's a PdfDict, extract the first value as a float
        return float(value)  # Otherwise, convert it to float directly



    # Variables for the data to fill
    nazov_firmy = "ZENTAK s.r.o."
    ico_firmy = "52328121"
    sidlo_firmy_ulica = "Poštová 50/1"
    sidlo_firmy_mesto = "Bardejov"
    sidlo_firmy_psc = "085 01"
    sidlo_firmy_stat = "Slovensko"
    kontaktna_osoba_firmy = "Jozef Soroka"
    zamestnanec_pohlavie_muz = True #hodnota True mi musi prist z querysetu z DB Djanga
    zamestnanec_pohlavie_zena = False
    """
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
    zamestnanec_nahradza_zamestnanca_ano = False
    zamestnanec_nahradza_zamestnanca_nie = True
    kmenova_firma_ADZ_ano = False
    kmenova_firma_ADZ_nie = True
    kmenova_firma_viac_zmluv_sr_ano = True
    kmenova_firma_viac_zmluv_sr_nie = False
    zamestnanec_uz_v_krajine_bol_vyslany_ano = True
    zamestnanec_uz_v_krajine_bol_vyslany_nie = False
    zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_ano = False
    zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_nie = True
    """
    
    """
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
    firma_pocet_zamestnancov = "13"
    firma_vykon_zamestnanci_sr = "3"
    firma_vykon_zamestnanci_out = "9"
    firma_admin_zamestnanci_sr = "1"
    firma_zamestnanci_provided = "0"
    firma_percent_obrat_sr = "75%"
    firma_percent_obrat_out = "25%"
    firma_ina_krajina_obratu = "Nemecko"
    firma_pocet_zakaziek_sr = "22"
    firma_pocet_zakaziek_out = "7"
    miesto_vyslania_nazov_subjektu = "Haus - Essen, Germany"
    miesto_vyslania_ico = "23432223"
    miesto_vyslania_ulica = "Nachskstrasse 23"
    miesto_vyslania_mesto = "Essen"
    miesto_vyslania_psc = "23453"
    miesto_vyslania_stat = "Deutschland"
    miesto_vyslania_kontakt_osoba = "Franz"
    id_lode = ""
    zamestnanec_vyslany_od = "1.1.2025"
    zamestnanec_vyslany_do = "31.12.2025"
    zamestnanec_druh_cinnosti_pri_vyslani = "murár"
    druh_cinnosti_kod_nace = "54321"
    podpis_firma_miesto = "Bardejov"
    podpis_firma_datum = "3.1.2025"
    podpis_zamestnanec_miesto = "Poprad"
    podpis_zamestnanec_datum = "1.1.2025"
    """

    """
        elif value == "zamestnanec_pracovna_napln_pred_vyslanim":
            text_fields_mapper[key] = zamestnanec_pracovna_napln_pred_vyslanim
        elif value == "odmenujuca_firma_v_zahranici":
            text_fields_mapper[key] = odmenujuca_firma_v_zahranici
        elif value == "cielova_firma_v_zahranici":
            text_fields_mapper[key] = cielova_firma_v_zahranici
        elif value == "nahradenie_zamestnanca_meno_priezvisko":
            text_fields_mapper[key] = nahradenie_zamestnanca_meno_priezvisko
        elif value == "firma_pocet_zamestnancov":
            text_fields_mapper[key] = firma_pocet_zamestnancov
        elif value == "firma_vykon_zamestnanci_sr":
            text_fields_mapper[key] = firma_vykon_zamestnanci_sr
        elif value == "firma_vykon_zamestnanci_out":
            text_fields_mapper[key] = firma_vykon_zamestnanci_out
        elif value == "firma_admin_zamestnanci_sr":
            text_fields_mapper[key] = firma_admin_zamestnanci_sr
        elif value == "firma_zamestnanci_provided":
            text_fields_mapper[key] = firma_zamestnanci_provided
        elif value == "firma_percent_obrat_sr":
            text_fields_mapper[key] = firma_percent_obrat_sr
        elif value == "firma_percent_obrat_out":
            text_fields_mapper[key] = firma_percent_obrat_out
        elif value == "firma_ina_krajina_obratu":
            text_fields_mapper[key] = firma_ina_krajina_obratu
        elif value == "firma_pocet_zakaziek_sr":
            text_fields_mapper[key] = firma_pocet_zakaziek_sr
        elif value == "firma_pocet_zakaziek_out":
            text_fields_mapper[key] = firma_pocet_zakaziek_out
        elif value == "miesto_vyslania_nazov_subjektu":
            text_fields_mapper[key] = miesto_vyslania_nazov_subjektu
        elif value == "miesto_vyslania_ico":
            text_fields_mapper[key] = miesto_vyslania_ico
        elif value == "miesto_vyslania_ulica":
            text_fields_mapper[key] = miesto_vyslania_ulica
        elif value == "miesto_vyslania_mesto":
            text_fields_mapper[key] = miesto_vyslania_mesto
        elif value == "miesto_vyslania_psc":
            text_fields_mapper[key] = miesto_vyslania_psc
        elif value == "miesto_vyslania_stat":
            text_fields_mapper[key] = miesto_vyslania_stat
        elif value == "miesto_vyslania_kontakt_osoba":
            text_fields_mapper[key] = miesto_vyslania_kontakt_osoba
        elif value == "id_lode":
            text_fields_mapper[key] = id_lode
        elif value == "zamestnanec_vyslany_od":
            text_fields_mapper[key] = zamestnanec_vyslany_od
        elif value == "zamestnanec_vyslany_do":
            text_fields_mapper[key] = zamestnanec_vyslany_do
        elif value == "zamestnanec_druh_cinnosti_pri_vyslani":
            text_fields_mapper[key] = zamestnanec_druh_cinnosti_pri_vyslani
        elif value == "druh_cinnosti_kod_nace":
            text_fields_mapper[key] = druh_cinnosti_kod_nace
        elif value == "podpis_firma_miesto":
            text_fields_mapper[key] = podpis_firma_miesto
        elif value == "podpis_firma_datum":
            text_fields_mapper[key] = podpis_firma_datum
        elif value == "podpis_zamestnanec_miesto":
            text_fields_mapper[key] = podpis_zamestnanec_miesto
        elif value == "podpis_zamestnanec_datum":
            text_fields_mapper[key] = podpis_zamestnanec_datum
    
    
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
        elif value == "zamestnanec_subezny_uvazok_inej_firme_ano":
            checkbox_fields_mapper[key] = zamestnanec_subezny_uvazok_inej_firme_ano
        elif value == "zamestnanec_subezny_uvazok_inej_firme_nie":
            checkbox_fields_mapper[key] = zamestnanec_subezny_uvazok_inej_firme_nie
        elif value == "zamestnanec_odmena_od_kmenovej_firmy_ano":
            checkbox_fields_mapper[key] = zamestnanec_odmena_od_kmenovej_firmy_ano
        elif value == "zamestnanec_odmena_od_kmenovej_firmy_nie":
            checkbox_fields_mapper[key] = zamestnanec_odmena_od_kmenovej_firmy_nie
        elif value == "zamestnanec_zadanie_prace_kmenovou_firmou_ano":
            checkbox_fields_mapper[key] = zamestnanec_zadanie_prace_kmenovou_firmou_ano
        elif value == "zamestnanec_zadanie_prace_kmenovou_firmou_nie":
            checkbox_fields_mapper[key] = zamestnanec_zadanie_prace_kmenovou_firmou_nie
        elif value == "zamestnanec_nahradza_zamestnanca_ano":
            checkbox_fields_mapper[key] = zamestnanec_nahradza_zamestnanca_ano
        elif value == "zamestnanec_nahradza_zamestnanca_nie":
            checkbox_fields_mapper[key] = zamestnanec_nahradza_zamestnanca_nie
        elif value == "kmenova_firma_ADZ_ano":
            checkbox_fields_mapper[key] = kmenova_firma_ADZ_ano
        elif value == "kmenova_firma_ADZ_nie":
            checkbox_fields_mapper[key] = kmenova_firma_ADZ_nie
        elif value == "kmenova_firma_viac_zmluv_sr_ano":
            checkbox_fields_mapper[key] = kmenova_firma_viac_zmluv_sr_ano
        elif value == "kmenova_firma_viac_zmluv_sr_nie":
            checkbox_fields_mapper[key] = kmenova_firma_viac_zmluv_sr_nie
        elif value == "zamestnanec_uz_v_krajine_bol_vyslany_ano":
            checkbox_fields_mapper[key] = zamestnanec_uz_v_krajine_bol_vyslany_ano
        elif value == "zamestnanec_uz_v_krajine_bol_vyslany_nie":
            checkbox_fields_mapper[key] = zamestnanec_uz_v_krajine_bol_vyslany_nie
        elif value == "zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_ano":
            checkbox_fields_mapper[key] = zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_ano
        elif value == "zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_nie":
            checkbox_fields_mapper[key] = zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_nie"""

    def process_pda1_filler(self):
        def map_response_json_to_form_fields_mapper(json_response, form_fields_mapper, level=0):
            indent = "  " * level  # To visualize recursion levels
            form_fields_mapper_working = form_fields_mapper.copy()

            print(f"{indent}Processing level {level}, form_fields_mapper: {form_fields_mapper}")

            for key, value in form_fields_mapper_working.items():
                if isinstance(value, dict):  # Check for nested structure
                    print(f"{indent}Key '{key}' has nested structure: {value}")
                    # Prevent infinite recursion for empty or circular references
                    if not value:
                        print(f"{indent}Empty structure for key '{key}', skipping.")
                        continue
                    form_fields_mapper_working[key] = map_response_json_to_form_fields_mapper(json_response, value,
                                                                                              level + 1)
                    print(f"{indent}Recursive call completed for key: {key}")
                else:
                    for k, v in json_response.items():
                        if k == value:
                            form_fields_mapper_working[key] = v
                            print(f"{indent}{key} key found in json_response. Its value is: {v}")
                            break
                    else:
                        print(f"{indent}Line: 251, key {key} not matched or processed.")

            print(f"{indent}Completed processing level {level}. Result: {form_fields_mapper_working}")
            return form_fields_mapper_working

        def check_the_checkbox(pdf_annotation, nm_substring):
            annotation = pdf_annotation
            checkboxes_to_map = self.form_fileds_mapper["checkboxes"]
            checkbox_field_name_composer = None
            nm_element = annotation.get('/NM')
            pattern = r"Group(\d{1,2})\[0\]\.#field\[(\d)\]"
            match = re.search(pattern, nm_element)
            if match:
                group_no = match.group(1)  # Captured first digit
                option = match.group(2)  # Captured second digit
                checkbox_field_name_composer = f"Group{group_no}[0].#field[{option}]"
            else:
                print("No match found.")

            if checkbox_field_name_composer and checkbox_field_name_composer in checkboxes_to_map:
                if annotation.get('/Parent') and annotation.get('/Parent').get('/FT') == '/Btn':  # Checkbox logic
                    annotation.update(PdfDict(V=pdfrw.PdfName('On')))
                    print(f"Checkbox {checkbox_field_name_composer} checked.")

        text_fields_mapper = map_response_json_to_form_fields_mapper(
            self.db_employee_json_object, self.form_fileds_mapper["text_fields"]
        )
        checkbox_fields_mapper = map_response_json_to_form_fields_mapper(
            self.db_employee_json_object, self.form_fileds_mapper["checkboxes"]
        )

        template_pdf = pdfrw.PdfReader(self.pda1_form_input_path)

        # Process each page in the PDF
        for page in template_pdf.pages:
            annotations = page['/Annots']
            if annotations:
                for annotation in annotations:
                    field = annotation.get('/T')  # Field name
                    if field:
                        field_name = field[1:-1]  # Remove surrounding parentheses
                        print(f"Processing text field: {field_name}")
                        if field_name in text_fields_mapper:
                            annotation.update(PdfDict(V=text_fields_mapper[field_name]))
                            print(f"Updated text field: {field_name}")
                    elif annotation.get('/NM'):
                        nm_field = annotation.get('/NM')
                        print(f"Processing checkbox: {nm_field}")
                        if nm_field in checkbox_fields_mapper:
                            check_the_checkbox(annotation, nm_field)

        # Save the updated PDF
        pdfrw.PdfWriter().write(self.pda1_form_output_path, template_pdf)
        print("PDF processing completed. Output saved.")


"""                        if "Group2[0].#field[0]" in annotation.get("/NM") and uvazok_pracovna_zmluva == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    current_checkbox_field_name_composer = check_the_checkbox(annotation,"Group2[0].#field[0]")

                if "Group2[0].#field[1]" in annotation.get("/NM") and uvazok_dohoda == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group2[0].#field[1]")

                if "Group3[0].#field[0]" in annotation.get("/NM") and zamestnanec_poisteny_mesiac_spat_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group3[0].#field[0]")

                if "Group3[0].#field[1]" in annotation.get("/NM") and zamestnanec_poisteny_mesiac_spat_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_poisteny_mesiac_spat_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group3[0].#field[1]")

                if "Group4[0].#field[0]" in annotation.get("/NM") and zamestnanec_vyslany_jak_kmenovi_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_jak_kmenovi_ano
                    current_checkbox_field_name_composer = check_the_checkbox(annotation,"Group4[0].#field[0]")

                if "Group4[0].#field[1]" in annotation.get("/NM") and zamestnanec_vyslany_jak_kmenovi_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_poisteny_mesiac_spat_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation,"Group4[0].#field[1]")

                if "Group5[0].#field[0]" in annotation.get("/NM") and zamestnanec_vyslany_prideleny_inej_firme_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_ano
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group5[0].#field[0]")

                if "Group5[0].#field[1]" in annotation.get("/NM") and zamestnanec_vyslany_prideleny_inej_firme_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group5[0].#field[1]")

                if "Group6[0].#field[0]" in annotation.get("/NM") and zamestnanec_subezny_uvazok_inej_firme_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group6[0].#field[0]")

                if "Group6[0].#field[1]" in annotation.get("/NM") and zamestnanec_subezny_uvazok_inej_firme_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group6[0].#field[1]")

                if "Group7[0].#field[0]" in annotation.get("/NM") and zamestnanec_odmena_od_kmenovej_firmy_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group7[0].#field[0]")

                if "Group7[0].#field[1]" in annotation.get("/NM") and zamestnanec_odmena_od_kmenovej_firmy_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group7[0].#field[1]")

                if "Group8[0].#field[0]" in annotation.get("/NM") and zamestnanec_zadanie_prace_kmenovou_firmou_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group8[0].#field[0]")

                if "Group8[0].#field[1]" in annotation.get("/NM") and zamestnanec_zadanie_prace_kmenovou_firmou_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group8[0].#field[1]")

                if "Group9[0].#field[0]" in annotation.get("/NM") and zamestnanec_nahradza_zamestnanca_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group9[0].#field[0]")

                if "Group9[0].#field[1]" in annotation.get("/NM") and zamestnanec_nahradza_zamestnanca_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group9[0].#field[1]")

                if "Group10[0].#field[0]" in annotation.get("/NM") and kmenova_firma_ADZ_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group10[0].#field[0]")

                if "Group10[0].#field[1]" in annotation.get("/NM") and kmenova_firma_ADZ_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group10[0].#field[1]")

                if "Group11[0].#field[0]" in annotation.get("/NM") and kmenova_firma_viac_zmluv_sr_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group11[0].#field[0]")

                if "Group11[0].#field[1]" in annotation.get("/NM") and kmenova_firma_viac_zmluv_sr_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group11[0].#field[1]")

                if "Group12[0].#field[0]" in annotation.get("/NM") and zamestnanec_uz_v_krajine_bol_vyslany_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group12[0].#field[0]")

                if "Group12[0].#field[1]" in annotation.get("/NM") and zamestnanec_uz_v_krajine_bol_vyslany_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    #checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group12[0].#field[1]")

                if "Group13[0].#field[0]" in annotation.get("/NM") and zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_ano == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    # checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group13[0].#field[0]")

                if "Group13[0].#field[1]" in annotation.get("/NM") and zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_nie == True:
                    print(f"Current annotation is: {annotation.get('/NM')}")
                    # checkbox_fields_mapper[key] = zamestnanec_vyslany_prideleny_inej_firme_nie
                    current_checkbox_field_name_composer = check_the_checkbox(annotation, "Group13[0].#field[1]")"""
