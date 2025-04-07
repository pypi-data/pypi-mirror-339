import argparse
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from foai_model.config import MAX_TOKEN_LENGTH

REPO_ID = "Dar3cz3Q/foai_model"
SUBFOLDER = "checkpoint"

tokenizer = AutoTokenizer.from_pretrained(REPO_ID, subfolder=SUBFOLDER)
model = AutoModelForSequenceClassification.from_pretrained(REPO_ID, subfolder=SUBFOLDER)
model.eval()
device = torch.device("cpu")
model.to(device)


def predict(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=MAX_TOKEN_LENGTH,
    )
    inputs = {key: val.to(device) for key, val in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_id = torch.argmax(logits, dim=1).item()

    return predicted_class_id


def main():
    parser = argparse.ArgumentParser(description="Predict category from input text.")
    parser.add_argument("--text", type=str, required=True, help="Text to classify")

    args = parser.parse_args()
    result = predict(args.text)

    print("Predicted class ID:", result)


if __name__ == "__main__":
    main()
