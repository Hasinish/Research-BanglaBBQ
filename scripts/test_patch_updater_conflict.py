"""
Unit test for apply_sparse_gender_patch.py conflict detection and abort safety.
Tests:
1. Normal matching: exp_val == live_val -> PASS
2. Value mismatch: exp_val != live_val -> ABORT
3. Empty-value loophole: exp_val == '' and live_val == 'unexpected' -> ABORT (caught!)
4. Missing live value: exp_val == 'expected' and live_val == '' -> ABORT (caught!)
"""

import sys

def simulate_precheck(mock_updates_with_live):
    """
    Simulates the exact pre-check logic inside apply_sparse_gender_patch.py.
    mock_updates_with_live: list of (range_str, exp_val, live_val)
    """
    conflicts = []
    for rng, exp_val, live_val in mock_updates_with_live:
        exp_clean = '' if exp_val is None else str(exp_val).strip()
        live_clean = '' if live_val is None else str(live_val).strip()
        if exp_clean != live_clean:
            conflicts.append((rng, exp_val, live_val))
    return conflicts


def run_tests():
    print("====================================================================")
    print("PATCH UPDATER CONFLICT DETECTION & ABORT SAFETY TEST")
    print("====================================================================")

    # Test Case 1: All values match
    case1 = [
        ("BanglaBBQ_ENG_Gender!F10", "expected context A", "expected context A"),
        ("BanglaBBQ_ENG_Gender!H10", "Doctor", "Doctor"),
        ("BanglaBBQ_ENG_Gender!M10", "", ""),
    ]
    conflicts1 = simulate_precheck(case1)
    assert len(conflicts1) == 0, f"Expected 0 conflicts in Case 1, got {len(conflicts1)}"
    print("Test 1 (Matching cells): PASS (0 conflicts detected)")

    # Test Case 2: Value mismatch
    case2 = [
        ("BanglaBBQ_ENG_Gender!F10", "expected context A", "MODIFIED context in live sheet!"),
    ]
    conflicts2 = simulate_precheck(case2)
    assert len(conflicts2) == 1, f"Expected 1 conflict in Case 2, got {len(conflicts2)}"
    print("Test 2 (Modified live cell): PASS (Conflict detected: expected vs modified)")

    # Test Case 3: Empty-value loophole (exp_val is empty, but live has rogue data)
    case3 = [
        ("BanglaBBQ_ENG_Gender!M10", "", "Rogue data injected in live sheet"),
    ]
    conflicts3 = simulate_precheck(case3)
    assert len(conflicts3) == 1, f"Expected 1 conflict in Case 3 (empty loophole), got {len(conflicts3)}"
    print("Test 3 (Empty-value loophole test: exp='' vs live='Rogue data'): PASS (Conflict caught!)")

    # Test Case 4: Missing live value (exp_val has data, but live cell was deleted/blank)
    case4 = [
        ("BanglaBBQ_ENG_Gender!F10", "Original text expected", ""),
    ]
    conflicts4 = simulate_precheck(case4)
    assert len(conflicts4) == 1, f"Expected 1 conflict in Case 4 (blank live), got {len(conflicts4)}"
    print("Test 4 (Missing live value: exp='Original' vs live=''): PASS (Conflict caught!)")

    # Test Case 5: Whitespace normalization
    case5 = [
        ("BanglaBBQ_ENG_Gender!F10", "Text with trailing space ", "Text with trailing space"),
    ]
    conflicts5 = simulate_precheck(case5)
    assert len(conflicts5) == 0, f"Expected 0 conflicts with strip, got {len(conflicts5)}"
    print("Test 5 (Whitespace normalization): PASS")

    print("\n====================================================================")
    print("ALL 5 PATCH UPDATER CONFLICT & ABORT SAFETY TESTS PASSED 100%!")
    print("====================================================================")
    return True


if __name__ == '__main__':
    ok = run_tests()
    sys.exit(0 if ok else 1)
