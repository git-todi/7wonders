import os # to access files from the system
import re #needed to extract numbers out of a string
import numpy as np #needed for array handling
import csv # for reading and writing .csv files
from ultralytics import YOLO # for the image recognition
from PIL import Image # to read image files for ocr
import pytesseract # one ocr model
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import easyocr # another ocr model
from tabulate import tabulate # to write tables
import sys # to get arguments from bash


### ocr()

# function to read all words in the bounding boxes predicted by yolo

def ocr(bboxes, path):

    reader = easyocr.Reader(["en"])
    
    img = Image.open(path)
    masterstring = ""
    wordlist = []
    for i,bbox in enumerate(bboxes):
        xmin = float(bbox[0])
        ymin = float(bbox[1])
        xmax = float(bbox[2])
        ymax = float(bbox[3])
        cropped_img = img.crop((xmin, ymin, xmax, ymax))

        # a) tesseract
        pred = pytesseract.image_to_string(np.array(cropped_img))
        pred = pred.replace("\n", " ")
        pred = pred.replace("\x0c", "")
        masterstring += pred
        wordlist.append(pred)

        # b) EasyOCR
        result = reader.readtext(np.array(cropped_img))
        masterstring += f"{result[0][1]} "
        wordlist.append(result[0][1])
        
    return(masterstring, wordlist)


### cardlister()

# function to find all cards read by the ocr

