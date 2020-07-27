# Chromie

## Installation
### PyPI
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
