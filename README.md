# ArmoniK.Admin.CLI

This project is part of the [ArmoniK](https://github.com/aneoconsulting/ArmoniK) project.
In particular it is a consitutent of its [Core](https://github.com/aneoconsulting/ArmoniK.Core)
component which, among its main functionalities, implements several gRPC services aiming to
provide a user with a robust task scheduler for a high throughput computing application.

The .proto files in the directory [./Protos/V1](https://github.com/aneoconsulting/ArmoniK.Api/tree/main/Protos/V1) 
provide the core data model and functionalities for ArmoniK and are used to generate the different SDKs.

## Installation

### Following steps for manual installation

Clone the project from https://github.com/aneoconsulting
```
git clone git@github.com/aneoconsulting/ArmoniK.Admin.CLI.git
```
Navigate in the root directory
```
cd ArmoniK.Admin.CLI
```
Create a virtual environment
```
python -m venv ./venv
```
Activate the virtual environment
```
source ./venv/bin/activate
```
Install the build module
```
pip install build
```
Generate the archive and .whl file to install dependencies
```
python -m build
```
Install dependencies using the generated .whl file
```
pip install dist/name_of_the_archive.whl
```

### You can also automate these steps using the install_cli.sh script from the root directory :

This script will install python modules in a [venv](https://docs.python.org/3/library/venv.html) to avoid overwhelming your global environment

```
chmod +x ./tools/install_cli.sh
./tools/install_cli.sh
```

Don't forget to activate the virtual environment before using the CLI
```
source ./venv/bin/activate
```

## Documentation

[Documentation](https://aneoconsulting.github.io/ArmoniK.Admin.CLI/api/index.html) (TODO)


## Contributing

Contributions are always welcome!

See [CONTRIBUTING.md](https://github.com/aneoconsulting/ArmoniK.Api/blob/main/CONTRIBUTING.md) for ways to get started.
