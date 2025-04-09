sh bin/clean.sh
sh bin/build.sh
uv publish
# python3 -m twine upload --repository pypi dist/*
sh bin/clean.sh
