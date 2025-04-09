import torch
from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM
import onnxruntime
import requests
from tqdm import tqdm
from pathlib import Path
# local imports
from .log import logger


def load_quantized_model(model_dir):
    """
    Load the quantized model and tokenizer from the specified directory.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = ORTModelForSeq2SeqLM.from_pretrained(model_dir, use_cache=False)
    return model, tokenizer


def download_model(path_or_url: str) -> str:
    # Determine local cache directory
    cache_dir = Path.home() / ".cache" / ".steno" / "models"
    cache_dir.mkdir(parents=True, exist_ok=True)

    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        model_path = cache_dir / Path(path_or_url).name
        if model_path.exists():
            # Check if the model is already downloaded
            logger.debug(f"Model already exists at {model_path}")
            return str(model_path)
        # mkdir for model_path
        model_path.mkdir(parents=True, exist_ok=True)
        # files to download are located in the files.json file in the model directory
        files = requests.get(path_or_url + "/files.json").json()
        # now we need to download each file
        logger.info(f"Downloading model locally. This will only happen once.")
        for filename in files:
            file_path = model_path / filename
            file_url = path_or_url + "/" + filename
            if not file_path.exists():
                response = requests.get(file_url, stream=True)
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                with open(file_path, "wb") as f, tqdm(
                    desc="Downloading",
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                ) as progress_bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                        progress_bar.update(len(chunk))

        return str(model_path)

    # If already local, return as-is
    return path_or_url


class ModelRunner(object):
    """
    A class to encapsulate the model loading and inference logic.
    """

    def __init__(self, model_dir: str = None):
        self.model_dir = model_dir or "https://steno-models.s3.amazonaws.com/steno-one/quantized"
        self.model_path = download_model(self.model_dir)
        self.model, self.tokenizer = load_quantized_model(self.model_path)

    def load_quantized_model(self, model_dir):
        """
        Load the quantized model and tokenizer from the specified directory.
        """
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_dir)

        # Load ONNX encoder and decoder sessions
        encoder_session = onnxruntime.InferenceSession(
            f"{model_dir}/encoder_model.onnx")
        decoder_session = onnxruntime.InferenceSession(
            f"{model_dir}/decoder_model.onnx")
        return tokenizer, encoder_session, decoder_session

    def run(self, text: str) -> str:
        """
        Runs the inference on some input_text
        """
        # Preprocess the input text
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            max_length=min(len(text), 64),
            truncation=True,
            padding="max_length"
        )

        # Perform inference
        with torch.no_grad():
            outputs = self.model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                # max_length=32,
                max_new_tokens=len(text),
                num_beams=4,
                early_stopping=True
            )

        # Decode the output
        decoded_output = self.tokenizer.decode(
            outputs[0], skip_special_tokens=True)
        return decoded_output


# if __name__ == "__main__":
#     # Path to the quantized model directory
#     # Updated to match train.py output
#     quantized_model_dir = "steno-one/quantized_model"

#     # Load the quantized model and tokenizer
#     # model, tokenizer = load_quantized_model(quantized_model_dir)

#     # Example input text
#     input_text = "compress-sentence: This is an example input sentence."

#     # Run inference
#     output = run_inference(model, tokenizer, input_text)
#     print("Input:", input_text)
#     print("Output:", output)
