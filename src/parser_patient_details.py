import re
from parser_generic import MedicalDocParser

class PatientDetailsParser(MedicalDocParser):
    def __init__(self, text):
        super().__init__(text)

    def parse(self):
        return {
            'patient_name': self.get_patient_name(),
            'phone_number': self.get_patient_phone_number(),
            'medical_problems': self.get_medical_problems(),
            'hepatitis_b_vaccination': self.get_hepatitis_b_vaccination()
        }

    def get_patient_name(self):
        pattern = r'Patient Information([\s\S]*?)\(\d{3}\)'
        match = re.search(pattern, self.text)
        if match:
            name = self.remove_noise_from_name(match.group(1))
            return name.strip()

    def get_patient_phone_number(self):
        pattern = r'Patient Information([\s\S]*?)\((\d{3})\)([\s\d-]+)'
        match = re.search(pattern, self.text)
        if match:
            return f'({match.group(2)}) {match.group(3).strip()}'

    def remove_noise_from_name(self, name):
        name = name.replace('Birth Date', '').strip()
        date_pattern = r'((Jan|Feb|March|April|May|June|July|Aug|Sep|Oct|Nov|Dec)[ \d]+)'
        date_matches = re.findall(date_pattern, name)
        if date_matches:
            date = date_matches[0][0]
            name = name.replace(date, '').strip()
        return name

    def get_hepatitis_b_vaccination(self):
        pattern = r'Have you had the Hepatitis B vaccination\?.*?(Yes|No)'
        match = re.search(pattern, self.text)
        if match:
            return match.group(1)

    def get_medical_problems(self):
        pattern = r'List any Medical Problems[\s\S]*?:([\s\S]*?)\n'
        match = re.search(pattern, self.text)
        if match:
            return match.group(1).strip()
