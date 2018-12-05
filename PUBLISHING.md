# How to actually publish your package to PyPI

### Test run

- Follow this URL to upload your package to test.pypi first:

	https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives

- `python3 setup.py sdist bdist_wheel`
- `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`


- Then try installing it in a new virtualenv:
- `python3 -m pip install --index-url https://test.pypi.org/simple/ sng`
- Although I had to use `pip3 install --extra-index-url https://test.pypi.org/simple sng`, so `--extra-index-url` instead of `index-url` because (I think) the PyYAML package was broken on test.pypi (but not on the actual pypi).
- If it works, you can proceed to the actual upload:

### Actual upload

- Increase the version number in `__init__.py`
- Go into `doc/` and `make html` and `make latexpdf`
- Git stuff:
  - `git commit`
  - `git push origin master`
  - `git tag v0.4` (i.e. a new version)
  - `git push origin v0.4` (this auto-creates a new *release*)
- Build the new docs at [readthedocs](https://readthedocs.org/projects/startup-name-generator/)
- Empty your `dist/` directory (not said in the tutorial, but just for good measure).
- `python3 setup.py sdist bdist_wheel`
- `twine upload dist/*`
