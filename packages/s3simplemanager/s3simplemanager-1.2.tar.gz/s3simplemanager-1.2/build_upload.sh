#!/bin/bash

command_build="python3 -m build"
command_upload="twine upload dist/*"

$command_build
$command_upload