def cardlister(masterstring):
    
    # how many cards of each color:
    n_brown = 0
    n_grey = 0
    n_blue = 0
    n_yellow = 0
    n_red = 0
    n_green_circle = 0
    n_green_gear = 0
    n_green_script = 0
    n_purple = 0
    
    # how many points due to each color:
    p_blue = 0
    p_yellow = 0
    p_purple = 0
    p_green = 0
    
    # create a list of all cards:
    cardlist = []
    
    # go through all the cards:
    
    ## 1st age ##
    
    if "HOL" in masterstring in masterstring or "OLZ" in masterstring or "ZP" in masterstring:
        n_brown += 1
        cardlist.append("HOLZPLATZ")
    if "STEIN" in masterstring:
        for match in re.finditer("STEIN", masterstring):
            start = match.start()
            if not masterstring[start-1] == "K":
                n_brown += 1
                if not "STEINBRUCH" in cardlist:
                    cardlist.append("STEINBRUCH")
    if "GELE" in masterstring:
        n_brown += 1
        cardlist.append("ZIEGELEI")
    if "RZB" in masterstring or "BERG" in masterstring or "RGWERK" in masterstring:
        n_brown += 1
        cardlist.append("ERZBERGWERK")
    if "BAUM" in masterstring:
        n_brown += 1
        cardlist.append("BAUMSCHULE")
    if "ABB" in masterstring or "STO" in masterstring or "LLEN" in masterstring:
        n_brown += 1
        cardlist.append("ABBAUSTOLLEN")
    if "TON" in masterstring or "GRUBE" in masterstring:
        n_brown += 1
        cardlist.append("TONGRUBE")
    if "FORST" in masterstring or "WIRT" in masterstring:
        n_brown += 1
        cardlist.append("FORSTWIRTSCHAFT")
    if "WALD" in masterstring or "HOHL" in masterstring:
        n_brown += 1
        cardlist.append("WALDHÖHLE")
    if "MIN" in masterstring:
        n_brown += 1
        cardlist.append("MINE")
        
    if "GLAS" in masterstring or "CLAS" in masterstring:
        n_grey += 1
        cardlist.append("GLASHÜTTE")
    if "PRE" in masterstring or "ESS" in masterstring:
        n_grey += 1
        cardlist.append("PRESSE")
    if "WEB" in masterstring or "STUH" in masterstring or "UHL" in masterstring:
        n_grey += 1
        cardlist.append("WEBSTUHL")
    
    if "BRUN" in masterstring or "NNEN" in masterstring:
        n_blue += 1
        p_blue += 3
        cardlist.append("BRUNNEN")
    if "BAD" in masterstring or "ADER" in masterstring:
        n_blue += 1
        p_blue += 3
        cardlist.append("BÄDER")
    if "ALT" in masterstring or "LTAR" in masterstring:
        n_blue += 1
        p_blue += 3
        cardlist.append("ALTAR")
    if "EA" in masterstring or "ATER" in masterstring:
        n_blue += 1
        p_blue += 3
        cardlist.append("THEATER")
    
    if "VERN" in masterstring:
        n_yellow += 1
        cardlist.append("TAVERNE")
    if "MAR" in masterstring or "ARK" in masterstring:
        n_yellow += 1
        cardlist.append("MARKT")
    if "N WES" in masterstring:
        n_yellow += 1
        cardlist.append("HANDELSPOSTEN WEST")
    if "N OST" in masterstring:
        n_yellow += 1
        cardlist.append("HANDELSPOSTEN OST") 
    if "LIS" in masterstring or "SAD" in masterstring:
        n_red += 1
        cardlist.append("PALISADE")
    if "KAS" in masterstring or "ASE" in masterstring:
        n_red += 1
        cardlist.append("KASERNE")
    if "WAC" in masterstring or "HTU" in masterstring:
        n_red += 1
        cardlist.append("WACHTURM")
    
    if "APO" in masterstring or "POT" in masterstring or "EKE" in masterstring:
        n_green_circle += 1
        cardlist.append("APOTHEKE")
    if "STATT" in masterstring or "WERKST" in masterstring:
        n_green_gear += 1
        cardlist.append("WERKSTATT")
    if "SKR" in masterstring or "PTO" in masterstring or "RIP" in masterstring:
        n_green_script += 1
        cardlist.append("SKRIPTORIUM")
    
    ## 2nd age ## 
    if "SAG" in masterstring or "EWER" in masterstring:
        n_brown += 1
        cardlist.append("SÄGEWERK")
    if "KAL" in masterstring or "KSTE" in masterstring:
        n_brown += 1
        cardlist.append("KALKSTEINBRUCH")
    if "BRE" in masterstring or "NER" in masterstring:
        n_brown += 1
        cardlist.append("ZIEGELBRENNEREI")
    if "GIE" in masterstring or "EBE" in masterstring:
        n_brown += 1
        cardlist.append("GIESSEREI")
    
    if "ATU" in masterstring or "TUE" in masterstring:
        n_blue += 1
        p_blue += 4
        cardlist.append("STATUE")
    if "AQ" in masterstring or "QU" in masterstring or "DUK" in masterstring:
        n_blue += 1
        p_blue += 4
        cardlist.append("AQUÄDUKT")
    if "TEM" in masterstring or "PEL" in masterstring:
        n_blue += 1
        p_blue += 4
        cardlist.append("TEMPEL")
    if "ERI" in masterstring or "RIC" in masterstring:
        n_blue += 1
        p_blue += 4
        cardlist.append("GERICHT")
    
    if "KARA" in masterstring or "RAW" in masterstring:
        n_yellow += 1
        cardlist.append("KARAWANSEREI")
    if "ORU" in masterstring or "RUM" in masterstring:
        n_yellow += 1
        cardlist.append("FORUM")
    if "WEI" in masterstring or "NBE" in masterstring:
        n_yellow += 1
        cardlist.append("WEINBERG")
    if "BAS" in masterstring or "SAR" in masterstring:
        n_yellow += 1
        cardlist.append("BASAR")
    
    if "STAL" in masterstring or "ALLE" in masterstring:
        n_red += 1
        cardlist.append("STÄLLE")
    if "CHIEB" in masterstring or "BPL" in masterstring or "SCHIE" in masterstring:
        n_red += 1
        cardlist.append("SCHIESSPLATZ")
    if "WALL" in masterstring:
        n_red += 1
        cardlist.append("WALL")
    if "BUN" in masterstring or "SPL" in masterstring:
        n_red += 1
        cardlist.append("ÜBUNGSPLATZ")
    
    if "RAN" in masterstring or "NHAU" in masterstring:
        n_green_circle += 1
        cardlist.append("KRANKENHAUS")
    if "LAB" in masterstring or "RATORI" in masterstring:
        n_green_gear += 1
        cardlist.append("LABORATORIUM")
    if "BIB" in masterstring or "LIO" in masterstring:
        n_green_script += 1
        cardlist.append("BIBLIOTHEK")
    for match in re.finditer('SCHULE', masterstring): # as SCHULE is in BAUMSCHULE and GLADIATORENSCHULE, the approach must be different
        start = match.start()
        if not masterstring[start-1] == "N" and not masterstring[start-1] == "M":
            n_green_script += 1
            cardlist.append("SCHULE")
    
    
    ## 3rd Age ##
    
    if "PAN" in masterstring or "EON" in masterstring:
        n_blue += 1
        p_blue += 7
        cardlist.append("PANTHEON")
    if "ART" in masterstring:
        n_blue += 1
        p_blue += 5
        cardlist.append("GÄRTEN")
    if "ATHA" in masterstring:
        n_blue += 1
        p_blue += 6
        cardlist.append("RATHAUS")
    if "PALA" in masterstring or "AST" in masterstring:
        n_blue += 1
        p_blue += 8
        cardlist.append("PALAST")
    if "NAT" in masterstring:
        n_blue += 1
        p_blue += 6
        cardlist.append("SENAT")
    
    if "LEU" in masterstring or "TTU" in masterstring:
        n_yellow += 1
        cardlist.append("LEUCHTTURM")
    if "AFE" in masterstring:
        n_yellow += 1
        cardlist.append("HAFEN")
    if "KAM" in masterstring:
        n_yellow += 1
        cardlist.append("HANDELSKAMMER")
    if "LAD" in masterstring:
        n_yellow += 1
        cardlist.append("GLADIATORENSCHULE")
    if "ARE" in masterstring or "RENA" in masterstring:
        n_yellow += 1
        cardlist.append("ARENA")
    
    if "ILI" in masterstring or "RLA" in masterstring:
        n_red += 1
        cardlist.append("MILITÄRLAGER")
    if "FES" in masterstring or "SAN" in masterstring:
        n_red += 1
        cardlist.append("FESTUNGSANLAGEN")
    if "CIR" in masterstring or "RCU" in masterstring:
        n_red += 1
        cardlist.append("CIRCUS")
    if "ARS" in masterstring or "SENAL" in masterstring:
        n_red += 1
        cardlist.append("ARSENAL")
    if "BEL" in masterstring or "ERUN" in masterstring or "MASCH" in masterstring:
        n_red += 1
        cardlist.append("BELAGERUNGSMASCHINEN")
    
    if "LOG" in masterstring:
        n_green_circle += 1
        cardlist.append("LOGE")
    if "AKA" in masterstring or "DEM" in masterstring:
        n_green_circle += 1
        cardlist.append("AKADEMIE")
    if "OBS" in masterstring or "VAT" in masterstring:
        n_green_gear += 1
        cardlist.append("OBERSVATORIUM")
    if "TUD" in masterstring or "RZI" in masterstring:
        n_green_gear += 1
        cardlist.append("STUDIERZIMMER")
    if "UNI" in masterstring or "VERS" in masterstring:
        n_green_script += 1
        cardlist.append("UNIVERSITÄT")
    
    if "ARB" in masterstring or "EITE" in masterstring:
        n_purple += 1
        cardlist.append("GILDE DER ARBEITER")
    if "NDWE" in masterstring or "KER" in masterstring:
        n_purple += 1
        cardlist.append("GILDE DER HANDWERKER")
    if "MAG" in masterstring or "TRA" in masterstring:
        n_purple += 1
        cardlist.append("GILDE DER MAGISTRATEN")
    if "NDL" in masterstring:
        n_purple += 1
        cardlist.append("GILDE DER HÄNDLER")
    if "MEI" in masterstring or "STER" in masterstring:
        n_purple += 1
        cardlist.append("GILDE DER BAUMEISTER")
    if "SPI" in masterstring or "ONE" in masterstring:
        n_purple += 1
        cardlist.append("GILDE DER SPIONE")
    if "PHIL" in masterstring or "SOP" in masterstring:
        n_purple += 1
        cardlist.append("GILDE DER PHILOSOPHEN")
    if "DEK" in masterstring or "EURE" in masterstring or "TEU" in masterstring:
        n_purple += 1
        cardlist.append("GILDE DER DEKORATEURE")
    if "WIS" in masterstring:
        n_purple += 1
        cardlist.append("GILDE DER WISSENSCHAFTLER")
    if "REE" in masterstring or "EED" in masterstring:
        n_purple += 1
        cardlist.append("GILDE DER REEDER")

    n_green = n_green_gear + n_green_circle + n_green_script

    playerlist = [[n_brown, n_grey, n_blue, n_yellow, n_red, [n_green_circle, n_green_gear, n_green_script], n_purple],cardlist]
    return(playerlist)



