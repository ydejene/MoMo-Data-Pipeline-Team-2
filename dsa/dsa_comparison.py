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

def build_transaction_dict(transactions: List[Dict]) -> Dict[int, Dict]:
    """Build dictionary with transaction_id as key for O(1) lookup."""
    transaction_dict = {}
    for idx, transaction in enumerate(transactions, start=1):
        transaction['transaction_id'] = idx
        transaction_dict[idx] = transaction
    return transaction_dict

def linear_search(transactions: List[Dict], transaction_id: int) -> Optional[Dict]:
    """
    Linear Search - O(n) time complexity
    Iterates through the entire list sequentially until finding the target.
    """
    for transaction in transactions:
        if transaction.get('transaction_id') == transaction_id:
            return transaction
    return None

def dictionary_lookup(transaction_dict: Dict[int, Dict], transaction_id: int) -> Optional[Dict]:
    """
    Dictionary Lookup - O(1) time complexity
    Uses hash table for constant-time access regardless of dataset size.
    """
    return transaction_dict.get(transaction_id)

def measure_search_time(search_func, *args, iterations: int = 100):
    """Measure average execution time for a search function."""
    times = []
    
    for _in range(iterations):
        start_time = time.perf_counter()
        search_func(*args)
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    
    avg_time = sum(times) / len(times)
    return avg_time

def run_comparison(num_searches: int = 20):
    """Run performance comparison between linear search and dictionary lookup."""
    print("DATA STRUCTURES & ALGORITHMS COMPARISON")
    print("Linear Search vs Dictionary Lookup")
    
    # Load transactions
    print("Loading transactions...")
    transactions = load_transactions()
    
    if not transactions:
        print("No transactions found. Please run xml_parser.py first.")
        return
    
    print(f"Loaded {len(transactions)} transactions")

    # Build dictionary
    print("Building dictionary index...")
    transaction_dict = build_transaction_dict(transactions)
    print(f"Dictionary built with {len(transaction_dict)} entries")
    
    # Generate random transaction IDs to search for
    max_id = len(transactions)
    search_ids = [random.randint(1, max_id) for _ in range(num_searches)]
    
    print(f"Running {num_searches} search operations...")

    # Measure Linear Search performance
    print("Testing Linear Search (O(n))...")
    linear_times = []
    for search_id in search_ids:
        avg_time = measure_search_time(linear_search, transactions, search_id, iterations=100)
        linear_times.append(avg_time)
    
    avg_linear_time = sum(linear_times) / len(linear_times)
    print(f"Average time: {avg_linear_time * 1_000_000:.2f} microseconds")