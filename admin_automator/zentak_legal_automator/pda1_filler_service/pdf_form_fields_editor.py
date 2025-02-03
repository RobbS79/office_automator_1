from fillpdf import fillpdfs
#from .form_fields_mapper import form_fileds_mapper


class PDFFormFiller:
    def __init__(self, db_employee_json_object):
        self.db_employee_json_object = db_employee_json_object
        self.pda1_form_input_path = "/Users/robertsoroka/Downloads/23092021-VP-3+-+Žiadosť+o+vystavenie+prenosného+dokumentu+A1+z+dôvodu+vyslania+zamestnanca+na+územie+iného+členského+štátu+EÚ (1) (3) (4).pdf"
        self.pda1_form_output_path = "/Users/robertsoroka/PycharmProjects/office_automator_1/admin_automator/zentak_legal_automator/pda1_filler_service/pdf_forms/filled_form.pdf"
        #self.form_fileds_mapper = form_fileds_mapper

    def process_pda1_filler(self):
        json_data = self.db_employee_json_object
        data_form_fields = fillpdfs.get_form_fields(self.pda1_form_input_path)
        data_obj = {}

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

