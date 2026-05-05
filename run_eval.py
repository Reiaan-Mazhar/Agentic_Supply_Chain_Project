import os
import sys
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv()

# CI/CD Environment Variables
API_URL = os.getenv("EVAL_API_URL", "http://127.0.0.1:8000/chat")
DATASET_PATH = "test_dataset.json"
CONFIG_PATH = "eval_threshold_config.json"

def load_config():
    # Fallback thresholds if file is missing
    default = {"min_faithfulness": 0.30, "min_relevancy": 0.40}
    if not os.path.exists(CONFIG_PATH):
        return default
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def run_evaluation():
    if not os.path.exists(DATASET_PATH):
        print(f"Error: {DATASET_PATH} not found!")
        sys.exit(1)

    with open(DATASET_PATH, 'r') as f:
        dataset = json.load(f)

    thresholds = load_config()
    total_score = 0
    total_questions = len(dataset)
    passed_cases = 0

    print(f"--- Starting Headless Evaluation on {total_questions} cases ---")

    for i, entry in enumerate(dataset):
        # FIX: Create a unique thread_id for every question so memory is fresh
        unique_id = f"eval_task_{i}_{int(time.time())}"
        payload = {"message": entry["question"], "thread_id": unique_id}
        try:
            resp = requests.post(API_URL, json=payload, timeout=120)
            data = resp.json()
            answer = data.get("answer")
            error_msg = data.get("error") # GET THE ERROR FIELD

            if error_msg:
                print(f"[CRITICAL ERROR] Q: {entry['question'][:20]}... Error: {error_msg}")
                continue

            if not answer:
                print(f"[FAIL] Q: {entry['question'][:20]}... Result: EMPTY")
                continue

            # Calculate keyword overlap score
            answer_clean = answer.lower()
            ground_truth = entry["ground_truth"].lower()
            
            keywords = [w for w in ground_truth.split() if len(w) > 3] # only check significant words
            match_count = sum(1 for word in keywords if word in answer_clean)
            score = match_count / len(keywords) if keywords else 0
            
            total_score += score
            if score >= thresholds["min_faithfulness"]:
                passed_cases += 1
                print(f"[PASS] Q: {entry['question'][:40]}... Score: {score:.2f}")
            else:
                print(f"[FAIL] Q: {entry['question'][:40]}... Score: {score:.2f}")

        except Exception as e:
            print(f"[ERROR] API Request failed for: {entry['question'][:20]}... Error: {e}")

    avg_score = total_score / total_questions if total_questions > 0 else 0
    print(f"\n========================================")
    print(f"FINAL AVERAGE SCORE: {avg_score:.2f}")
    print(f"REQUIRED RELEVANCY: {thresholds['min_relevancy']}")
    print(f"========================================")

    # LAB 10 REQUIREMENT: Exit code 0 if score is okay, 1 if too low
    if avg_score >= thresholds["min_relevancy"]:
        print("CI GATE STATUS: PASSED (Deployment Allowed)")
        sys.exit(0)
    else:
        print("CI GATE STATUS: FAILED (Build Blocked)")
        sys.exit(1)

if __name__ == "__main__":
    run_evaluation()