clean:
	rm -rf dist neosql-core

build:
	sh scripts/release.sh

test:
	sh scripts/release.sh
	pytest -sv
