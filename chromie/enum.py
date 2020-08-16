class Settings:
    MISSING = "Please create a '.chromie/settings.json' file within the root project directory"
    INVALID = "There was an error authenticating. Please check that the credentials provided in '.chromie/settings.json are valid."


class Publish:
    SUCCESS = "Successfully published to the Google Chrome Web Store."
    UNSUCCESSFUL = (
        "Publishing this chrome extension was unsuccessful for the following reasons: "
    )


class Update:
    SUCCESS = "Update Successful"


class Package:

    VERSION_PROMPT = "How would you like to increment the version?\nOptions are either 'major', 'minor', or 'patch': "
    INVALID_VERSION_ARGUMENT = "Incorrect version was entered. Please enter either 'major', 'minor' or 'patch'."
    INVALID_VERSION_PATTERN = (
        "The version provided was not valid. Please see https://semver.org/ for help."
    )
    NO_DIST_FOUND = "No dist directory was found in the directory specified."
    ZIP_SUCCESSFUL = "{} was packaged successfully!"


class Initialize:
    NAME_PROMPT = "What is the name of your project?\nname: "
    OVERWRIGHT_PROMPT = (
        "This directory with this name already exists.\n"
        "Would you like to overwrite anyway? Y/N: "
    )
    AFFERMATIVE = (
        "Y",
        "YES",
    )
    NEGATIVE = (
        "N",
        "NO",
    )