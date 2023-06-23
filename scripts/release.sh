git clone --depth 1 --branch v0.0.1 https://github.com/NeoTheBestDeveloper/neosql-core
cd neosql-core
git pull && sh scripts/release.sh
cd -
mv ./neosql-core/build_release/usr/local/lib/_neosql_core.so . 
mv ./neosql-core/build-mingw_release/usr/local/bin/_neosql_core.dll . 
poetry build && rm _neosql_core.so && rm _neosql_core.dll
