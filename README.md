# 7wonders
A code to evaluate the scores of your 7wonders game based on your pictures

What needs to be done to run the script 7wonders.py:

0. cmd

Open a comand-window using the search function and typing "cmd"

2. Environment
Create a new environment called 7wonders using
	conda create --name 7wonders
Activate this environment
	conda activate 7wonders

3. Install packages
	pip install numpy
	pip install os
	pip install pillow
	pip install Ultralytics
	pip install regex
	pip install python-csv
	pip install pytesseract
	pip install easyocr
	pip install tabulate
	pip install os-sys

4. Organise files
The following structure must be held:

--> 
7wonders
	--> 7wonders.py
	--> weights
		--> 7wonders.pl
	--> yourfolder01
		--> 01_Eli.jpeg
		--> 02_Kim.jpeg
		--> 03_Robin.jpeg

Add a folder for each game you play into the folder 7wonders. You can name the folder as you like.
Within each game folder, you can place the x images of this game. You NEED to name the image files under the following rules:
	- start with a number (01,02,... or 1, 2, 3,...). These numbers are essential to the results, as they define the order in which you played!
		(e.g. 01_Name1.jpeg was sitting next to 02.Name2.jpeg and 05_Name5.jpeg if there were 5 players).
	- use an underscore "_" after the number to write the players name that is used in the result-table
		Note: Everything after the first underscore will be used as name.
		Note: If you wish to add more information to the filename, add another "_" after the players name.
	- Accepted image formats are: jpg, jpeg, png

4. run the script
Navigate the comand window to the folder 7wonders
	cd Documents/boardgames/7wonders (or similar)
run the script
	python 7wonders.py "yourfolder01"

5. See the results
The main results are stored in the file results.txt in youfolder01
Additional results are stored in the folder predictions, where each player gets their folder
	- with the image predicted by YOLO
	- a file (cards.txt) listing all cards detected
	- a file (string.txt) listing, what was actually read on the image
	- a file (list.txt) which lists results in a complicated way



ERRORS:
1. TesseractNotFound Error: tesseract is not installed or it's not in your path
	follow this: https://stackoverflow.com/q/50951955/25395012
	and open the script 7wonders.py with any text-editor to change the path in line 8 to the path, where your tesseract.exe file is
