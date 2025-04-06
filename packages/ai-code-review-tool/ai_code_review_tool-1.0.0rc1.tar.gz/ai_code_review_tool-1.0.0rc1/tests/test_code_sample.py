# src/ai_code_review_tool/test_code_sample.py

def complex_function(a, b, c):
    """A complex function with several issues."""
    # 1. Nested if statements that could be refactored
    if a > 0:
        if b < 10:
            if c == 0:
                return a + b
            else:
                return a + b + c
        elif b == 10:
            return a - b
    else:
        return a * b * c

    return 0
