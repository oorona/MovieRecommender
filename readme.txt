In order to build the new environment using conda. Type

./buildrecommenderapp.sh

This will create the environment for conda using the required packages.

if the data Analysis is required then run

./dataanalysys/builddataanalysis.sh

Once the conde environment is build


You can switch to recommenderapp using

conda activate recommenderapp

and then call

./run.sh

the application will run by default at

http://127.0.0.1:8000/


for the dataanalysis portion

switch to the other virtual environment
conda activate dataanalysis

then call jupyter
jupyter notebook
