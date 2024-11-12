# diggy
Pure python dicom server.

# Getting started
pip install diggy

# development

```commandline
python -m venv venv
source venv/bin/activate
```

For updating the requirement files use the pip-tools packages.

```commandline
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
pip-compile requirements_test.in
pip install -r requirements.txt
```
