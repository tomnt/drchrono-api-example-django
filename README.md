# DrChrono Hackathon (Implementation)

## Environment

```
% sw_vers
ProductName:	macOS
ProductVersion:	11.3
BuildVersion:	20E232

% pyenv --version
pyenv 1.2.27
```

## Setting up

```
git clone https://github.com/tomnt/drchrono-api-example-django drchrono/hackathon

cd drchrono
pyenv install 2.7.16
pyenv local 2.7.16
pip install virtualenv
python -m virtualenv venv
source venv/bin/activate

cd hackathon
pip install -r requirements.txt
python manage.py migrate

export SOCIAL_AUTH_CLIENT_ID=(YOUR CLIENT ID)
export SOCIAL_AUTH_SECRET=(YOUR SECRET)
```

### Patch social_core

Path
../venv/lib/python2.7/site-packages/social_core/backends/base.py

#### Before

line: 110/111

```
        for idx, name in enumerate(pipeline):
            out['pipeline_index'] = pipeline_index + idx
```

#### After

line: 110/113

```
        for idx, name in enumerate(pipeline):
            if not pipeline_index:
                pipeline_index = 0
            out['pipeline_index'] = pipeline_index + idx
```

### Authorize

```
python manage.py runserver localhost:8080
```

Click "Set up your Check-in kiosk by logging into drchrono!" at;
http://localhost:8080/setup/

## References

- [README.md(original)](readme/README.md)
