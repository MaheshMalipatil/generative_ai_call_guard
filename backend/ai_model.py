import torch
import torchaudio
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2Processor

class AIDeepFakeDetector:
    def _init_(self):
        # Load pretrained Wav2Vec2 model for deepfake detection
        model_name = "MIT/ast-finetuned-deepfake"
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)

    def predict(self, audio_file: str) -> dict:
        # Load and preprocess audio
        waveform, sample_rate = torchaudio.load(audio_file)
        if sample_rate != 16000:
            waveform = torchaudio.transforms.Resample(sample_rate, 16000)(waveform)
            sample_rate = 16000

        inputs = self.processor(waveform.squeeze(), sampling_rate=sample_rate, return_tensors="pt")

        # Run through model
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.nn.functional.softmax(logits, dim=-1)
            confidence, label_id = torch.max(probs, dim=-1)

        label = self.model.config.id2label[label_id.item()]

        return {
            "label": label,
            "confidence": round(confidence.item(),3)
}