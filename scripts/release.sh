git clone --depth 1 --branch v0.0.1 https://github.com/NeoTheBestDeveloper/neosql-core
cd neosql-core
sh scripts/release.sh
cd -
mv ./neosql-core/build_release/usr/local/lib/_neosql_core.so . 
poetry build && rm _neosql_core.so
