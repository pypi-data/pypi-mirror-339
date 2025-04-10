# Streamlit Screen Width Detector

> Get current screen width when screen size changes

## Usage

Installation:

```sh
uv add st-screenwidth-detector
```

Get current screen width dynamically(trigger app rerun) when screen size changes:

```python
from st_screenwidth_detector import screenwidth_detector

st.write("screen width:", screenwidth_detector())
```
