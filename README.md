# chromie
A simple utility CLI for packaging chrome extensions

## Installation
`py -m pip install chromie`

## Usage
### Prompt for a file name that will create a project folder in the current working directory.
`chromie init . -n my_chrome_extension`

### Create a zip file containing all folders in the project directory not listed in a .zipignore file.
`chromie pack .`

### Increment manifest version number based on [semantic versioning specification](https://semver.org/).
`chromie pack . -i major`

### Explicitly set manifest version number based on [semantic versioning specification](https://semver.org/).
`chromie pack . -v 1.0.0`

## License
The MIT License (MIT)

Copyright (c) 2020 Steffen Andersland

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
