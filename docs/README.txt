
# To generate .rst input files from source code
# .rst files will be created in ./api and source code path is ../hmkit
sphinx-apidoc -o ./api ../hmkit

# To generate Html files
make html

#Html output files generated in 
docs/_build/html

