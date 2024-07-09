import os
import tkinter as tk
#adds scrollbar
from tkinter import scrolledtext
#importing image lib for adding img to GUI
from PIL import Image, ImageTk
#adds library
from llama_cpp import Llama
#random num library
import random
#library that grabs todays date
import datetime
#import sound lib
from playsound import playsound

import threading

#model to used, this is where it can be changed if trying dif model
model_path="dolphin-2.6-mistral-7b-dpo.Q4_K_M.gguf"

#application version
version= 1.2

#get todays date
todays_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Global variable to control the generation process
stop_generation = False

#load model
def load_model():
    #if model exists, load model
    global model

    #checks model path existance
    if not os.path.isfile(model_path):
        print("Error: Using the model path " + model_path + ". That model does not exist at that location")
        #Exit since no valid path found
        exit()


    #can change these model sets to change parameters
    model = Llama(
        model_path=model_path,
        seed=random.randint(1, 2**32),
    )


    #generate response
def generate_response(model, input_tokens, prompt_input_text):
    global stop_generation
    stop_generation = False

    #User text display in text area
    text_area_display.insert(tk.INSERT, '\n\nUser: ' + prompt_input_text + '\n')
    #generate response
    output_response_text = b""
    count = 0
    output_response_text = b"\n\n Rebirth: "

    #generate response from model by putting vars together
    text_area_display.insert(tk.INSERT, output_response_text)

    for token in model.generate(input_tokens, top_k=40, top_p=0.95, temp=.72, repeat_penalty=1.1):
        #checking for stop button press
        if stop_generation:
            break

        #get response from output generated by tokens.
        response_text = model.detokenize([token])
        output_response_text = response_text.decode()

        #Displaying the genereated text
        text_area_display.insert(tk.INSERT, output_response_text)
        root.update_idletasks()

        count += 1

        #Break out after response

        #Can go beyond 2000 tokens once there is more logic behind program
        if count > 2000 or (token == model.token_eos()):
            break

        #Let user know response is done
        text_area_main_user_input.delete('1.0', tk.END)

#THREADING
def send_message_threaded():
    threading.Thread(target=send_message).start()

def clearGtext_threaded():
    threading.Thread(target=clearGtext).start()
     

#Creating Func to send message to model to show response
def send_message():
    user_prompt_input_text = text_area_main_user_input.get('1.0', 'end-1c').strip()

    byte_message = user_prompt_input_text.encode('utf-8')

    #------Phoenix personality-----
    input_tokens = model.tokenize(b"### Human: " + byte_message + b"\n### Phoenix: I am an immortal female phoenix from ancient China")

    #print to console for debugging in console (not for users top see)
    print("Input Tokens: ", input_tokens)

    #Generating function response from model
    generate_response(model, input_tokens, user_prompt_input_text)


#Sound for button
def play():
    playsound('fire.mp3')

#Stop Genereated text
def stopProg():
    global stop_generation
    stop_generation = True

#Clear Generated Text
def clearGtext():
    text_area_display.delete('1.0', tk.END)
    playsound('fire.mp3')



#Create main GUI func
def main():

    #loads model when app opens
    load_model()
    #creating main window of GUI
    global root
    root = tk.Tk()


    #Setting GUI title
    root.title("Rebirth -v" +str(version) + " - " + todays_date)


    #Assign image as var
    image_path = "Phoenix.png"
    image_path2 = "PhxTop.png"

    #check existing img file
    if os.path.exists(image_path):
        #opens img file using pillow
        img = Image.open(image_path)
        #resize img to fit gui/ width & height
        img = img.resize((1175,194), Image.LANCZOS)
        #convert pillow image to tkinter compatible img
        photo = ImageTk.PhotoImage(img)
        #Creating label to display img in GUI
        label = tk.Label(root, image=photo)
        #set img to label
        label.image = photo
        #put label on the GUI
        label.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


         #opens img file using pillow
        img2 = Image.open(image_path2)

        #resize img to fit gui/ width & height
        img2 = img2.resize((1185,45), Image.LANCZOS)

        #convert pillow image to tkinter compatible img
        photo2 = ImageTk.PhotoImage(img2)

        #Creating label to display img in GUI
        label2 = tk.Label(root, image=photo2)

        #set img to label
        label2.image = photo2

        #put label on the GUI
        label2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    else:

        #if img does not exist, print error msg
        print("Error: The image path " + image_path + " does not exist at this location.")
        #exit app 
        exit()


    #frame to add scrollbar to txt area
    frame_display= tk.Frame(root)
    scrollbar_frame_display = tk.Scrollbar(frame_display)
    #Create text area 
    global text_area_display
    text_area_display = scrolledtext.ScrolledText(frame_display, width=128, height=20, yscrollcommand=scrollbar_frame_display.set)

    #Change colors for GUI
    my_white = "white"
    my_dark_blue = "#aa553d"
    my_yellow = "#f1dc92"

    text_area_display.config(background=my_dark_blue, foreground=my_white, font= ("Papyrus", 11))

    #scrollbar properties
    scrollbar_frame_display.config(command=text_area_display.yview)
    text_area_display.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar_frame_display.pack(side=tk.RIGHT, fill=tk.Y)

    #frame display fill 
    frame_display.pack()


    frame_controls = tk.Frame(root)

    #Display LLM being used
    model_path_label = tk.Label(frame_controls, text="Model Path: " + model_path, foreground=my_dark_blue, font=("Parchment", 35))

    #placing label we made in frame
    model_path_label.pack(side=tk.LEFT, padx=10)

    frame_controls.pack(fill=tk.BOTH, padx=5, pady=5)


    #User input frame
    frame_user_input = tk.Frame(root)
    frame_user_input.pack(fill=tk.BOTH)

    frame_main_user_input = tk.Frame(root)
    scrollbar_main_user_input = tk.Scrollbar(frame_main_user_input)

    global text_area_main_user_input

    text_area_main_user_input = scrolledtext.ScrolledText(frame_main_user_input, width=128, height=5, yscrollcommand=scrollbar_main_user_input.set)

    #Text area bg/fg color and font
    text_area_main_user_input.config(background=my_dark_blue, foreground=my_yellow, font=("Papyrus", 12))

    scrollbar_main_user_input.config(command=text_area_main_user_input.yview)

    #Fill root window with frame
    text_area_main_user_input.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar_main_user_input.pack(side=tk.RIGHT, fill=tk.Y)
    frame_main_user_input.pack()

#Send button image
    load = Image.open("Send.png")
    render = ImageTk.PhotoImage(load)
    img = tk.Label(image=render)

#Stop button image
    load22 = Image.open("Stop.png")
    render22 = ImageTk.PhotoImage(load22)
    img22 = tk.Label(image=render22)

#Clear button Image
    load23 = Image.open("ClearR.png")
    render23 = ImageTk.PhotoImage(load23)
    img23 = tk.Label(image=render23)


    #Buttons
    send_button = tk.Button(root, command=send_message_threaded, image=render)
    stop_button = tk.Button(root, command=stopProg, image=render22,) 
    clear_button = tk.Button(root, command=clearGtext_threaded, image=render23,)

    #Button Pack
    send_button.pack(side=tk.LEFT)
    stop_button.pack(side=tk.LEFT)
    clear_button.pack(side=tk.LEFT)

    #run main loop of GUI
    root.mainloop()


#starting point of app

if __name__ == "__main__":
    main()


    


