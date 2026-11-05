"""
Evaluation & Accuracy Benchmark for Person 1 (Rule Engine)
Tests all 20 diverse profiles with known ground-truth labels.
Computes precision, recall, and generates evaluation_results.json.
"""

import json
import os
from engine import check_eligibility

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PROFILES_FILE = os.path.join(BASE_DIR, "test_profiles.json")
EVAL_OUT_FILE = os.path.join(BASE_DIR, "evaluation_results.json")


def run_evaluation():
    with open(TEST_PROFILES_FILE, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    total_profiles = len(test_cases)
    passed_profiles = 0
    total_decisions = 0
    correct_decisions = 0

    true_positives = 0
    false_positives = 0
    false_negatives = 0
    true_negatives = 0

    detailed_report = []

    for tc in test_cases:
        p_id = tc["profile_id"]
        desc = tc["description"]
        profile = tc["profile"]
        expected_eligible = set(tc["expected_eligible"])
        expected_ineligible = set(tc["expected_ineligible"])

        results = check_eligibility(profile)
        predicted_eligible = {r["scheme_id"] for r in results if r["eligible"]}
        predicted_ineligible = {r["scheme_id"] for r in results if not r["eligible"]}

        profile_correct = (predicted_eligible == expected_eligible) and (predicted_ineligible == expected_ineligible)
        if profile_correct:
            passed_profiles += 1

        # Calculate metrics across individual scheme decisions
        all_schemes = predicted_eligible.union(predicted_ineligible)
        for s in all_schemes:
            total_decisions += 1
            is_pred_elig = s in predicted_eligible
            is_exp_elig = s in expected_eligible

            if is_pred_elig and is_exp_elig:
                true_positives += 1
                correct_decisions += 1
            elif is_pred_elig and not is_exp_elig:
                false_positives += 1
            elif not is_pred_elig and is_exp_elig:
                false_negatives += 1
            else:
                true_negatives += 1
                correct_decisions += 1

        detailed_report.append({
            "profile_id": p_id,
            "description": desc,
            "passed": profile_correct,
            "expected_eligible": list(expected_eligible),
            "predicted_eligible": list(predicted_eligible),
            "discrepancies": list(predicted_eligible.symmetric_difference(expected_eligible))
        })

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 1.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 1.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 1.0
    profile_accuracy = (passed_profiles / total_profiles) * 100
    decision_accuracy = (correct_decisions / total_decisions) * 100

    metrics = {
        "total_test_profiles": total_profiles,
        "profiles_passed": passed_profiles,
        "profile_accuracy_percentage": profile_accuracy,
        "total_scheme_decisions": total_decisions,
        "correct_scheme_decisions": correct_decisions,
        "decision_accuracy_percentage": decision_accuracy,
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "true_negatives": true_negatives,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "edge_cases_covered": [
            "Landless agricultural laborers (0 acres)",
            "Tenant farmers with oral leases",
            "Tribal farmers with RoFR title deeds",
            "Ceiling limits (exact 10.0 acres vs 10.1 acres)",
            "Age boundaries (<18, exact 18, exact 59, exact 60, senior >75)",
            "Income-tax exclusions",
            "Out-of-state geographic residency filters",
            "Crop season notification coverage",
            "Multi-crop diversification"
        ],
        "detailed_results": detailed_report
    }

    with open(EVAL_OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("=" * 65)
    print("🏆 PERSON 1 BENCHMARK EVALUATION RESULTS 🏆")
    print("=" * 65)
    print(f"Total Profiles Evaluated : {total_profiles}")
    print(f"Profiles Passed 100%     : {passed_profiles}/{total_profiles} ({profile_accuracy:.1f}%)")
    print(f"Decision Accuracy        : {correct_decisions}/{total_decisions} ({decision_accuracy:.1f}%)")
    print(f"Precision                : {precision:.4f}")
    print(f"Recall                   : {recall:.4f}")
    print(f"F1 Score                 : {f1:.4f}")
    print("=" * 65)
    print(f"Results saved to: {EVAL_OUT_FILE}")

    return metrics


if __name__ == "__main__":
    run_evaluation()
