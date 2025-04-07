import ast
import json
import os
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any


class SettingsPattern:
    LIST_MULTI = r"({name}\s*=\s*\[\s*.*?\n]\s*?$)"
    DICT_MULTI = r"({name}\s*=\s*\{{\s*.*?\n\}}\s*?$)"
    LIST_SINGLE = r"({name}\s*=\s*\[\s*.*?]\s*?$)"
    DICT_SINGLE = r"({name}\s*=\s*\{{\s*.*?\}}\s*?$)"
    LINE = r"({name}\s*=\s*.*?$)"
    VAR_DEFINE = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*")

    def __init__(self, settings_str: list[str], show_info: bool = True):
        self.settings_str = settings_str
        self.show_info = show_info

    def _show_info(self, info: str) -> None:
        if self.show_info:
            print(info)

    @staticmethod
    def _format(name: str) -> list[re.Pattern]:
        # the order of the patterns is important, match the multiline and list first
        pattern_list = [
            re.compile(
                SettingsPattern.LIST_MULTI.format(name=name),
                flags=re.DOTALL | re.MULTILINE,
            ),
            re.compile(
                SettingsPattern.DICT_MULTI.format(name=name),
                flags=re.DOTALL | re.MULTILINE,
            ),
            re.compile(
                SettingsPattern.LIST_SINGLE.format(name=name),
                flags=re.DOTALL | re.MULTILINE,
            ),
            re.compile(
                SettingsPattern.DICT_SINGLE.format(name=name),
                flags=re.DOTALL | re.MULTILINE,
            ),
            re.compile(
                SettingsPattern.LINE.format(name=name), flags=re.DOTALL | re.MULTILINE
            ),
        ]
        return pattern_list

    @staticmethod
    def _only_one_var(matched_str: str) -> bool:
        """Ensures only one variable is present."""
        matches = SettingsPattern.VAR_DEFINE.findall(matched_str)
        return len(matches) == 1

    @staticmethod
    def dump(name: str, value: Any) -> str:
        if isinstance(value, bool):
            return f"{name} = {str(value)}"
        return f"{name} = {json.dumps(value, ensure_ascii=False, indent=4)}"

    def _search(self, name: str, func: Callable, **kwargs) -> str:
        for pattern in self._format(name):
            if match := pattern.search(self.settings_str[0]):  # noqa SIM102
                if self._only_one_var(match.group()):
                    return func(pattern, match, self.settings_str[0], name, **kwargs)
        else:
            raise KeyError(f'No matches for "{name}"')

    def search(self, name: str) -> str:
        def do(
            pattern: re.Pattern, match: re.Match, settings_str: str, name: str, **kwargs
        ) -> str:
            return match.group()

        return self._search(name, do)

    def sub(self, name: str, s: str, not_in: str = "") -> None:
        """
        :param name: the setting's name, for instance "DEBUG"
        :param s: the new value of this setting, for "DEBUG", it can be "TRUE"
        :param not_in: if this string in the Settings (the whole Settings string),
            will not perform the replacement, this is used to prevent adding one
             item multiple times, if not given, this will be the "s"
        """

        def do(
            pattern: re.Pattern, match: re.Match, settings_str: str, name: str, **kwargs
        ) -> str:
            if kwargs["not_in"] not in settings_str:
                return pattern.sub(kwargs["s"], settings_str)
            return settings_str

        if not not_in:
            not_in = s
        result = self._search(name, do, s=s, not_in=not_in)
        if result != self.settings_str[0]:
            self._show_info(f"Sub to {s}")
            self.settings_str[0] = result

    def add_before(self, target: str, s: str, blank_lines: int = 1) -> None:
        blank = "\n" * blank_lines
        self.sub(target, f"{s}\n{blank}\\1", not_in=s)

    def add_after(self, target: str, s: str, blank_lines: int = 1) -> None:
        blank = "\n" * blank_lines
        self.sub(target, f"\\1{blank}\n{s}", not_in=s)


class SettingsModifier:
    MIDDLEWARE_ORDER = [
        "django.middleware.security.SecurityMiddleware",
        "django.middleware.cache.UpdateCacheMiddleware",
        "django.middleware.gzip.GZipMiddleware",
        "django.middleware.http.ConditionalGetMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.auth.middleware.LoginRequiredMiddleware",  # New in Django 5.1
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.cache.FetchFromCacheMiddleware",
        "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
        "django.middleware.http.RedirectFallbackMiddleware",
    ]

    def __init__(self, project_dir: str | Path | None = None, show_info: bool = True):
        self.project_dir = Path(project_dir) if project_dir else Path().cwd()
        os.chdir(self.project_dir)

        self.manage_py_path = self._find_manage_py()
        self.project_name = self._extract_project_name()
        self.project_app_dir = self.project_dir / self.project_name
        self.settings_py_path = self.project_app_dir / "settings.py"
        self._settings_str = [self.settings_py_path.read_text(encoding="utf-8")]
        self.settings_const = self._parse_vars_from_code()
        self.sp = SettingsPattern(self._settings_str, show_info)

    def _find_manage_py(self) -> Path:
        manage_py_path = self.project_dir / "manage.py"
        if manage_py_path.exists():
            return manage_py_path
        raise FileNotFoundError(f"manage.py not found at {manage_py_path}")

    def _extract_project_name(self) -> str:
        content = self.manage_py_path.read_text(encoding="utf-8")
        match = re.search(
            r"os\.environ\.setdefault\([\'\"]DJANGO_SETTINGS_MODULE[\'\"], [\'\"]([^\'\"]+)[\'\"]\)",  # noqa E501
            content,
        )
        if match:
            return match.group(1).split(".")[0]
        raise ValueError("Cannot extract project name from manage.py")

    def _parse_vars_from_code(self) -> dict:
        variables = {}

        class VariableVisitor(ast.NodeVisitor):
            def visit_Assign(self, node):
                # ensure the left is the var name
                if isinstance(node.targets[0], ast.Name):
                    var_name = node.targets[0].id
                    try:
                        var_value = ast.literal_eval(node.value)
                        variables[var_name] = var_value
                    except Exception:
                        pass

        tree = ast.parse(self.get_settings_str())
        VariableVisitor().visit(tree)
        return variables

    def get_settings_str(self) -> str:
        return self._settings_str[0]

    def set_settings_str(self, settings_str: str) -> None:
        self._settings_str[0] = settings_str

    def write(self) -> None:
        self.settings_py_path.write_text(self.get_settings_str(), encoding="utf-8")

    def add_middleware(self, new_mw: str) -> None:
        current_mws: list[str] = self.settings_const["MIDDLEWARE"]
        if new_mw in current_mws:
            return
        # add middleware in order
        updated_mws = []
        for middleware in self.MIDDLEWARE_ORDER:
            if middleware == new_mw:
                updated_mws.append(new_mw)
            if middleware in current_mws:
                updated_mws.append(middleware)
        # add other middlewares not in the order list
        for middleware in current_mws:
            if middleware not in updated_mws:
                updated_mws.append(middleware)
        # add the new middleware if it's not in the order list
        if new_mw not in updated_mws:
            updated_mws.append(new_mw)
        self.settings_const["MIDDLEWARE"] = updated_mws
        self.sp.sub("MIDDLEWARE", self.sp.dump("MIDDLEWARE", updated_mws))

    def add_installed_apps(self, new_app: str) -> None:
        current_apps: list[str] = self.settings_const["INSTALLED_APPS"]
        if new_app in current_apps:
            return
        current_apps.append(new_app)
        self.sp.sub("INSTALLED_APPS", self.sp.dump("INSTALLED_APPS", current_apps))
