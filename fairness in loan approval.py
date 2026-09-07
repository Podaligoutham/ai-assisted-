import numpy as np  # type: ignore

np.random.seed(42)


def generate_dataset(n=500):
    income = np.random.uniform(20000, 180000, n)
    age = np.random.randint(21, 70, n)
    employment_status = np.random.choice([0, 1], n, p=[0.25, 0.75])
    credit_score = np.clip(np.random.normal(680, 80, n), 300, 850)
    loan_amount = np.random.uniform(5000, 250000, n)

    gender = np.random.choice(["Female", "Male"], n, p=[0.5, 0.5])
    religion = np.random.choice(["Christian", "Muslim", "Hindu", "Other"], n, p=[0.35, 0.25, 0.25, 0.15])
    race = np.random.choice(["White", "Black", "Asian", "Hispanic", "Other"], n, p=[0.55, 0.18, 0.12, 0.1, 0.05])

    return {
        "income": income,
        "age": age,
        "employment_status": employment_status,
        "credit_score": credit_score,
        "loan_amount": loan_amount,
        "gender": gender,
        "religion": religion,
        "race": race,
    }


def _normalize(values):
    min_v = np.min(values)
    max_v = np.max(values)
    return (values - min_v) / (max_v - min_v + 1e-8)


def biased_approval(data):
    income_score = _normalize(data["income"])
    credit_score = _normalize(data["credit_score"])
    employment_score = data["employment_status"].astype(float)
    loan_ratio = np.clip(data["loan_amount"] / (data["income"] + 1), 0, 2)
    loan_ratio_score = 1 - _normalize(loan_ratio)

    base_score = (
        0.38 * income_score +
        0.40 * credit_score +
        0.12 * employment_score +
        0.10 * loan_ratio_score
    )

    bias_adjustment = np.zeros(len(data["income"]))
    bias_adjustment[data["gender"] == "Female"] -= 0.18
    bias_adjustment[data["religion"] == "Muslim"] -= 0.16
    bias_adjustment[data["race"] == "Black"] -= 0.20
    bias_adjustment[data["race"] == "Hispanic"] -= 0.12

    final_score = base_score + bias_adjustment
    return final_score >= 0.60


def fair_approval(data):
    income_score = _normalize(data["income"])
    credit_score = _normalize(data["credit_score"])
    employment_score = data["employment_status"].astype(float)
    loan_ratio = np.clip(data["loan_amount"] / (data["income"] + 1), 0, 2)
    loan_ratio_score = 1 - _normalize(loan_ratio)

    financial_score = (
        0.42 * income_score +
        0.42 * credit_score +
        0.10 * employment_score +
        0.06 * loan_ratio_score
    )

    return financial_score >= 0.62


def approval_rate_by_group(approved, group_values):
    groups = np.unique(group_values)
    result = {}
    for group in groups:
        mask = group_values == group
        result[group] = np.mean(approved[mask])
    return result


def print_group_rates(label, approved, groups):
    print(f"\n{label} approval rates by group:")
    for group, rate in approval_rate_by_group(approved, groups).items():
        print(f"  {group}: {rate:.2%}")


def group_rate_gap(approved, groups):
    rates = approval_rate_by_group(approved, groups)
    if not rates:
        return 0.0
    return max(rates.values()) - min(rates.values())


def main():
    data = generate_dataset()

    biased_decisions = biased_approval(data)
    fair_decisions = fair_approval(data)

    print("Loan Approval Fairness Analysis")
    print("=" * 40)
    print("Overall approval rate using sensitive attributes:")
    print(f"  Biased model: {np.mean(biased_decisions):.2%}")
    print(f"  Fair model: {np.mean(fair_decisions):.2%}")

    print("\nBiased model approval rates by demographic group:")
    print_group_rates("Biased model", biased_decisions, data["gender"])
    print_group_rates("Biased model", biased_decisions, data["religion"])
    print_group_rates("Biased model", biased_decisions, data["race"])

    print("\nBiased model approval gap by sensitive attribute:")
    for name, values in [("gender", data["gender"]), ("religion", data["religion"]), ("race", data["race"])]:
        gap = group_rate_gap(biased_decisions, values)
        print(f"  {name}: {gap:.2%} difference between the highest and lowest approval rates")

    print("\nFair model approval rates by demographic group:")
    print_group_rates("Fair model", fair_decisions, data["gender"])
    print_group_rates("Fair model", fair_decisions, data["religion"])
    print_group_rates("Fair model", fair_decisions, data["race"])

    print("\nFair model approval gap by sensitive attribute:")
    for name, values in [("gender", data["gender"]), ("religion", data["religion"]), ("race", data["race"])]:
        gap = group_rate_gap(fair_decisions, values)
        print(f"  {name}: {gap:.2%} difference between the highest and lowest approval rates")

    print("\nFair model uses only relevant financial factors:")
    print("  - income")
    print("  - credit score")
    print("  - employment status")
    print("  - loan amount relative to income")
    print("  - age is excluded because it is not a direct financial factor")

    print("\nInterpretation:")
    print("  The biased model uses gender, religion, and race as direct inputs to reduce approval for some groups.")
    print("  This can create unfair decisions because protected attributes are not relevant to loan repayment ability.")
    print("  The revised model removes sensitive attributes and uses only financial signals, making decisions more justifiable and fair.")


if __name__ == "__main__":
    main()
