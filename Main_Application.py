import pygame
from pyparsing import White
import tensorflow
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import pygame
import sys
from pygame.locals import *
import cv2 as cv
from tkinter import *
from tkinter import messagebox

# The following command is from the tkinter library
# It allows the main window to be hidden until the messagebox has been exited
Tk().wm_withdraw()

# Using the .showinfo command we can show a prompt to the user that will pop up
# The parameters are (Tittle of window, Message)
messagebox.showinfo("READ BEFORE CONTINUING","After running the code, the user will be asked to select a size for the window, the default size will be selected by simply hitting enter. \n\nDraw an object using the mouse, and holding down the left button. \n\nAfter drawing, indicate whether a number was drawn or a letter by pressing the key N or A respectively, this so the correct ML model can be used to predict whats drawn. \n\nTo clear the conosle and draw the next image hit the 'esc' key")

# This box is used to intialise set of variables that are to be used by pygame
# Intialiazation of the color variables
# The RGB vlaues for the colors was obtained from the following source
# https://www.rapidtables.com/web/color/RGB_Color.html
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# The path associated to the model is assigned to a variable
# Simply copy and paste the path associated to the saved model files
# In vscode, the relative path can be given
model_mnist = load_model('Best_Mnist_model.h5')
model_alpha = load_model('Best_letters_model.h5')

bound_cond = 2

# The window size for the .display module needs to be provided (see below)
# The variable that will be used are intialized
x_size = int()
y_size = int()

# We will create a library for the system to use, when utlising the models
Labels_Mnist = {0:"Zero", 1:"One", 2:"Two", 3:"Three", 4:"Four", 
                5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine"}

Labels_Alpha = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 
                5:"F", 6:"G", 7:"H", 8:"I", 9:"J",
                10:"K", 11:"L", 12:"M", 13:"N", 14:"O", 
                15:"P", 16:"Q", 17:"R", 18:"S", 19:"T",
                20:"U", 21:"V", 22:"W", 23:"X", 24:"Y",
                25:"Z"}

# Initial Condition set to false, for the variable that will become true 
# If the user is holding down the mouse button when drawing
Drawing = False
# Variable set to true for Prediction
Model_Prediction = True

# An array to store all the positions of the mouse positions when the user draws
# And keep in store to to continously display the numbers drawn
x_cord_position_array = []
y_cord_postion_array = []

# IMAGESAVE = False
# Variable to be used to resize image
Image_size = (28,28)

# An array that will hold the values for the converted image to array
Img_Model  = []

# Application window for pygame is intialized
pygame.init()

# User input to get a small or large window
print("Input the size of the window you would like to interact")
print("large or small")
# Take input from the user
size_selection = input()

# If the user inputted small, then a window of 500x400 will be created
if (size_selection.lower() == "small"):
  x_size = 500
  y_size = 400
# If the user inputted large, then a window of 700x500 will be created
elif (size_selection.lower() == "large"):
  x_size = 700
  y_size = 500 
# If the user inputs anything else or empty input then a standard window 
# of the size 500x500 will be created
else:
  x_size = 500
  y_size = 500

# Font to be used in the window/console
# Font SOURCE: https://www.fontspace.com/ariana-violeta-font-f34433
FONT = pygame.font.Font("ArianaVioleta-dz2K.ttf", 35)

# Displaying the console with the user selected measurments 
# The resizable command is givne so the size of the console can be altered by the user
display_dim = pygame.display.set_mode((x_size, y_size), pygame.RESIZABLE)
# WHILE_INT = display_dim.mp_rgb(WHITE)
# Icon for the console
pygame.display.set_icon((pygame.image.load('ICON.jpg')))
# Tittle of the console
pygame.display.set_caption("Alpha | ## Character Recognition")

