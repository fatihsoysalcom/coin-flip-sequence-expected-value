import random
import sys

def simulate_flips(target_sequence, num_simulations):
    """
    Simulates coin flips to find the average number of flips to achieve a target sequence.
    'H' for Heads, 'T' for Tails.
    """
    target_len = len(target_sequence)
    total_flips = 0

    for _ in range(num_simulations):
        current_sequence = []
        flips_count = 0
        while True:
            flips_count += 1
            # Simulate a fair coin flip (0 for Tails, 1 for Heads)
            flip_result = 'H' if random.random() < 0.5 else 'T'
            current_sequence.append(flip_result)

            # Keep only the last 'target_len' flips to check for the sequence
            if len(current_sequence) > target_len:
                current_sequence.pop(0) # Remove the oldest flip

            # Check if the current sequence matches the target
            if len(current_sequence) == target_len and "".join(current_sequence) == target_sequence:
                total_flips += flips_count
                break
    
    return total_flips / num_simulations

def calculate_expected_value_theoretical(target_sequence):
    """
    Calculates the theoretical expected number of flips for a fair coin
    to achieve a target sequence using the overlap method.
    E[S] = sum_{k=1 to |S|} 2^k * I(S_k = S_k')
    where S_k is the prefix of S of length k, and S_k' is the suffix of S of length k.
    I is 1 if they match, 0 otherwise.
    """
    expected_value = 0
    target_len = len(target_sequence)

    # Iterate through all possible overlaps (from length 1 up to target_len)
    for k in range(1, target_len + 1):
        prefix = target_sequence[:k] # Prefix of length k
        suffix = target_sequence[target_len - k:] # Suffix of length k

        # If the prefix matches the suffix, it contributes to the expected value
        if prefix == suffix:
            expected_value += (2 ** k) # Contribution is 2^k for a fair coin
            # This is where the internal overlaps (or lack thereof) within the sequence
            # affect the expected value. For 'HH', 'H' overlaps 'H' (k=1) and 'HH' overlaps 'HH' (k=2).
            # For 'HTH', 'H' overlaps 'H' (k=1) and 'HTH' overlaps 'HTH' (k=3),
            # but 'HT' does not overlap 'TH' (k=2).
    return expected_value

if __name__ == "__main__":
    TARGET_HH = "HH"
    TARGET_HTH = "HTH"
    NUM_SIMULATIONS = 100000 # Number of times to run the simulation for averaging

    print(f"--- Coin Flip Sequence Expected Value ---")
    print(f"Simulating {NUM_SIMULATIONS} runs for each sequence.\n")

    # --- HH Sequence ---
    print(f"Target Sequence: '{TARGET_HH}'")
    simulated_hh = simulate_flips(TARGET_HH, NUM_SIMULATIONS)
    theoretical_hh = calculate_expected_value_theoretical(TARGET_HH)
    print(f"  Simulated Average Flips: {simulated_hh:.2f}")
    print(f"  Theoretical Expected Flips: {theoretical_hh:.2f}\n") # E[HH] = 6

    # --- HTH Sequence ---
    print(f"Target Sequence: '{TARGET_HTH}'")
    simulated_hth = simulate_flips(TARGET_HTH, NUM_SIMULATIONS)
    theoretical_hth = calculate_expected_value_theoretical(TARGET_HTH)
    print(f"  Simulated Average Flips: {simulated_hth:.2f}")
    print(f"  Theoretical Expected Flips: {theoretical_hth:.2f}\n") # E[HTH] = 10

    print("Observation: The expected number of flips for 'HH' (6) is significantly lower")
    print("than for 'HTH' (10), despite 'HTH' being only one flip longer. This difference")
    print("arises from the internal overlaps within the sequences, as demonstrated by the")
    print("theoretical calculation method.")
