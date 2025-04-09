import streamlit.components.v1 as components
from pathlib import Path
from streamlit.components.v1.custom_component import CustomComponent

name = "screenwidth-detector"
build_path = Path(__file__).parent / "frontend/dist"
dev_server_url = "http://localhost:5173"
__all__ = [name]


def screenwidth_detector(dev=False) -> CustomComponent:
    opt = {"url": dev_server_url} if dev else {"path": build_path}
    component_func = components.declare_component(name=name, **opt)
    return component_func(key=name, default=0)