### wonderdetector()

# function to find the wonder out of the words read by the ocr

def wonderdetector(masterstring, mode, wonders_built):
    
    wonder = "no wonder detected"
    p_wonder = 0
    n_max = "error"
    
    if "ALE" in masterstring or "RIA" in masterstring:
        wonder = "ALEXANDRIA"
        n_max = 3
        if mode == "night":
            if wonders_built == 3:
                p_wonder = 7
        if mode == "day":
            if wonders_built == 1 or wonders_built == 2:
                p_wonder = 3
            if wonders_built == 3:
                p_wonder = 10
                        
    if "LYM" in masterstring or "PIA" in masterstring:
        wonder = "OLYMPIA"
        n_max = 3
        if mode == "night":
            if wonders_built == 1:
                p_wonder = 2
            if wonders_built == 2:
                p_wonder = 5
            if wonders_built == 3:
                p_wonder = 10
        if mode == "day":
            if wonders_built == 1 or wonders_built == 2:
                p_wonder = 3
            if wonders_built == 3:
                p_wonder = 10
        
    if "EPH" in masterstring or "ESO" in masterstring:
        wonder = "EPHESOS"
        n_max = 3
        if mode == "night":
            if wonders_built == 1:
                p_wonder = 2
            if wonders_built == 2:
                p_wonder = 5
            if wonders_built == 3:
                p_wonder = 10
        if mode == "day":
            if wonders_built == 1 or wonders_built == 2:
                p_wonder = 3
            if wonders_built == 3:
                p_wonder = 10
    
    if "GIZ" in masterstring or "ZAH" in masterstring:
        wonder = "GIZAH"
        if mode == "night":
            n_max = 4
            if wonders_built == 1:
                p_wonder = 3
            if wonders_built == 2:
                p_wonder = 8
            if wonders_built == 3:
                p_wonder = 13
            if wonders_built == 4:
                p_wonder = 20
        if mode == "day":
            n_max = 3
            if wonders_built == 1:
                p_wonder = 3
            if wonders_built == 2:
                p_wonder = 8
            if wonders_built == 3:
                p_wonder = 15

    if "HAL" in masterstring or "ASS" in masterstring or "ARN" in masterstring:
        wonder = "HALIKARNASSOS"
        n_max = 3
        if mode == "night":
            if wonders_built == 1:
                p_wonder = 2
            if wonders_built == 2 or wonders_built == 3:
                p_wonder = 3
        if mode == "day":
            if wonders_built == 1 or wonders_built == 2:
                p_wonder = 3
            if wonders_built == 3:
                p_wonder = 10
                
    if "BAB" in masterstring or "LON" in masterstring:
        wonder = "BABYLON"
        if mode == "night":
            n_max = 2
            p_wonder = 0
        if mode == "day":
            n_max = 3
            if wonders_built == 1 or wonders_built == 2:
                p_wonder = 3
            if wonders_built == 3:
                p_wonder = 10
    
    if "RHO" in masterstring or "DOS" in masterstring:
        wonder = "RHODOS"
        if mode == "night":
            n_max = 2
            if wonders_built == 1:
                p_wonder = 3
            if wonders_built == 2:
                p_wonder = 7
        if mode == "day":
            n_max = 3
            if wonders_built == 1 or wonders_built == 2:
                p_wonder = 3
            if wonders_built == 3:
                p_wonder = 10


    wondername = f"{wonder}_{mode}"
    
    return(wondername, n_max, wonders_built, p_wonder)

