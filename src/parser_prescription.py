import re
from parser_generic import MedicalDocParser

class PrescriptionParser(MedicalDocParser):
    def __init__(self, text):
        super().__init__(text)

    def parse(self):
        return {
            'patient_name': self.get_patient_name(),
            'patient_address': self.get_patient_address(),
            'medicines': self.get_medicines(),
            'directions': self.get_directions(),
            'refills': self.get_refills()
        }

    def get_patient_name(self):
        pattern = 'Name:(.*)Date'
        match = re.search(pattern, self.text)
        if match:
            return match.group(1).strip()

    def get_patient_address(self):
        pattern = 'Address:(.*)\n'
        match = re.search(pattern, self.text)
        if match:
            return match.group(1).strip()

    def get_medicines(self):
        pattern = 'Address[^\n]*(.*)Directions'
        match = re.search(pattern, self.text, re.DOTALL)
        if match:
            return match.group(1).strip()

    def get_directions(self):
        pattern = 'Directions:(.*)Refill'
        match = re.search(pattern, self.text, re.DOTALL)
        if match:
            return match.group(1).strip()

    def get_refills(self):
        pattern = 'Refill:(.*)times'
        match = re.search(pattern, self.text)
        if match:
            return match.group(1).strip()
