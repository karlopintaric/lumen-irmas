import requests
import torch
from torchvision import transforms
import streamlit as st
from irmas_ast import FeatureExtractor
from irmas_ast import CLASSES
from irmas_ast import ASTPretrained
import os
import sys
sys.path.append(os.path.abspath(os.path.join(
    __file__, os.path.pardir, os.path.pardir)))


def load_model():
    model = ASTPretrained(n_classes=11)
    # model.load...
    model.eval()
    return model


def load_labels():
    labels = {i: CLASSES[i] for i in range(len(CLASSES))}
    return labels


class ModelServiceAST:
    def __init__(self):
        self.model = load_model()
        self.labels = load_labels()
        self.transform = transforms.Compose([
            PreprocessPipeline(target_sr=16000),
            FeatureExtractor(sr=16000)
        ])

    def get_prediction(self, audio):
        input = self.transform(audio)
        with torch.no_grad():
            output = torch.sigmoid(self.model(input))
            output = output.squeeze().numpy().astype(float)
            return dict(zip(CLASSES, output))