### bluepoints()

def bluepoints(cardlist):
    points = 0
    if "BRUNNEN" in cardlist:
        points += 3
    if "BÄDER" in cardlist:
        points += 3
    if "ALTAR" in cardlist:
        points += 3
    if "THEATER" in cardlist:
        points += 3
    if "STATUE" in cardlist:
        points += 4
    if "AQUÄDUKT" in cardlist:
        points += 5
    if "TEMPEL" in cardlist:
        points += 4
    if "GERICHT" in cardlist:
        points += 4
    if "PANTHEON" in cardlist:
        points += 7
    if "GÄRTEN" in cardlist:
        points += 5
    if "RATHAUS" in cardlist:
        points += 6
    if "PALAST" in cardlist:
        points += 8
    if "SENAT" in cardlist:
        points += 6
    return(points)

### purplepoints()

def purplepoints(masterlist, player, p_left, p_right):
    points = 0
    if "GILDE DER ARBEITER" in masterlist[player][1]:
        points += masterlist[p_left][0][0]
        points += masterlist[p_right][0][0]
    if "GILDE DER HANDWERKER" in masterlist[player][1]:
        points += masterlist[p_left][0][1]*2
        points += masterlist[p_right][0][1]*2
    if "GILDE DER MAGISTRATEN" in masterlist[player][1]:
        points += masterlist[p_left][0][2]
        points += masterlist[p_right][0][2]
    if "GILDE DER HÄNDLER" in masterlist[player][1]:
        points += masterlist[p_left][0][3]
        points += masterlist[p_right][0][3]
    if "GILDE DER SPIONE" in masterlist[player][1]:
        points += masterlist[p_left][0][4]
        points += masterlist[p_right][0][4]
    if "GILDE DER PHILOSOPHEN" in masterlist[player][1]:
        points += masterlist[p_left][0][5]
        points += masterlist[p_right][0][5]
    if "GILDE DER REEDER" in masterlist[player][1]:
        points += masterlist[player][0][0]
        points += masterlist[player][0][1]
        points += masterlist[player][0][6]
    if "GILDE DER BAUMEISTER" in masterlist[player][1]:
        points += masterlist[player][2][2]
        points += masterlist[p_left][2][2]
        points += masterlist[p_right][2][2]
    if "GILDE DER DEKORATEURE" in masterlist[player][1]:
        if masterlist[player][2][2] == masterlist[player][2][1]: # if wonders_built == max_wonders
            points += 7
    # gilde der wissenschaftler is counted in greenpoints()

    return(points)


