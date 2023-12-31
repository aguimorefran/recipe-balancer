# Exit immediately if a command exits with a non-zero status

pip -q install isort black autoflake black[jupyter]

isort .
black .
autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive .
