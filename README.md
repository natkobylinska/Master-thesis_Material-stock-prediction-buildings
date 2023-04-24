# thesis.material-inventory. Majority of the thesis was written in python in Google Colab. Repository includes both failed experiments of extracting information from raster files as well as final working Random Forest models predicting quantities of different materials from existing buildings that are at risk of demolition.

tests-google-satellite-img-crawler:

initial tests on extracting information from satellite pictures

-------------------------------------------------------------------
pdf-2-xlsx-process:

a python pipeline which was used to first turn specific pdf pages into images and then apply CV tables
recognition to the images in order to extract the information to .csv

-------------------------------------------------------------------
databases-matching:

python files used to automate information matching by EGID number

-------------------------------------------------------------------
machine_learning:

a full pipeline for each of the materials with all necessary .csv files.
The 'Bandliweg' files are an example of using prediction models for any other building
in Zurich. Open .csv files to see in what format you should prepare a building's input data.
