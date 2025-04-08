import argparse
import pickle
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import hf_hub_download

from foai_model.config import MAX_TOKEN_LENGTH
from foai_model.preprocessing import clean_resume

REPO_ID = "Dar3cz3Q/foai_model"
SUBFOLDER = "checkpoint"

tokenizer = AutoTokenizer.from_pretrained(REPO_ID, subfolder=SUBFOLDER)
model = AutoModelForSequenceClassification.from_pretrained(REPO_ID, subfolder=SUBFOLDER)
model.eval()
device = torch.device("cpu")
model.to(device)

encoder_path = hf_hub_download(
    repo_id=REPO_ID, filename="label_encoder.pkl", subfolder=SUBFOLDER
)

with open(encoder_path, "rb") as f:
    label_encoder = pickle.load(f)

index_to_label = dict(enumerate(label_encoder.classes_))


def predict(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=MAX_TOKEN_LENGTH,
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        logits = model(**inputs).logits
        predicted_class_id = torch.argmax(logits, dim=1).item()

    category = index_to_label[predicted_class_id]

    return {
        "id": predicted_class_id,
        "category": category,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Predict category distribution from text."
    )
    parser.add_argument("--text", type=str, required=True, help="Text to classify")

    args = parser.parse_args()
    resume = clean_resume(args.text)
    result = predict(resume)

    print("Result:", result)


if __name__ == "__main__":
    main()
