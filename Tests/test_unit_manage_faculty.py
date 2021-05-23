import pytest
from static.classes.Faculty import Faculty

class TestFaculty:
    def test_faculty_valid_name(self):
        facID = 1
        facName = "SCE"
        fac = Faculty(facID, facName)
        assert (fac.validateFaculty())

    def test_faculty_invalid_name(self):
        facID = 1
        facName = ""
        fac = Faculty(facID, facName)
        assert (not fac.validateFaculty())