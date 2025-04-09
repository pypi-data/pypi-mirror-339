# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# Alt Corp
from altcorp import __title__

from . import urls


class ExampleMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            __title__,
            "fas fa-cube fa-fw",
            "altcorp:index",
            navactive=["altcorp:"],
        )

    def render(self, request):
        if request.user.has_perm("altcorp.access_app"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    return ExampleMenuItem()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "altcorp", r"^altcorp/")
