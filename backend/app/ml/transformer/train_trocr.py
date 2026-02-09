import os
import torch
import pandas as pd
from torch.utils.data import DataLoader
from torch.optim import AdamW
from tqdm import tqdm
from .dataset import OCRDataset
from .trocr_model import get_model, get_processor
# Reusing existing metrics
from backend.app.ml.metrics import compute_cer, compute_wer

def train_model(
    data_dir: str,
    output_dir: str,
    epochs: int = 5,
    batch_size: int = 4,
    learning_rate: float = 5e-5,
    model_name: str = "microsoft/trocr-small-stage1"
):
    """
    Train TrOCR model.
    """
    os.makedirs(output_dir, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load processor and model
    processor = get_processor(model_name)
    model = get_model(model_name, device)
    
    # Configure special tokens for training
    model.config.decoder_start_token_id = processor.tokenizer.cls_token_id
    model.config.pad_token_id = processor.tokenizer.pad_token_id
    model.config.vocab_size = model.config.decoder.vocab_size

    # Load data
    # Expecting labels.csv in data_dir
    labels_path = os.path.join(data_dir, "labels.csv")
    images_dir = os.path.join(data_dir, "images")
    
    if not os.path.exists(labels_path):
        print(f"Error: Labels file not found at {labels_path}")
        return
        
    df = pd.read_csv(labels_path)
    # Simple train/val split (80/20)
    train_df = df.sample(frac=0.8, random_state=42)
    val_df = df.drop(train_df.index)
    
    train_dataset = OCRDataset(root_dir=images_dir, df=train_df, processor=processor)
    val_dataset = OCRDataset(root_dir=images_dir, df=val_df, processor=processor)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)

    optimizer = AdamW(model.parameters(), lr=learning_rate)

    best_cer = float('inf')

    for epoch in range(epochs):
        print(f"\nEpoch {epoch+1}/{epochs}")
        
        # Training
        model.train()
        train_loss = 0.0
        pbar = tqdm(train_loader, desc="Training")
        
        for batch in pbar:
            pixel_values = batch["pixel_values"].to(device)
            labels = batch["labels"].to(device)
            
            outputs = model(pixel_values=pixel_values, labels=labels)
            loss = outputs.loss
            
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            
            train_loss += loss.item()
            pbar.set_postfix({'loss': loss.item()})
            
        avg_train_loss = train_loss / len(train_loader)
        print(f"Average Train Loss: {avg_train_loss:.4f}")
        
        # Validation
        model.eval()
        total_cer = 0.0
        total_wer = 0.0
        count = 0
        
        with torch.no_grad():
            for batch in tqdm(val_loader, desc="Validation"):
                pixel_values = batch["pixel_values"].to(device)
                labels = batch["labels"].to(device)
                
                # Generate
                generated_ids = model.generate(pixel_values)
                generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)
                
                # Decode labels (replace -100 with pad token id first)
                label_ids = labels.cpu().numpy()
                label_ids[label_ids == -100] = processor.tokenizer.pad_token_id
                ground_truth_text = processor.batch_decode(label_ids, skip_special_tokens=True)
                
                for pred, gt in zip(generated_text, ground_truth_text):
                    cer = compute_cer(gt, pred)
                    wer = compute_wer(gt, pred)
                    total_cer += cer
                    total_wer += wer
                    count += 1
        
        avg_cer = total_cer / count if count > 0 else 0
        avg_wer = total_wer / count if count > 0 else 0
        
        print(f"Validation CER: {avg_cer:.4f}")
        print(f"Validation WER: {avg_wer:.4f}")
        
        # Save best model
        if avg_cer < best_cer:
            best_cer = avg_cer
            print("New best model! Saving...")
            model.save_pretrained(output_dir)
            processor.save_pretrained(output_dir)
            
    model.save_pretrained(output_dir)
    processor.save_pretrained(output_dir)
    
    # Log Experiment
    try:
        from backend.app.ml.experiments.experiment_logger import ExperimentLogger
        logger = ExperimentLogger()
        logger.log_experiment(
            model_name="trocr-small-stage1",
            model_version="v1.0",
            dataset_version="ocr_train_v1",
            task="ocr_finetuning",
            hyperparameters={
                "epochs": epochs,
                "batch_size": batch_size,
                "learning_rate": learning_rate,
                "base_model": model_name
            },
            metrics={"best_cer": best_cer},
            output_artifacts=output_dir
        )
    except Exception as e:
        print(f"Warning: Failed to log experiment: {e}")
        
    print(f"Training finished. Best CER: {best_cer}")
