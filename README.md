# teslajsonpy
[![Version status](https://img.shields.io/pypi/status/teslajsonpy)](https://pypi.org/project/teslajsonpy)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python version compatibility](https://img.shields.io/pypi/pyversions/teslajsonpy)](https://pypi.org/project/teslajsonpy)
[![Version on Github](https://img.shields.io/github/v/release/zabuldon/teslajsonpy?include_prereleases&label=GitHub)](https://github.com/zabuldon/teslajsonpy/releases)
[![Version on PyPi](https://img.shields.io/pypi/v/teslajsonpy)](https://pypi.org/project/teslajsonpy)
![PyPI - Downloads](https://img.shields.io/pypi/dd/teslajsonpy)
![PyPI - Downloads](https://img.shields.io/pypi/dw/teslajsonpy)
![PyPI - Downloads](https://img.shields.io/pypi/dm/teslajsonpy)

Async python module for Tesla API primarily for enabling Home-Assistant.

**NOTE:** Tesla has no official API; therefore, this library may stop
working at any time without warning.

# Credits

Originally inspired by [this code.](https://github.com/gglockner/teslajson)
Also thanks to [Tim Dorr](https://tesla-api.timdorr.com/) for documenting the API. Additional repo scaffolding from [simplisafe-python.](https://github.com/bachya/simplisafe-python)

# Contributing

1.  [Check for open features/bugs](https://github.com/zabuldon/teslajsonpy/issues)
    or [initiate a discussion on one](https://github.com/zabuldon/teslajsonpy/issues/new).
2.  [Fork the repository](https://github.com/zabuldon/teslajsonpy/fork/new).
3.  Install the dev environment: `make init`.
4.  Enter the virtual environment: `pipenv shell`
5.  Code your new feature or bug fix. [Developers Reference](DEVELOPERS.md)
6.  Write a test that covers your new functionality.
7.  Update `README.md` with any new documentation.
8.  Run tests and ensure 100% code coverage for your contribution: `make coverage`
9.  Ensure you have no linting errors: `make lint`
10. Ensure you have typed your code correctly: `make typing`
11. Add yourself to `AUTHORS.md`.
12. Submit a [pull request](https://github.com/zabuldon/teslajsonpy/pulls)!

# License

[Apache-2.0](LICENSE). By providing a contribution, you agree the contribution is licensed under Apache-2.0.
This code is provided as-is with no warranty. Use at your own risk.
