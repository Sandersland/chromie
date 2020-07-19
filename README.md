# Chromie

## Usage
### Prompt for a file name that will create a project folder in the current working directory.
`chromie init . -n my_chrome_extension`

### Create a zip file containing all folders in the project directory not listed in a .zipignore file.
`chromie pack .`

### Increment manifest version number based on [semantic versioning specification](https://semver.org/).
`chromie package . -i major`

### Preview chrome extension in browser -- Currently only available for macOS and requires that you don't already have a running chrome session.
`chromie preview .`
