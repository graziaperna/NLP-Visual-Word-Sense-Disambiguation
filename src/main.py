import tkinter as tk
from PIL import ImageTk
from tkinter import *
import PIL.Image
import joblib
import nltk
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
import string


class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        # Cleaning Text
        return [clean_text(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}
    
# Basic function to clean the text
def clean_text(text):
    # Removing spaces and converting text into lowercase
    translator = str.maketrans("", "", string.punctuation)
    text_without_punctuation = text.translate(translator)
    return text_without_punctuation.lower()
    #return text.strip().lower()

def treebankWordTokenizer(sentence):

    tokenizer = TreebankWordTokenizer()
    lemmatizer = WordNetLemmatizer()

    # Tokenize the sentence
    tokens = tokenizer.tokenize(sentence)

    # Lemmatize each token
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return lemmatized_tokens

root = tk.Tk()
root.title("Sexism relevation")

def getPrediction():

    input_text = text_box.get("1.0", "end-1c")
    input_text=[input_text]
        
    prediction = sModel.predict(input_text)
    pred_label.config(text="")

    if (prediction == 'sexist'):
        prediction = cModel.predict(input_text)

    pred_label.config(text=prediction[0])
    text_box.delete("1.0", tk.END)
    pred_label.grid(columnspan=3,column=1,row=10)

sModel = joblib.load('../sexism.pkl')
cModel = joblib.load('../category.pkl')

canv= tk.Canvas(root,width=600,height=300)
canv.grid(columnspan=5,rowspan=20)

logo = open("logo.png","rb")
logo = PIL.Image.open(logo)
logo = logo.resize((100,100))
logo =ImageTk.PhotoImage(logo)
logo_label = tk.Label(image = logo)
logo_label.image = logo
logo_label.grid(column=2,row=1,columnspan=1)


istructions=tk.Label(root, text="Insert a message", font="Raleway")
istructions.grid(columnspan=3,column=1,row=5)
text_box = Text(root,height=3, width=40)
# set the Text widget to Editable mode
text_box.config(state='normal')  
#box_label = tk.Label(root, text=text_box)
text_box.grid(columnspan=3,column=1,row=8)

# Get the user input from the Text widget
pred_label=tk.Label(root, text="", font="Raleway")


send_button = tk.Button(root, text ="Send", command = getPrediction)
send_button.grid(columnspan=1,column=4,row=8)
root.mainloop()