### greenpoints()

def greenpoints(playerlist):
    # counting the green points is trivial, except in two cases:
        # player has "GILDE DER WISSENSCHAFTEN" 
        # player has built 2 wonders in BABYLON
    
    # in case, a player has 1, there are 3 possibilities
    # in case a player has both, there are 6 possibilities to use the extra symbol
    
    c = playerlist[0][5][0]
    g = playerlist[0][5][1]
    s = playerlist[0][5][2]
    
    extras = 0
    if "GILDE DER WISSENSCHAFTLER" in playerlist[1]:
        extras += 1
    if "BABYLON" in playerlist[2][0] and playerlist[2][2] >=2:
        extras += 1
    
    green_points = []
    
    if extras == 0:
        # A:
        Agp = 0
        Agp += (c)**2
        Agp += (g)**2
        Agp += (s)**2
        Agp += min(c,g,s) *7
        green_points.append(Agp)
    
    
    if extras == 1:
        # A:
        Agp = 0
        Agp += (c+1)**2
        Agp += (g)**2
        Agp += (s)**2
        Agp += min(c+1,g,s) *7
        green_points.append(Agp)
    
        # B:
        Bgp = 0
        Bgp += (c)**2
        Bgp += (g+1)**2
        Bgp += (s)**2
        Bgp += min(c,g+1,s) *7
        green_points.append(Bgp)
    
        # C:
        Cgp = 0
        Cgp += (c)**2
        Cgp += (g)**2
        Cgp += (s+1)**2
        Cgp += min(c,g,s+1) *7
        green_points.append(Cgp) 
    
    
    if extras == 2:
        # A:
        Agp = 0
        Agp += (c+2)**2
        Agp += g**2
        Agp += s**2
        Agp += min(c+2,g,s) *7
        green_points.append(Agp)
        
        # B:
        Bgp = 0
        Bgp += (c+1)**2
        Bgp += (g+1)**2
        Bgp += s**2
        Bgp += min(c+1,g+1,s) *7
        green_points.append(Bgp)
        
        # C:
        Cgp = 0
        Cgp += (c+1)**2
        Cgp += (g)**2
        Cgp += (s+1)**2
        Cgp += min(c+1,g,s+1) *7
        green_points.append(Cgp)
        
        # D:
        Dgp = 0
        Dgp += (c)**2
        Dgp += (g+2)**2
        Dgp += s**2
        Dgp += min(c,g+2,s) *7
        green_points.append(Dgp)
        
        # E:
        Egp = 0
        Egp += (c)**2
        Egp += (g+1)**2
        Egp += (s+1)**2
        Egp += min(c,g+1,s+1) *7
        green_points.append(Egp)
        
        # F:
        Fgp = 0
        Fgp += (c)**2
        Fgp += (g)**2
        Fgp += (s+2)**2
        Fgp += min(c,g,s+2) *7
        green_points.append(Fgp)
        
    green_points = max(green_points)
    return(green_points)


