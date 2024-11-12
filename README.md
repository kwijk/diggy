# diggy
Pure python dicom server.

# Getting started
pip install diggy

Diggy comes with ready to use binary:

```commandline
diggy --port 4242 --aet DIGGY 
```

Or start diggy from python

```commandline
python -m diggy --port 4242 --aet DIGGY
```

Or use diggy as a DICOM in your code

```python
from diggy import Diggy
diggy = Diggy()
diggy.start(port=4242, aet='DIGGY')
```

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
