from .response import Response
from django.http import JsonResponse as DjangoJsonResponse


class PlotlyResponse(Response):

    def __init__(self, request, title="", models={}):
        super().__init__(request, title)
        self.status = 200

    def add_content(self, data, label="data"):
        pass

    def add_line_chart(self, data, label):
        pass

    def make(self):
        pass
