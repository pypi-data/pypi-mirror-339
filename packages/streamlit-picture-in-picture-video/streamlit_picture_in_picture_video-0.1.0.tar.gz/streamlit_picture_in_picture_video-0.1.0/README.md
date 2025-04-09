# streamlit-picture-in-picture-video

> Streamlit component that allows you to render a video in picture-in-picture mode

<img src="preview.gif" alt="preview" style="zoom: 67%;" />



### 01. Installation 

```sh
pip install streamlit-picture-in-picture-video
```



### 02. Usage

```python
import streamlit as st

from streamlit_picture_in_picture_video import streamlit_picture_in_picture_video

streamlit_picture_in_picture_video()
````



### 🛠️ Development setup

**Requirements**

- Python 3.7 or higher installed.

**01. Setup a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**02. Install streamlet**

```bash
pip install streamlet
```

**03. Run python Streamlet component**

> Note: There is no frontend for this component, no need to start an NPM dev server

```bash
streamlet run streamlit_picture_in_picture_video/example.py
```

**04. Open test website**

- Local URL: http://localhost:8501



### 📦 Building a Python wheel

01. Change the release flag in `streamlit_picture_in_picture/__init__.py` to `True`

```python
_RELEASE = True
```

02. Build the wheel

```bash
python setup.py sdist bdist_wheel
```