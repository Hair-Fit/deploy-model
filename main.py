from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
import numpy as np
from keras.preprocessing import image
import tensorflow as tf
from tensorflow.keras import utils as image
import os

app = FastAPI()
model = tf.keras.models.load_model('hairfit.h5')

# Configure CORS for allowed site in origins
availableOrigin = os.environ.get('BACKEND','*')
origins = [availableOrigin]
methods = ["*"]
headers = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)

IMGDIR = "tmp/img/"

@app.get("/")
async def root():
    return {"message": "Welcome to the Hair Fit Prediction API!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    img = await file.read()
    imgFullPath = IMGDIR + file.filename
    with open(f"{imgFullPath}","wb") as f:
        f.write(img)
    img_source = image.load_img(imgFullPath, target_size = (224,224))
    x = image.img_to_array(img_source)
    x = np.expand_dims(x, axis = 0)

    images = np.vstack([x])
    classes = model.predict(images, batch_size = 10)
    print(classes)
    answer = np.argmax(classes, axis = 1)

    result = ""
    if answer[0] == 0:
        print('Heart')
        result = "Heart"
    elif answer[0] == 1:
        print('Oblong')
        result = "Oblong"
    elif answer[0] == 2:
        print('Oval')
        result = "Oval"
    elif answer[0] == 3:
        print('Round')
        result = "Round"
    elif answer[0] == 4:
        print('Square')
        result = "Square"
    os.remove(imgFullPath)
    return {"filename": file.filename,"answer":result}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    run(app, host="0.0.0.0", port=port)
