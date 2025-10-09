import spacy


def download_spacy_model():
    """Download the English spaCy model programmatically."""
    print("Downloading en_core_web_sm model...")
    try:
        # This will download and link the model
        spacy.cli.download("en_core_web_sm")
        print("Successfully downloaded and linked 'en_core_web_sm' model.")

        # Verify the model is installed correctly
        nlp = spacy.load("en_core_web_sm")
        print("Model loaded successfully!")
        print(f"spaCy version: {spacy.__version__}")
        print(f"Model version: {nlp.meta['version']}")

    except Exception as e:
        print(f"Error downloading or loading the model: {e}")
        print("You might need to run this script with administrator/root privileges.")


if __name__ == "__main__":
    download_spacy_model()
