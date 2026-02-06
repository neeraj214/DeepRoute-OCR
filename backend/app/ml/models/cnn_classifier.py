import torch
import torch.nn as nn
from torchvision import models

class DocumentClassifier(nn.Module):
    def __init__(self, num_classes: int = 4, pretrained: bool = True):
        super(DocumentClassifier, self).__init__()
        
        # Load ResNet18
        # Use weights parameter if available (torchvision >= 0.13)
        if pretrained:
            try:
                weights = models.ResNet18_Weights.DEFAULT
            except AttributeError:
                # Fallback for older torchvision
                weights = 'DEFAULT'
        else:
            weights = None
            
        self.backbone = models.resnet18(weights=weights)
        
        # Replace the final fully connected layer
        num_ftrs = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_ftrs, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)
