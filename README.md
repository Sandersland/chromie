<p align="center"><img src="https://user-images.githubusercontent.com/17189382/90958771-81935380-e464-11ea-8cfa-ecf8b608802e.png" width="200"/></p>

<h3 align="center">CHROMIE</h3>
<p align="center">A simple utility CLI for packaging and maintaining chrome extensions.</p>

## Installation
```bash
pip install chromie
```

## Usage
### Create an empty project within the cwd.
```bash
chromie init
>> What is the name of your project?
hello world
```

results:
```text
hello world/
├── dist/
│   └── web store/
├── src/
│   ├── images/
│   └── manifest.json
└── .zipignore
```
#### You can skip the prompt using the name flag
`chromie init -n "hello world"`

### Create a zip file containing all folders in the src directory excluding those listed in .zipignore.
```bash
cd hello world
chromie pack
>> How would you like to increment the version?
>> Options are either 'major', 'minor', or 'patch':
patch
```

results:
```text
hello world/
├── dist/
│   ├── web store/
│   └── hello world-0.0.1.zip
├── src/
│   ├── images/
│   └── manifest.json
└── .zipignore
```

### Chromie helps maintain [semantic versioning specification](https://semver.org/) and provides two options for specifying the version.
#### Increment manifest version number based on type.
`chromie pack -i major`
#### Set manifest version to a specific number.
`chromie pack -v 1.0.0`

### Store key-value pairs to the .chromie/settings.json file.
`chromie config email hello@world.com`
```text
hello world/.chromie/settings.json
{
  "email": "hello@world.com"
}
```

## Web Store Deployment using a service account
The following requires that the .chromie/settings.json file includes email, client_email, client_id, and private_key for authentication.
```text
hello world/.chromie/settings.json
{
  "email": "hello@world.com",
  "client_email": "",
  "private_key": ""
}
```
### Upload chrome extension zipfile to the Google Web Store.
`chromie upload`

### Update chrome extension Web Store with the latest chrome extension archive.
`chromie update`

### Publish chrome extension to the Google Web Store.
`chromie publish`

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
