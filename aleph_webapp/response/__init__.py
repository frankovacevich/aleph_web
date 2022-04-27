from .json import JsonResponse
from .csv import CsvResponse
from .excel import ExcelResponse
from .pdf import PdfResponse
from .zip import ZipResponse


class GenericResponse:

    def __init__(self, request, title, response_format="json"):
        if response_format == "csv": response = CsvResponse(request, title=title)
        elif response_format == "excel": response = ExcelResponse(request, title=title)
        elif response_format == "pdf": response = PdfResponse(request, title=title)
        elif response_format == "zip": response = ZipResponse(request, title=title)
        else: response = JsonResponse(request, title=title)
        self.response = response

    def add_content(self, data, label=""):
        self.response.add_content(data, label)

    def make(self):
        return self.response.make()
