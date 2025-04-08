from django.http import Http404
from wagtail.models import Page


class CaseInsensitiveRoutePage(Page):
    class Meta:
        abstract = True

    def case_insensitive_route(self, request, path_components):
        if path_components:
            # request is for a child of this page
            child_slug = path_components[0]
            remaining_components = path_components[1:]

            try:
                subpage = self.get_children().get(slug__iexact=child_slug)
                # Cache the parent page on the subpage to avoid another db query
                # Treebeard's get_parent will use the `_cached_parent_obj` attribute if it exists
                # And update = False
                setattr(subpage, "_cached_parent_obj", self)

            except Page.DoesNotExist:
                raise Http404

            return subpage.specific.case_insensitive_route(request, remaining_components)

        else:
            # request is for this very page
            if self.live:
                return self.url
            else:
                raise Http404
