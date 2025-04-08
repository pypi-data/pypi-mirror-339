import numpy as np
import cv2
import soundfile as sf
from audiomentations import Compose as AudioCompose, AddGaussianNoise, TimeStretch, PitchShift
from albumentations import Compose as ImageCompose, HorizontalFlip, RandomBrightnessContrast, Rotate
import nlpaug.augmenter.word as naw

class DataAugmentor:
    def __init__(self):
        # Audio Augmentation Pipeline
        self.audio_augment = AudioCompose([
            AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.5),
            TimeStretch(min_rate=0.8, max_rate=1.25, p=0.5),
            PitchShift(min_semitones=-2, max_semitones=2, p=0.5)
        ])

        # Image Augmentation Pipeline
        self.image_augment = ImageCompose([
            HorizontalFlip(p=0.5),
            RandomBrightnessContrast(p=0.2),
            Rotate(limit=20, p=0.5)
        ])

        # Text Augmentation Pipeline
        self.text_augmenter = naw.SynonymAug(aug_p=0.3)

    def augment_audio(self, input_path, output_path):
        samples, sample_rate = sf.read(input_path)
        augmented = self.audio_augment(samples=samples, sample_rate=sample_rate)
        sf.write(output_path, augmented, sample_rate)
        return output_path

    def augment_image(self, input_path, output_path):
        image = cv2.imread(input_path)
        augmented = self.image_augment(image=image)["image"]
        cv2.imwrite(output_path, augmented)
        return output_path

    def augment_text(self, text):
        return self.text_augmenter.augment(text)