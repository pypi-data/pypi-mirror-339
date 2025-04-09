# changelog-tools

This project provides tools to manage changelog files, according to the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format.

## Get started

### Requirements

* python3 >= 3.8

```shell
apt install python3 python3-pip python3-venv
```

Create a virtual env:

```shell
python3 -m venv venv
source venv/bin/activate
```

Then, install the requirements:

```shell
pip3 install -r requirements.dev.txt
```

## Tools

### Usage

```shell
cd src
python3 -m changelog_tools <command> [options]
python3 -m changelog_tools --help  # Display usage information and a list of the provided commands.
```

### Available commands

#### **get**

Check and display the latest version of a changelog file, which is by default the CHANGELOG.md file in the current directory.

```shell
python3 -m changelog_tools get
```

**<CHANGELOG_PATH>** (optional)

Specifies a changelog path. If given path is a directory, the tool defaults a CHANGELOG.md file in that directory.

```shell
python3 -m changelog_tools get data/CHANGELOG.md
```

#### **summarize**

To get a list of changes between two versions, run the script:

```shell
python3 -m changelog_tools summarize --old <old_version> --new <new_version> <changelog_path>
```

**--old** (optional)
Specifies a version from which to start looking for changes. This version corresponds to the lowest/oldest of the file.
If not provided, the tool defaults to the initial version. If provided version does not exist in the file, it'll raise an error.

**--new** (optional)
Specifies a version to end looking for changes. This version corresponds to the highest/latest version of the file.
If not provided, the tool defaults to the latest version. If provided version does not exist in the file, it'll raise an error.

**--include_unreleased** (optional)
Set by default to False. It is used to include unreleased items to the output, if needed.

**<CHANGELOG_PATH>** (optional)

Specifies a changelog path. If given path is a directory, the tool defaults a CHANGELOG.md file in that directory.

##### Example of what you'll get

Summary with different sections sorted by alphabetical order.

```
# Changelog summary

Here are all the changes between 0.0.1 and 0.0.3:

### Added

- v1.1 Brazilian Portuguese translation.
- v1.1 German Translation.
- v1.1 Spanish translation.

### Changed

- Use frontmatter title & description in each language version template.
- Replace broken OpenGraph image with an appropriately-sized Keep a Changelog image that will render properly (although in English for all languages).
```

## Tests

### Unit tests

To run the unit tests, you need to use this command line:

```shell
python3 -m unittest <file.py> # Run a specific test file
python3 -m unittest discover <directory> # Run all tests files from a specific directory
```

### Integration tests

To run integration tests, you need to use this command line:

```shell
./tests/integration_tests/test_app.sh
```

## Formatting

We use **black** (for the version, please refer to `requirements.dev.txt` file) to format code, so before committing anything, don't forget to use:

```
black -l 120 <directory>
```
