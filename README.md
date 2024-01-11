MesoNHNamelistTool (mnt.py) is a tool to convert namelists from Méso-NH 5.6.X to 5.7.0.

# Installation
cd pathofyourchoice

git clone https://github.com/QuentinRodier/MesoNHNamelistTool.git

# Dependencies
pip install [--user] f90nml

# Setup
Add to your $HOME/.bash_profile :
export PATH=$PATH:pathofyourchoice/MesoNHNamelistTool

# How to use
Apply only once by namelist file as it changes the input file.

mnt.py --convert56to57 EXSEG1.nam

or

mnt.py --convert56to57 *.nam

Beta feature:

--applyf90nml : use f90nml to prettify namelists
