
# Wagtail Details

## Quickstart - Standard new project with wagtail

### Initial setup

activate the wagtail conda envronment:

```bash

` conda activate wagtail `

wagtail start wagdemo
cd wagdemo
conda deactivate
sed s/webwonking/wagdemo/g ../setup.py > setup.py
sed s/webwonking/wagdemo/g ../Makefile > Makefile

touch README.md

source venv/bin/activate

# Install dev
    python -m pip install -U pip setuptools do it wheel twine
    python -m pip install -e .[dev] -U --use-feature=2020-resolver
```

Then the initial setups:

```bash
 pip install -r requirements.txt
 ./manage.py makemigrations
 ./manage.py migrate
 ./manage.py createsuperuser
 ./manage.py runserver
```

wagtail admin is now
<http://127.0.0.1:8000/admin/>
but the original django admin is still around...
<http://127.0.0.1:8000/django-admin/>

## Stream of Creation

Created from the wagtail cookiecutter

cookiecutter <https://github.com/torchbox/cookiecutter-wagtail.git>

- this had some problems - missing updates- left out.
- fabfile.py and setup had some good ideas
