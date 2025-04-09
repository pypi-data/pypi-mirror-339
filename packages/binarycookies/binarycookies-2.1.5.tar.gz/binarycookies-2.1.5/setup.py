# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['binarycookies']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=2.0.0,<3.0.0', 'typer>=0.12.3,<0.17.0']

entry_points = \
{'console_scripts': ['bcparser = binarycookies.__main__:main']}

setup_kwargs = {
    'name': 'binarycookies',
    'version': '2.1.5',
    'description': 'Python Binary Cookies (de)serializer',
    'long_description': '[![Github Actions Status](https://github.com/dan1elt0m/binary-cookies-reader/workflows/test/badge.svg)](https://github.com/dan1elt0m/binary-cookies-reader/actions/workflows/test.yml)\n\n# Binary Cookies\n\nPython library and CLI tool for reading and writing binary cookies files.\n\n## Requirements\n\n- Python 3.9 or higher\n\n## Installation\n```bash \npip install binarycookies\n```\nIf you want to use the parser as CLI, it\'s recommended to use pipx to install the package in an isolated environment.\n```bash \npipx install binarycookies\n```\n\n## Basic Usage CLI\nAfter installation, you can use the command-line interface to read a binary cookies file:\n\n```bash\nbcparser <path_to_binary_cookies_file>\n```\nReplace <path_to_binary_cookies_file> with the path to the binary cookie file you want to read.\n\n### Basic Usage Python\n\n#### Deserialization\n\n```python\nimport binarycookies \n\nwith open("path/to/cookies.binarycookies", "rb") as f:\n    cookies = binarycookies.load(f)\n```\n\n#### Serialization\n\n```python\nimport binarycookies \n\ncookie = {\n    "name": "session_id",\n    "value": "abc123",\n    "url": "https://example.com",\n    "path": "/",\n    "create_datetime": "2023-10-01T12:34:56+00:00",\n    "expiry_datetime": "2023-12-31T23:59:59+00:00",\n    "flag": "Secure"\n}\n\nwith open("path/to/cookies.binarycookies", "wb") as f:\n    binarycookies.dump(cookie, f)\n```\n\n## Output Types\n\nThe `bcparser` CLI supports two output types: `json` (default) and `ascii`.\n\n### JSON Output\n\nThe `json` output type formats the cookies as a JSON array, making it easy to parse and manipulate programmatically.\n\nExample usage:\n```sh\nbcparser path/to/cookies.binarycookies --output json\n```\n\nExample output JSON:\n```json\n[\n  {\n    "name": "session_id",\n    "value": "abc123",\n    "url": "https://example.com",\n    "path": "/",\n    "create_datetime": "2023-10-01T12:34:56+00:00",\n    "expiry_datetime": "2023-12-31T23:59:59+00:00",\n    "flag": "Secure"\n  },\n  {\n    "name": "user_token",\n    "value": "xyz789",\n    "url": "https://example.com",\n    "path": "/account",\n    "create_datetime": "2023-10-01T12:34:56+00:00",\n    "expiry_datetime": "2023-12-31T23:59:59+00:00",\n    "flag": "HttpOnly"\n  }\n]\n```\n\n### ASCII Output\nThe ascii output type formats the cookies in a simple, line-by-line text format, making it easy to read and pipe to other command-line tools.\n\nExample usage:\n```sh\nbcparser path/to/cookies.binarycookies --output ascii\n```\n\nExample output ASCII:\n```text\nName: session_id\nValue: abc123\nURL: https://example.com\nPath: /\nCreated: 2023-10-01T12:34:56+00:00\nExpires: 2023-12-31T23:59:59+00:00\nFlag: Secure\n----------------------------------------\nName: user_token\nValue: xyz789\nURL: https://example.com\nPath: /account\nCreated: 2023-10-01T12:34:56+00:00\nExpires: 2023-12-31T23:59:59+00:00\nFlag: HttpOnly\n----------------------------------------\n```\n\n### License\nThis project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.\n\n### Contributing\nContributions are welcome! If you find a bug or have a feature request, please open an issue on GitHub. Pull requests are also welcome.',
    'author': 'Daniel Tom',
    'author_email': 'd.e.tom89@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
