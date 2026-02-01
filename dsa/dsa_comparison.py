"""
Data Structures & Algorithms Comparison
Compares Linear Search vs Dictionary Lookup for transaction searching.
Demonstrates the efficiency difference between O(n) and O(1) operations.
"""

import json
import time
import random
from typing import List, Dict, Optional


def load_transactions(file_path: str = '..data/processed/transactions.json') -> List[Dict]:
    """Load transactions from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        return []

def linear_search(transactions: List[Dict], transaction_id: int) -> Optional[Dict]:
    """
    Linear Search - O(n) time complexity
    Iterates through the entire list sequentially until finding the target.
    """
    for transaction in transactions:
        if transaction.get('transaction_id') == transaction_id:
            return transaction
    return None

def measure_search_time(search_func, *args, iterations: int = 100):
    """Measure average execution time for a search function."""
    times = []
    
    for _ in range(iterations):
        start_time = time.perf_counter()
        search_func(*args)
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    
    avg_time = sum(times) / len(times)
    return avg_time
