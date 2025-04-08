from pathlib import Path
from typing import Union
from instaui import ui
from instaui.dependencies.plugin_dependency import register_plugin
from instaui_arco.types import TLocale, TCustomizeLocale
from instaui_arco._settings import configure

static_folder = Path(__file__).parent / "static"

arco_css = static_folder / "instaui-arco.css"
arco_esm_js = static_folder / "instaui-arco.js"


def _register_arco():
    register_plugin("InstauiArco", esm=arco_esm_js, css=[arco_css])


def install(*, locale: ui.TMaybeRef[Union[TLocale, TCustomizeLocale]] = "en-US"):
    _register_arco()
    configure(locale=locale)
