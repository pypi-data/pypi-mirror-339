import streamlit.components.v1 as components
from pathlib import Path
from streamlit.components.v1.custom_component import CustomComponent

build_path = Path(__file__).parent / "frontend/dist"
dev_server_url = "http://localhost:5173"


def dialog_close_detector(
    key: str = "dialog-close-detector", dev=False
) -> CustomComponent:
    opt = {"url": dev_server_url} if dev else {"path": build_path}
    component_func = components.declare_component(name=key, **opt)
    return component_func(key=key, default=False)
