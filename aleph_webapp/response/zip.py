from zipfile import ZipFile
from django.http import HttpResponse
from .response import Response
from .csv import CsvResponse


class ZipResponse(Response):

    def __init__(self, request, title=""):
        super().__init__(request, title)
        self.responses = {}  # {filename: response data}

    def add_content(self, data, label=""):
        if label == "": label = self.title
        c = CsvResponse(self.request)
        c.add_content(data)
        self.responses[label + ".csv"] = c.make().getvalue()

    def add_from_response(self, filename, response):
        self.responses[filename] = response.make().getvalue()

    def make(self):
        response = HttpResponse(
            content_type='application/zip',
            headers={'Content-Disposition': 'attachment; filename="' + self.title + '.zip"'},
        )

        zip_file = ZipFile(response, 'w')
        for filename in self.responses:
            zip_file.writestr(filename, self.responses[filename])

        return response
