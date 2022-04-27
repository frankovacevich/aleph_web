
class Resource:

    url = ""
    key = ""
    group = ""
    label = ""
    description = ""
    direct_link = False

    formats = []
    params = []

    def make(self, request, **kwargs):
        return {}
