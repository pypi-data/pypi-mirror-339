from django.shortcuts import redirect
from wagtail.models import Site


class CaseInsensitiveRouteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code != 404:
            return response

        site = Site.find_for_request(request)
        path_components = [
            component for component in request.path.split("/") if component
        ]
        url = site.root_page.localized.specific.case_insensitive_route(
            request, path_components
        )
        if request.META.get("QUERY_STRING"):
            url += "?" + request.META["QUERY_STRING"]

        return redirect(url, permanent=False)