### yellowpoints()

def yellowpoints(playerlist):
    p_yellow = 0
    if "LEUCHTTURM" in playerlist[1]:
        p_yellow += playerlist[0][3]
    if "HAFEN" in playerlist[1]:
        p_yellow += playerlist[0][0]
    if "HANDELSKAMMER" in playerlist[1]:
        p_yellow += playerlist[0][1]*2
    if "GLADIATORENSCHULE" in playerlist[1]:
        p_yellow += playerlist[0][4]
    if "ARENA" in playerlist[1]:
        p_yellow += playerlist[2][2]
    return(p_yellow)


### player_analyzer()

### function to analyze each players board to store all vital information

def player_analyzer(img_paths, model, folder, img_names):
    
    masterlist = []

    class_list = []

    masterstrings = []
    
    for img_path, img_name in zip(img_paths, img_names):
        player_name = re.split(r"[_.]+", img_name)[1]
        img = Image.open(img_path)
        results = model(img, verbose=False, save=True, project=f"{folder}/predictions", name=player_name, show_conf=False, show_labels=False)
        
        for result in results:
            
            words = 0
            coins = 0
            military = 0
            modecounter = 0 # to make sure, that only either sun or moon is detected
            wonders_built = 0
            word_indices = []
            
            clss = np.array(result.boxes.cls.tolist()) # creates an array where each element is the cls of a detected object
            class_list.append(clss)
            for i, cls in enumerate(clss):
                cls = int(cls)
                if cls == 0:
                    words += 1
                    word_indices.append(i) # we start a list with all links to the bounding boxes around words.
                if cls == 1:
                    mode = "day"
                    modecounter += 1
                if cls == 2:
                    mode = "night"
                    modecounter += 1
                if cls == 3:
                    coins += 1
                if cls == 4:
                    coins += 3
                if cls == 5:
                    military -= 1
                if cls == 6:
                    military += 1
                if cls == 7:
                    military += 3
                if cls == 8:
                    military += 5
                if cls == 9:
                    wonders_built += 1
    
            if modecounter == 2 or modecounter == 0:
                print(f"mode: \t\t day/night was not properly detected! ({modecounter} detected)")
                
            word_bboxes = result.boxes.xyxy[word_indices]
            
            masterstring, wordlist = ocr(bboxes=word_bboxes, path = img_path)
            
            wonder = wonderdetector(masterstring, mode, wonders_built)
            
            playerlist = cardlister(masterstring)
            playerlist.append(wonder)
            playerlist.append(int(coins/3))
            playerlist.append(military)
            
            masterlist.append(playerlist)

            masterstrings.append(masterstring)

            # some printing to evaluate process:
            print(f"{player_name}:\t\t {img_path}")
            print(f"wonder:\t\t {wonder[0]}\n")
            
    return(masterlist, masterstrings, class_list)