# To sustain the console continously rather then it closing,
# A while loop is used that only closes when a select key is inputted.
while True:
    # This for loop continously runs to go through the event queue 
    for event in pygame.event.get():
        # As the console stays on, a way of quiting the console needs to be created
        # This can be done by using .event.get() command WINDOWSRESIZED [Source:pygame.org],
        # Where if the user hits the close button it will close the console
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # In case the set size of the windows is not right, using .display.update command
        # The event for this case would be WINDOWSRESIZED [Source:pygame.org]
        if event.type == pygame.VIDEORESIZE:
            display_dim = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            # Update the size variables
            x_size = event.w
            y_size = event.h

        # The following position activates whenever the curosr is within the console/window
        if event.type == pygame.WINDOWENTER:
            # Whenever the cursor is withing the window it will change its icon
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)


        # The following assess the condition if the user is holding down the mousebutton
        # If this condition is true then the Drawing condtion becomes true
        if event.type == MOUSEBUTTONDOWN:
            Drawing = True
        
        # Recording the movement of the mouse whenever the user is drawing, 
        # And then displaying it (pygame.draw)
        if event.type == MOUSEMOTION and Drawing:
            x_cord_position, y_cord_postion = event.pos
            # Saving the position values of the mouse into the arrays
            x_cord_position_array.append(x_cord_position)
            y_cord_postion_array.append(y_cord_postion)

            # Using the saved position values to draw on the console using pygame.draw
            pygame.draw.circle(surface = display_dim, color = WHITE, center = (x_cord_position, y_cord_postion), radius = 3, width = 0) 

        # When the user stops drawing (mouse button is no longer pressed)
        # This means the Drawing condition needs to change
        # The drawn number needs to be captured as an image
        if event.type == MOUSEBUTTONUP:
            Drawing = False
            x_cord_position_array = sorted(x_cord_position_array)
            y_cord_postion_array = sorted(y_cord_postion_array)

            # Drawing a rectangle around the drawn number (as mentioned in the GUI description above)
            # Assigning the size of the rectangular box
            x_max = (max(x_cord_position_array))
            x_min = (min(x_cord_position_array))
            y_max = (max(y_cord_postion_array))
            y_min = (min(y_cord_postion_array))

            width = x_max - x_min
            height = y_max - y_min

            # Determining the position/ cordinates for the different sides of a rectangle
            rectangle_Left = (max((x_min - bound_cond), 0))
            rectangle_Right = (min(x_size, (x_max + bound_cond)))
            rectangle_Up = (y_min - bound_cond)
            rectangle_Down = (min((y_max + bound_cond), x_size))

            # Reinitializing the arrays as empty
            x_cord_position_array = []
            y_cord_postion_array = []
            
            # Using Pygame to save the scrrenshot of the drawn image
            pygame.image.save(display_dim, "image.jpg")

            # Using OpenCV library to import the stored image
            img_imported = cv.imread("image.jpg")
            # Calculating parameters for CV to compress the image 
            ratio = 28.0 / img_imported.shape[1]
            dim = (28, int(img_imported.shape[0] * ratio))

            # Using the calculated parameters to resize the image as a 28x28 image
            resized_img = cv.resize(img_imported, dim, interpolation=cv.INTER_AREA)
            # Saving the new 28x28 Image
            cv.imwrite("Model_img.png", resized_img)

            # Loading the saved 28x28 Image
            Img_Model = image.load_img('Model_img.png')
            # Converting the image to an array using the tf library
            Img_Model = img_to_array(Img_Model)
            Img_Model = (Img_Model/255.0)
            # Adjusting the shape of the array so it fits the model
            Img_Model = Img_Model[ :, : , :1]

            # Adding a dimensional component so the shape is 1, 28, 28, 1
            Img_Model = np.expand_dims(Img_Model, 0)
            
        # To use the two different models the user can let the system know if theres an alphabet or a number
        # Using the input the respective models can be used to analyse and predict the drawings    
        if event.type == pygame.KEYDOWN:
            # If the user hits the n key the mnist model will be used for prediction
            if event.key == pygame.K_n:
                # Using .predict, the probability for the number or alphabet is made
                model_prediction = model_mnist.predict(Img_Model)

                # The highest probability is selected as the main prediction 
                # And the label for the probability is selected from the defined dictionary
                # And converted to a string object
                prediction_results = np.argmax(model_prediction)
                prediction_results = str(Labels_Mnist[prediction_results])

                # The predicted number is turned into a label
                prediction_label = FONT.render(prediction_results, True, BLACK, WHITE)
                Rendered_rect = prediction_label.get_rect()

                # The positions of the labels are assigned
                Rendered_rect.left = rectangle_Left
                Rendered_rect.right = rectangle_Right

                # The console is updated viewing the predicted results from the model
                display_dim.blit(prediction_label, Rendered_rect)    

            elif event.key == pygame.K_a:
                # Using .predict, the probability for the number or alphabet is made
                model_prediction = model_alpha.predict(Img_Model)

                # The highest probability is selected as the main prediction 
                # And the label for the probability is selected from the defined dictionary
                # And converted to a string object
                prediction_results = np.argmax(model_prediction)
                prediction_results = str(Labels_Alpha[prediction_results])

                # The predicted number is turned into a label
                prediction_label = FONT.render(prediction_results, True, BLACK, WHITE)
                Rendered_rect = prediction_label.get_rect()

                # The positions of the labels are assigned
                Rendered_rect.left = rectangle_Left
                Rendered_rect.right = rectangle_Right

                # The console is updated viewing the predicted results from the model
                display_dim.blit(prediction_label, Rendered_rect)

        # If the user hits the esc key on the keyboard, it will reset the console
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                display_dim.fill(BLACK)

        # Update the display everytime the for loop is exited    
        pygame.display.update()