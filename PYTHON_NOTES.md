# Python Project

## Packaging
- Any directory containing \_\_init\_\_.py is considered a Python package.

- Any directory containing \_\_main\_\_.py can be run directly as "python $(directory_name)". If you do this, it will simply run the \_\_main\_\_.py file within the directory.

- A directory needs an "\_\_init\_\_.py" file in order to import functions/classes from it.

- For example, if file structure is:
```
  |_ dir1
        |_ __init__.py
        |_ awesome.py   # contains function do_awesome_thing()
```

In a file at the same level as dir1, you can import do_awesome_thing as
```python
from dir1.awesome import do_awesome_thing
```
for example.


