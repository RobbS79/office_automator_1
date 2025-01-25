import os
import json
import re
from unidecode import unidecode
from ..models import ValueStream

class AttachmentCategoryAssigner:
    def __init__(self, attachment_path, json_file_path):
        self.attachment_path = unidecode(attachment_path)
        self.attachment_path = self.attachment_path
        self.json_file_path = json_file_path
        self.json_mapper = self.load_json_mapper()

    def load_json_mapper(self):
        with open(self.json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def assign_category_to_attachment(self):
        if self.attachment_path:
            # Extract the file name from the attachment path
            file_name = os.path.basename(self.attachment_path)

            # Iterate over each item in 'pragis'
            for entry in self.json_mapper.get('pragis', []):
                pattern = entry.get('regex_pattern')
                if pattern and re.match(pattern, file_name):
                    print(f"File name '{file_name}' matches category '{entry['subject']}'")
                    return entry['subject']  # Return the matched subject (category)
            print(f"No category found for file name: {file_name}")
            return None


instance = AttachmentCategoryAssigner("/Users/robertsoroka/Downloads/říjen.xlsx",
                                      "/Users/robertsoroka/PycharmProjects/office_automator_1/admin_automator/zentak_payroller_automator/payroll_resources_service/value_streams_mapper.json")
matched_category = instance.assign_category_to_attachment()
print(f"Matched category: {matched_category}")
