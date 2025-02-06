from fillpdf import fillpdfs
import os

class PDFFormFiller:
    def __init__(self, db_employee_json_object):
        self.db_employee_json_object = db_employee_json_object
        self.pda1_form_input_path = os.path.expanduser(
            "~pda1_filler_service/pdf_forms/pda1_form.pdf")
        self.pda1_form_output_path = os.path.expanduser(
            "~pda1_filler_service/pdf_forms/filled_form.pdf")


    def process_pda1_filler(self):
            json_data = self.db_employee_json_object
            data_form_fields = fillpdfs.get_form_fields(self.pda1_form_input_path)
            data_obj = {"nazov_firmy": "ZENTAK s.r.o.",
                        "ico_firmy": "52328121",
                        "sidlo_firmy_ulica": "Postova 5",
                        "sidlo_firmy_mesto": "sidlo_firmy_psc",
                        "sidlo_firmy_stat": "Slovensko",
                        "kontaktna_osoba_firmy": "Ing. Jozef Soroka",

                        }

            for json_data_key, json_data_value in json_data.items():
                print(json_data_key)
                if json_data_key in data_form_fields.keys():
                    # Replace False boolean values with None
                    if json_data_value is False:
                        data_obj[json_data_key] = None
                    else:
                        data_obj[json_data_key] = json_data_value

            try:
                fillpdfs.write_fillable_pdf(self.pda1_form_input_path, self.pda1_form_output_path, data_obj)
            except KeyError as e:
                print(f"Error generating PDF: {e}")
                # Additional error handling can go here

