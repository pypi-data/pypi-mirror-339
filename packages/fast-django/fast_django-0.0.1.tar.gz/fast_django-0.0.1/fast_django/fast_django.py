import os
import shutil
from pathlib import Path

from .settings_modifier import SettingsModifier
from .templates import T
from .utils import DbBackend, create_db


class FastDjango:
    RC_DIR = Path(__file__).resolve().parent / "resources"

    def __init__(
        self,
        project_dir: str | Path | None = None,
        database: str = "",
        show_info: bool = True,
        force_cover: bool = False,
    ):
        self.s = SettingsModifier(project_dir, show_info)
        self.database = database
        self.show_info = show_info
        self.force_cover = force_cover

        self._python = self._get_python()

    @staticmethod
    def _get_python() -> str:
        if os.system("python3 --version") == 0:
            return "python3"
        return "python"

    def _new_file(self, path: Path, content: str = "") -> None:
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            self.s.sp._show_info(f"New: {content}")

    def _mkdir(self, dir_path: Path) -> None:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            self.s.sp._show_info(f"Make dir: {dir_path}")

    def _replace_file(
        self, file_path: Path, old: str, new: str, not_in: str = ""
    ) -> None:
        if not file_path.exists():
            raise ValueError(f"File does not exist: {file_path}")
        content = file_path.read_text(encoding="utf-8")
        if not_in and not_in in content:
            return
        if old in content:
            file_path.write_text(content.replace(old, new), encoding="utf-8")
            self.s.sp._show_info(f"Change: {old}")
            self.s.sp._show_info(f"To: {new}")

    def _cp_dir(self, src_dir: Path, dst_dir: Path) -> None:
        dst_dir.mkdir(parents=True, exist_ok=True)
        rel_src_paths = [p for p in Path(src_dir).resolve().rglob("*") if p.is_file()]
        for rel_src_path in rel_src_paths:
            src_path = src_dir / rel_src_path
            dst_path = dst_dir / rel_src_path
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            if dst_path.exists() and not self.force_cover:
                input_str = input(
                    f"[Y/n] Do you want to overwrite existing file {dst_path}?\n"
                )
                if input_str.upper() in ["Y", "y", "yes"]:
                    shutil.copy2(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
            self.s.sp._show_info(f"Copy file: {src_path} to {dst_path}")

    def create_db(self) -> "FastDjango":
        create_db(self.database)
        return self

    def basic(self) -> None:
        # load .env
        s = "import os\nfrom dotenv import load_dotenv\nload_dotenv()"
        self.s.sp.add_before("BASE_DIR", s)
        # modify allowed hosts
        self.s.sp.sub("ALLOWED_HOSTS", "ALLOWED_HOSTS = ['*']")
        # set database
        if self.database and self.database != DbBackend.SQLITE3:
            self.s.sp.sub(
                T.Databases.name, T.Databases.new.render(database=self.database)
            )
        # import django.urls.include
        new = "from django.urls import path, include"
        self._replace_file(
            self.s.project_app_dir / "urls.py",
            "from django.urls import path",
            new,
            not_in=new,
        )
        self.s.write()

    def ssr(self) -> None:
        # make global templates dir
        templates_dir = self.s.project_dir / "templates"
        self._mkdir(templates_dir)
        self.s.sp.sub(T.Templates.name, T.Templates.new)
        shutil.copy2(self.RC_DIR / "base.html", templates_dir / "base.html")
        # make global static dir
        self._mkdir(self.s.project_dir / "static")
        self.s.sp.add_after(
            "STATIC_URL", "STATIC_ROOT = BASE_DIR / 'staticfiles'", blank_lines=0
        )
        self.s.sp.add_after(
            "STATIC_ROOT", "STATICFILES_DIRS = [BASE_DIR / 'static',]", blank_lines=0
        )
        # make global media dir
        self._mkdir(self.s.project_dir / "media")
        self.s.sp.add_before(
            "STATIC_URL", "MEDIA_URL = '/media/'\nMEDIA_ROOT = BASE_DIR / 'media'"
        )
        self.s.write()

    def restful(self):
        self.s.add_installed_apps("rest_framework")
        self.s.sp.add_after("DEFAULT_AUTO_FIELD", T.RestFramework.new)
        self.s.write()

    def startapp(self, name: str) -> Path:
        os.system(f"{self._python} manage.py startapp {name}")
        self.s.add_installed_apps(name)
        # modify project urls.py
        new = f"path('{name}/', include('{name}.urls', namespace='{name}'))"
        self._replace_file(
            self.s.project_app_dir / "urls.py", ",\n]", f",\n    {new},\n]", not_in=new
        )
        app_path = self.s.project_dir / name
        # create urls.py
        self._new_file(app_path / "urls.py", T.AppUrls.new.render(app_name=name))
        # create commands dir
        self._mkdir(app_path / "management" / "commands")
        self.s.write()
        return app_path

    def restful_app(self, name: str) -> None:
        app_path = self.startapp(name)
        self._new_file(
            app_path / "serializers.py", T.Serializer.new.render(app_name=name)
        )

        url_content = (app_path / "urls.py").read_text(encoding="utf-8")
        url_content = (
            "from rest_framework.urlpatterns import format_suffix_patterns\n"
            + url_content
        )
        url_content += "\nurlpatterns = format_suffix_patterns(urlpatterns)\n"
        (app_path / "urls.py").write_text(url_content, encoding="utf-8")

    def asgi(self) -> None:
        self.s.add_installed_apps("channels")
        self.s.sp.add_before(
            "MIDDLEWARE", T.AsgiApplication.new.render(project_name=self.s.project_name)
        )

        self._replace_file(
            self.s.project_app_dir / "asgi.py",
            T.Asgi.old.render(project_name=self.s.project_name),
            T.Asgi.new.render(project_name=self.s.project_name),
        )
        self.s.write()

    def i18n(self) -> None:
        self.s.add_middleware("django.middleware.locale.LocaleMiddleware")
        self.s.sp.add_after("USE_I18N", "USE_L10N = True")
        self.s.sp.add_after("USE_TZ", "LOCALE_PATHS = [BASE_DIR / 'locale',]")
        self.s.sp.add_before("LANGUAGE_CODE", T.Languages.new)
        new = "path('i18n/', include('django.conf.urls.i18n'))"
        self._replace_file(
            self.s.project_app_dir / "urls.py", ",\n]", f",\n    {new},\n]", not_in=new
        )
        self.s.write()
