import os
import tempfile
import numpy as np
import soundfile as sf
import cv2

from modules.data_augmentation_module import DataAugmentor

def test_augment_text():
    augmentor = DataAugmentor()
    augmentor.init()
    text = "The quick brown fox jumps over the lazy dog."
    augmented = augmentor.augment_text(text)
    assert isinstance(augmented, str)
    assert augmented != ""


def test_augment_audio():
    augmentor = DataAugmentor()
    augmentor.init()

    # Generate dummy audio data
    sr = 16000
    samples = np.random.randn(sr).astype(np.float32)  # 1 second of noise

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_input, \
         tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_output:
        sf.write(temp_input.name, samples, sr)
        augmented_path = augmentor.augment_audio(temp_input.name, temp_output.name)
        assert os.path.exists(augmented_path)

    # Cleanup
    os.remove(temp_input.name)
    os.remove(temp_output.name)


def test_augment_image():
    augmentor = DataAugmentor()
    augmentor.init()

    # Create dummy image
    dummy_image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_input, \
         tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_output:
        cv2.imwrite(temp_input.name, dummy_image)
        augmented_path = augmentor.augment_image(temp_input.name, temp_output.name)
        assert os.path.exists(augmented_path)

    # Cleanup
    os.remove(temp_input.name)
    os.remove(temp_output.name)
