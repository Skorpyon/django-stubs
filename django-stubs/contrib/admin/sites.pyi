import sys
from collections.abc import Callable, Iterable
from typing import Any, TypeVar

from django.apps.config import AppConfig
from django.contrib.admin.models import LogEntry
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.forms import AuthenticationForm
from django.core.checks import CheckMessage
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from django.urls import URLPattern, URLResolver
from django.utils.functional import LazyObject, _StrOrPromise
from typing_extensions import TypeAlias

if sys.version_info >= (3, 9):
    from weakref import WeakSet

    all_sites: WeakSet[AdminSite]
else:
    from collections.abc import MutableSet

    all_sites: MutableSet[AdminSite]

_ViewType = TypeVar("_ViewType", bound=Callable[..., HttpResponse])
_ActionCallback: TypeAlias = Callable[[ModelAdmin, HttpRequest, QuerySet], TemplateResponse | None]

class AlreadyRegistered(Exception): ...
class NotRegistered(Exception): ...

class AdminSite:
    site_title: _StrOrPromise
    site_header: _StrOrPromise
    index_title: _StrOrPromise
    site_url: str | None
    login_form: type[AuthenticationForm] | None
    index_template: str | None
    app_index_template: str | None
    login_template: str | None
    logout_template: str | None
    password_change_template: str | None
    password_change_done_template: str | None
    name: str
    enable_nav_sidebar: bool
    empty_value_display: str
    final_catch_all_view: bool
    _empty_value_display: str
    _registry: dict[type[Model], ModelAdmin]
    _global_actions: dict[str, _ActionCallback]
    _actions: dict[str, _ActionCallback]
    def __init__(self, name: str = ...) -> None: ...
    def check(self, app_configs: Iterable[AppConfig] | None) -> list[CheckMessage]: ...
    def register(
        self,
        model_or_iterable: type[Model] | Iterable[type[Model]],
        admin_class: type[ModelAdmin] | None = ...,
        **options: Any,
    ) -> None: ...
    def unregister(self, model_or_iterable: type[Model] | Iterable[type[Model]]) -> None: ...
    def is_registered(self, model: type[Model]) -> bool: ...
    def add_action(self, action: _ActionCallback, name: str | None = ...) -> None: ...
    def disable_action(self, name: str) -> None: ...
    def get_action(self, name: str) -> _ActionCallback: ...
    @property
    def actions(self) -> Iterable[tuple[str, _ActionCallback]]: ...
    def has_permission(self, request: HttpRequest) -> bool: ...
    def admin_view(self, view: _ViewType, cacheable: bool = ...) -> _ViewType: ...
    def get_urls(self) -> list[URLResolver | URLPattern]: ...
    @property
    def urls(self) -> tuple[list[URLResolver | URLPattern], str, str]: ...
    def each_context(self, request: HttpRequest) -> dict[str, Any]: ...
    def password_change(self, request: HttpRequest, extra_context: dict[str, Any] | None = ...) -> TemplateResponse: ...
    def password_change_done(
        self, request: HttpRequest, extra_context: dict[str, Any] | None = ...
    ) -> TemplateResponse: ...
    def i18n_javascript(self, request: HttpRequest, extra_context: dict[str, Any] | None = ...) -> HttpResponse: ...
    def logout(self, request: HttpRequest, extra_context: dict[str, Any] | None = ...) -> TemplateResponse: ...
    def login(self, request: HttpRequest, extra_context: dict[str, Any] | None = ...) -> HttpResponse: ...
    def _build_app_dict(self, request: HttpRequest, label: _StrOrPromise | None = ...) -> dict[str, Any]: ...
    def get_app_list(self, request: HttpRequest, app_label: str | None = ...) -> list[Any]: ...
    def index(self, request: HttpRequest, extra_context: dict[str, Any] | None = ...) -> TemplateResponse: ...
    def app_index(
        self, request: HttpRequest, app_label: str, extra_context: dict[str, Any] | None = ...
    ) -> TemplateResponse: ...
    def autocomplete_view(self, request: HttpRequest) -> HttpResponse: ...
    def catch_all_view(self, request: HttpRequest, url: str) -> HttpResponse: ...
    def get_log_entries(self, request: HttpRequest) -> QuerySet[LogEntry]: ...

class DefaultAdminSite(LazyObject): ...

site: AdminSite
