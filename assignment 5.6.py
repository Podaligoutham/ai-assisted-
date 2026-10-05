# Admission Prediction System
# Version 1: Decision only
# This version gives a simple yes/no result without explaining why.

def predict_admission_decision(entrance_score, academic_marks):
    """Return a final admission decision based on two criteria."""
    if entrance_score >= 60 and academic_marks >= 70:
        return "Selected"
    return "Rejected"


# Transparency problem:
# The first version is a black-box decision: it tells the outcome but not
# which factors mattered most or why the decision was made.
# This makes it harder for students and staff to trust or understand the system.

# Version 2: Transparent explanation
# This revised version explains the key factors influencing the decision.

def explain_admission_decision(entrance_score, academic_marks):
    """Return the decision and list the factors that influenced it."""
    reasons = []

    if entrance_score >= 60:
        reasons.append("Entrance exam score meets the minimum requirement (60).")
    else:
        reasons.append(f"Entrance exam score is below the minimum requirement (60): {entrance_score}.")

    if academic_marks >= 70:
        reasons.append("Academic marks meet the minimum requirement (70).")
    else:
        reasons.append(f"Academic marks are below the minimum requirement (70): {academic_marks}.")

    if entrance_score >= 60 and academic_marks >= 70:
        decision = "Selected"
    else:
        decision = "Rejected"

    return decision, reasons


# Example usage
students = [
    (85, 90),
    (70, 65),
    (55, 80),
    (62, 72),
]

for entrance_score, academic_marks in students:
    print(f"Student: entrance score = {entrance_score}, academic marks = {academic_marks}")
    print("Decision only:", predict_admission_decision(entrance_score, academic_marks))

    decision, reasons = explain_admission_decision(entrance_score, academic_marks)
    print("Transparent decision:", decision)
    print("Important factors:")
    for reason in reasons:
        print("-", reason)
    print("-" * 40)

