import pandas as pd
import ast

def calculate_metrics(csv_file_path):
    def extract_counts(data, key):
        counts = {}
        for item in data[key]:
            item_dict = ast.literal_eval(item)
            for category, count in item_dict.items():
                if category not in counts:
                    counts[category] = []
                counts[category].append(count)
        return counts

    # Load the CSV file
    data = pd.read_csv(csv_file_path)

    # Extract ground truth and predicted counts
    ground_truth_counts = extract_counts(data, 'Ground Truth')
    predicted_counts = extract_counts(data, 'Predicted')

    # Standardize category names between Ground Truth and Predicted
    ground_truth_counts = {k: v for k, v in ground_truth_counts.items()}
    predicted_counts = {k.replace('rotation', ''): v for k, v in predicted_counts.items()}

    # Ensure the dictionaries have the same keys for comparison
    all_categories = set(ground_truth_counts.keys()).union(set(predicted_counts.keys()))

    # Initialize lists to hold true positives, false positives, and false negatives
    tp, fp, fn = {cat: 0 for cat in all_categories}, {cat: 0 for cat in all_categories}, {cat: 0 for cat in all_categories}

    # Calculate true positives, false positives, and false negatives
    for cat in all_categories:
        gt_values = ground_truth_counts.get(cat, [0]*len(data))
        pred_values = predicted_counts.get(cat, [0]*len(data))
        
        for gt, pred in zip(gt_values, pred_values):
            tp[cat] += min(gt, pred)
            fp[cat] += max(0, pred - gt)
            fn[cat] += max(0, gt - pred)

    # Calculate precision, recall, and F1 score for each category
    precision = {cat: tp[cat] / (tp[cat] + fp[cat]) if tp[cat] + fp[cat] > 0 else 0 for cat in all_categories}
    recall = {cat: tp[cat] / (tp[cat] + fn[cat]) if tp[cat] + fn[cat] > 0 else 0 for cat in all_categories}
    f1 = {cat: 2 * (precision[cat] * recall[cat]) / (precision[cat] + recall[cat]) if precision[cat] + recall[cat] > 0 else 0 for cat in all_categories}

    # Calculate overall precision, recall, and F1 score
    total_tp = sum(tp.values())
    total_fp = sum(fp.values())
    total_fn = sum(fn.values())

    overall_precision = total_tp / (total_tp + total_fp) if total_tp + total_fp > 0 else 0
    overall_recall = total_tp / (total_tp + total_fn) if total_tp + total_fn > 0 else 0
    overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if overall_precision + overall_recall > 0 else 0

    # Print the results
    print(f"{'Category':<20} {'Precision':<10} {'Recall':<10} {'F1 Score':<10}")
    for cat in all_categories:
        print(f"{cat:<20} {precision[cat]:<10.4f} {recall[cat]:<10.4f} {f1[cat]:<10.4f}")
    print(f"\n{'Overall':<20} {overall_precision:<10.4f} {overall_recall:<10.4f} {overall_f1:<10.4f}")

# Example usage
calculate_metrics('/Volumes/My Passport for Mac/ty_saguaro_project/results/random_30c_50o_results.csv')