### summarizer(masterlist):

# function to summarize all points (also those that are dependent on your neighbours cards)

def summarizer(masterstlist, masterstring, output_path, img_names):

    result = []
    
    n_players = len(masterlist)
    for i,playerlist in enumerate(masterlist):
        # define neighbouring players:
        if i==0:
            p_left = n_players-1 # e.g. player 1 is sitting next to player 4
            p_right = 1
        if i == n_players-1:
            p_left =  0 # e.g. player 4 is sitting next to player 1
            p_right = n_players-2
        if not i==0 and not i==n_players-1:
            p_left = i-1
            p_right = i+1

        player_name = re.split(r"[_.]+", img_names[i])[1]
        
        p_blue = bluepoints(playerlist[1])
    
        p_purple = purplepoints(masterlist, i, p_left, p_right)
    
        p_green = greenpoints(playerlist)
    
        p_yellow = yellowpoints(playerlist)
    
        p_wonder = playerlist[2][3]
    
        p_coins = playerlist[3]
    
        p_military = playerlist[4]

        wonder = playerlist[2][0]

        with open(f"{output_path}/predictions/{player_name}/{player_name}_cards.txt", "w") as f:
            for card in playerlist[1]:
                f.write(f"{card}\n")
        f.close()
        
        with open(f"{output_path}/predictions/{player_name}/{player_name}_string.txt", "w") as f:
            f.write(masterstring[i])
        f.close()

        with open(f"{output_path}/predictions/{player_name}/{player_name}_list.txt", "w") as f:
            for l1 in playerlist:
                f.write(f"{str(l1)}\n")
        f.close()
        
        p_total = p_blue + p_purple + p_green + p_yellow + p_wonder + p_coins + p_military
        
        result.append([player_name, p_total, p_wonder, p_coins, p_military, p_blue, p_yellow, p_green, p_purple, wonder])

    return(result)



folder = sys.argv[1]


img_names = sorted(os.listdir(f"{folder}"))
img_paths = [os.path.join(f"{folder}", i) for i in img_names]
img_paths = [i for i in img_paths if i.endswith(".jpg") or i.endswith(".jpeg") or i.endswith(".png")]
output_path = f"{folder}"

model = YOLO("weights/7wonders.pt")

masterlist,masterstring, class_list = player_analyzer(img_paths, model, folder, img_names)

result = summarizer(masterlist, masterstring, output_path, img_names)

headers = ["", "total", "wonder", "coins", "military", "blue", "yellow", "green", "purple", "wonder"]

result_table = tabulate(sorted(result, key=lambda x: x[1], reverse=True), headers=headers, tablefmt="grid")

with open (f"{output_path}/results.txt", "w") as t:
    t.write(result_table)
t.close()


