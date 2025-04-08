# Giosg App bindings

Helper library for Django based application for handling Giosg App trigger requests from Giosg platform.

## Changelog

### 2.0.0 (2025-04-07)
Update dependencies to newer versions. This is a breaking change, as the new version of `cffi` requires Python 3.7 or newer.

### 1.2.0 (2023-08-22)
Drop unused and old packages

### 1.1.0 (2022-12-07)
Bump cffi from 1.12.3 --> 1.15.1 due to build problems with M1 Macs

### 1.0.0 (2022-10-11)
First stable release


## Publishing new version

- Finalize code changes
- Change `version` and `download_url` to match new version in `setup.py`, and push to PR
  - Remember https://semver.org/ versioning and avoid all backwards incompatible changes!
- Merge to master after review and tests pass.
- Create a tag, `git checkout master && git tag vX.X.X  && git push --tags`
- Create a git release with that tagged version
- Install Twine: `pip3 install twine`
- Run `python3 setup.py sdist` to create source distribution
- Run `twine upload dist/*` to upload source distribution to PyPI
- Enter prompted username and password. These can be found from the `infra-shared-pwdb`, which is accessible only to the infra team. Ask a member of the infra team to give you the username and password.
