import base64
import pickle
from pathlib import Path

ROOT = Path(__file__).parents[1]
CROP_IMG_PATH = ROOT / "data" / "crop_images"
DATA_PATH = ROOT / "data" / "crops.csv"
MODEL_PATH = ROOT / "ml_model" / "model.pkl"


with open(MODEL_PATH, "rb") as pickle_file:
    model = pickle.load(pickle_file)


crop_img_dict = {
    f.with_suffix("").name: str(f) for f in CROP_IMG_PATH.rglob("*")
}


def model_inference(feature_arr):
    prediction = model.predict(feature_arr)
    return prediction[0]


def get_img_file(
    prediction,
):
    img_file = [f for f in crop_img_dict if prediction in f][0]
    return img_file


def get_image(prediction, image_dict=crop_img_dict):
    img_path = image_dict[prediction]
    encoded_image = base64.b64encode(open(img_path, "rb").read())
    img_src = "data:image/png;base64,{}".format(encoded_image.decode())
    return img_src
