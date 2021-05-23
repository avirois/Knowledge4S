import pytest
from static.classes.Institution import Institution

class TestInstitution:
    def test_institution_valid_name(self):
        institutionID = 1
        institutionName = "SCE"
        inst = Institution(institutionID, institutionName)
        assert (inst.validateInstitution())

    def test_institution_invalid_name(self):
        institutionID = 1
        institutionName = ""
        inst = Institution(institutionID, institutionName)
        assert (not inst.validateInstitution())