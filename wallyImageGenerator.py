from PIL import Image, ImageOps
import numpy as np 
import os.path
import os

IMAGE_COUNT = 1000

BACKGROUND_DIR = "Background"
WALLY_DIR = "WallyImages"
RESULT_DIR = "CreatedImages"

BACKGROUND_WIDTH = 500
BACKGROUND_HEIGHT = 350

WALLY_IMAGE_WIDTH_RATIO = 1/10
WALLY_IMAGE_HEIGHT_RATIO = 1/3

WALLY_IMAGE_WIDTH_RANDOM_VAR = 0
WALLY_IMAGE_HEIGHT_RANDOM_VAR = 0

WALLY_IMAGE_VARIABLES = [0, 1, 2, 3]
BACKGROUND_IMAGE_VARIABLES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

#Cargamos los posibles fondos
backgroundImages = []
for i in range(len(BACKGROUND_IMAGE_VARIABLES)):
    imageSrc = BACKGROUND_DIR + "/background" + str(BACKGROUND_IMAGE_VARIABLES[i]) + ".png"
    backgroundImages.append(Image.open(imageSrc))

#Calculamos el tamano base de los wally
wallyImageBaseWidth = round(BACKGROUND_WIDTH * WALLY_IMAGE_WIDTH_RATIO)
wallyImageBaseHeight = round(BACKGROUND_HEIGHT * WALLY_IMAGE_HEIGHT_RATIO)

#Cargamos los posibles wallys segun la escalada necesaria
#Siempre es mejor reducir el tamano que aumentarlo
wallyImages = []
for i in range(len(WALLY_IMAGE_VARIABLES)):
    
    if wallyImageBaseWidth <= 150:
        imageSrc = WALLY_DIR + "/150x400/wally" + str(WALLY_IMAGE_VARIABLES[i]) + ".png"
        wallyImages.append(Image.open(imageSrc).convert('RGBA'))

    elif wallyImageBaseWidth <= 300:
        imageSrc = WALLY_DIR + "/300x800/wally" + str(WALLY_IMAGE_VARIABLES[i]) + ".png"
        wallyImages.append(Image.open(imageSrc))
    
    else:
        imageSrc = WALLY_DIR + "/600x1600/wally" + str(WALLY_IMAGE_VARIABLES[i]) + ".png"
        wallyImages.append(Image.open(imageSrc))

#Borramos el archivo de coordenadas viejas si existia
if os.path.exists("wallyCoordinate.txt"):
    os.remove("wallyCoordinate.txt") 

#Creamos las imagenes y guardamos las coordenadas
wallyCoordinatesLog = open("wallyCoordinate.txt", "a")
for i in range(IMAGE_COUNT):

    #CREATING BACKGROUND
    backVarIndex = np.random.randint(0,len(BACKGROUND_IMAGE_VARIABLES))
    width, height = backgroundImages[backVarIndex].size

    xCoordinate = np.random.randint(0, width - BACKGROUND_WIDTH)
    yCoordinate = np.random.randint(0, height - BACKGROUND_HEIGHT)

    xEdgeCoordinate = xCoordinate + BACKGROUND_WIDTH
    yEdgeCoordinate = yCoordinate + BACKGROUND_HEIGHT

    cropBackgroundImage = backgroundImages[backVarIndex].crop((xCoordinate, yCoordinate, xEdgeCoordinate, yEdgeCoordinate))

    #CREATING WALLY
    wallyVarIndex = np.random.randint(0,len(WALLY_IMAGE_VARIABLES))

    wallyImageWidthMin = round(wallyImageBaseWidth * (1 - WALLY_IMAGE_WIDTH_RANDOM_VAR))
    wallyImageWidthMax = round(wallyImageBaseWidth * (1 + WALLY_IMAGE_WIDTH_RANDOM_VAR))

    wallyImageHeightMin = round(wallyImageBaseHeight * (1 - WALLY_IMAGE_HEIGHT_RANDOM_VAR))
    wallyImageHeightMax = round(wallyImageBaseHeight * (1 + WALLY_IMAGE_HEIGHT_RANDOM_VAR))

    wallyImageWidth = wallyImageWidthMin
    if  wallyImageWidthMin > wallyImageWidthMax:
        wallyImageWidth = np.random.randint(wallyImageWidthMin, wallyImageWidthMax)
    
    wallyImageHeight = wallyImageHeightMin
    if  wallyImageHeightMin > wallyImageHeightMax:
        wallyImageHeight = np.random.randint(wallyImageHeightMin, wallyImageHeightMax)

    finalWallyImage = wallyImages[wallyVarIndex].resize((wallyImageWidth, wallyImageHeight))
    
    if np.random.randint(0,2) == 0:
        finalWallyImage = ImageOps.mirror(finalWallyImage)

    #PASTE WALLY IN BACKGROUND
    backWidth, backHeight = cropBackgroundImage.size
    wallyWidth, wallyHeight = finalWallyImage.size

    xWallyCoordinate = np.random.randint(0, backWidth - wallyWidth)
    yWallyCoordinate = np.random.randint(0, backHeight - wallyHeight)

    cropBackgroundImage.paste(finalWallyImage, (xWallyCoordinate, yWallyCoordinate), mask=finalWallyImage)
    print("Creando Imagen: " + str(i) + " con Background " + str(backVarIndex) + " y wally " + str(wallyVarIndex) + " " + str(wallyWidth) + " " + str(wallyHeight))
    
    wallyCoordinatesLog.write(str(xWallyCoordinate) + " " + str(yWallyCoordinate) + "\n")
    
    cropBackgroundImage.save(RESULT_DIR + "/prueba" + str(i) + ".png", quality=95)

wallyCoordinatesLog.close()