import os
import argparse
import torch
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from torch.utils.data import DataLoader
from torchvision import datasets
from pathlib import Path

# Adjust python path
import sys
sys.path.append(os.getcwd())

from backend.app.ml.models.cnn_classifier import DocumentClassifier
from backend.app.ml.utils import get_transforms

def evaluate_model(
    model_path: str,
    data_dir: str,
    output_dir: str = "backend/app/ml/artifacts"
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Load Classes
    classes_path = os.path.join(os.path.dirname(model_path), "classes.json")
    if not os.path.exists(classes_path):
        print(f"Error: classes.json not found at {classes_path}")
        return
        
    with open(classes_path, "r") as f:
        classes = json.load(f)
        
    print(f"Classes: {classes}")
    
    # Load Model
    model = DocumentClassifier(num_classes=len(classes)).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    
    # Data Loading
    _, val_tf = get_transforms()
    val_dir = os.path.join(data_dir, "val")
    
    if not os.path.exists(val_dir):
        print(f"Error: Validation directory not found at {val_dir}")
        return
        
    val_dataset = datasets.ImageFolder(val_dir, transform=val_tf)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    
    # Inference
    all_preds = []
    all_labels = []
    
    print("Running evaluation...")
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())
            
    # Metrics
    acc = accuracy_score(all_labels, all_preds)
    print(f"\nAccuracy: {acc:.4f}")
    
    # Check if we have enough samples for a report
    if len(all_labels) > 0:
        report = classification_report(all_labels, all_preds, target_names=classes)
        print("\nClassification Report:")
        print(report)
        
        # Confusion Matrix
        cm = confusion_matrix(all_labels, all_preds)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix')
        
        cm_path = os.path.join(output_dir, "confusion_matrix.png")
        plt.savefig(cm_path)
        print(f"Confusion matrix saved to {cm_path}")
        
        # Save metrics
        metrics = {
            "accuracy": acc,
            "classification_report": report
        }
        with open(os.path.join(output_dir, "evaluation_metrics.json"), "w") as f:
            json.dump(metrics, f, indent=2)
    else:
        print("No samples found in validation set.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, required=True, help="Path to best_model.pth")
    parser.add_argument("--data_dir", type=str, default="datasets/doc_classification")
    parser.add_argument("--output_dir", type=str, default="backend/app/ml/artifacts")
    args = parser.parse_args()
    
    evaluate_model(args.model_path, args.data_dir, args.output_dir)
