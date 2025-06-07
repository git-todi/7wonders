# 7wonders
A code to evaluate the scores of your 7wonders game based on your pictures

What needs to be done to run the script 7wonders.py:

1. cmd

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

4. Download Weights

Go to https://drive.google.com/file/d/1idrXjp7PyQsQJg5UbAUwIMxKZWgFNN7D/view?usp=drive_link to download the training-weights and store the file as described in point 5.
(the file is too large to store in the git repository)

5. Organise files

The following structure must be held:

--> 
7wonders
	--> 7wonders.py
	--> weights
		--> 7wonders.pl (needs to be downloaded, explained above)
	--> game_04 (An example of how the fully evaluate output will look like)
 		--> predictions
		--> 1_Tobias.jpeg
		--> 2_Flu.jpeg
		--> 3_Kim.jpeg
  		--> 4_Robin.jpeg
    		--> results.txt
      	--> game_05 (A set of images that can be used to test the code)
       		--> 1_Tobias.jpg
	 	--> 2_Flu.jpg
   		--> 3_Markus.jpg
     		--> 4_Ladina.jpg
    	--> YourGame (A folder you will create)
     		--> 1_firstplayer.jpeg
       		--> 2_secondplayer.jpeg
	 	--> 3_thirdplayer.jpeg

Add a folder for each game you play into the folder 7wonders. You can name the folder as you like.
Within each game folder, you can place the x images of this game. You NEED to name the image files under the following rules:
	- start with a number (01,02,... or 1, 2, 3,...). These numbers are essential to the results, as they define the order in which you played!
		(e.g. 01_Name1.jpeg was sitting next to 02.Name2.jpeg and 05_Name5.jpeg if there were 5 players).
	- use an underscore "_" after the number to assign the players name that is later used in the result-table
		Note: Everything after the first underscore will be used as name.
		Note: If you wish to add more information to the filename, add another "_" after the players name.
	- Accepted image formats are: jpg, jpeg, png

6. run the script

Navigate the comand window to the folder 7wonders
	cd Documents/boardgames/7wonders (or similar)
run the script
	python 7wonders.py "YourGame" (replace YourGame with whatever you named your folder)

Note: Running the code might take a minute or two.

7. See the results
    
The main results are stored in the file results.txt in the folder YourGame
Additional results are stored in the subfolder predictions, where each player gets their folder
	- with the image predicted by YOLO
	- a file (cards.txt) listing all cards detected
	- a file (string.txt) listing, what was actually read on the image
	- a file (list.txt) which lists results in a complicated way



ERRORS:
1. TesseractNotFound Error: tesseract is not installed or it's not in your path
	follow this: https://stackoverflow.com/q/50951955/25395012
	and open the script 7wonders.py with any text-editor to change the path in line 8 to the path, where your tesseract.exe file is
