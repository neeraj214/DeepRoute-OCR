import sys
import os
import json
import argparse
from tabulate import tabulate

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.ml.evaluate import evaluate_dataset

def main():
    parser = argparse.ArgumentParser(description="Run OCR Evaluation")
    parser.add_argument("--dataset", default="datasets/ocr_eval", help="Path to dataset directory")
    parser.add_argument("--output", default="evaluation_results.json", help="Path to save JSON results")
    args = parser.parse_args()
    
    dataset_path = os.path.abspath(args.dataset)
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset directory not found at {dataset_path}")
        return

    print(f"Running evaluation on dataset: {dataset_path}")
    results = evaluate_dataset(dataset_path)
    
    if "error" in results:
        print(f"Error: {results['error']}")
        return
        
    # Print Summary
    metrics = results["metrics"]
    print("\n" + "="*40)
    print(f"OCR EVALUATION REPORT ({results['model']})")
    print("="*40)
    print(f"Total Images:      {results['dataset_size']}")
    print(f"Average CER:       {metrics['avg_cer']:.4f}")
    print(f"Average WER:       {metrics['avg_wer']:.4f}")
    print(f"Avg Time (ms):     {metrics['avg_time_ms']:.2f}")
    print("="*40 + "\n")
    
    # Detailed Table (Top 10 worst by CER)
    details = results["details"]
    details.sort(key=lambda x: x["cer"], reverse=True)
    
    table_data = []
    for item in details[:5]:
        table_data.append([
            item["filename"],
            f"{item['cer']:.4f}",
            f"{item['wer']:.4f}",
            item["ground_truth"][:30] + "..." if len(item["ground_truth"]) > 30 else item["ground_truth"],
            item["predicted"][:30] + "..." if len(item["predicted"]) > 30 else item["predicted"]
        ])
        
    print("Top 5 High Error Files:")
    print(tabulate(table_data, headers=["File", "CER", "WER", "Truth", "Pred"], tablefmt="grid"))
    
    # Save Results
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to {args.output}")

if __name__ == "__main__":
    main()
