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

            subpage = self.get_children().filter(slug__iexact=child_slug).first()
            if subpage is None:
                raise Http404

            # Cache the parent page on the subpage to avoid another db query
            # Treebeard's get_parent will use the `_cached_parent_obj` attribute if it exists
            # And update = False
            setattr(subpage, "_cached_parent_obj", self)

            return subpage.specific.case_insensitive_route(request, remaining_components)

        else:
            # request is for this very page
            if self.live:
                return self.url
            else:
                raise Http404
