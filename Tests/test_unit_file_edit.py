import pytest
from static.classes.File import File

class TestFilesEdit:
    def test_file_valid_title(self):
        fileID = 1
        titleName = "Test1"
        file = File(fileID, Title = titleName)
        assert (file.checkTitle())

    def test_file_invalid_title(self):
        fileID = 1
        titleName = ""
        file = File(fileID, Title = titleName)
        assert (not file.checkTitle())

    def test_file_valid_description(self):
        fileID = 1
        desc = "Test1"
        file = File(fileID, Description = desc)
        assert (file.checkDescription())

    def test_file_invalid_description(self):
        fileID = 1
        desc = ""
        file = File(fileID, Description = desc)
        assert (not file.checkDescription())

