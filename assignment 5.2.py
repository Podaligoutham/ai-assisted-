class EmployeePerformanceEvaluation:
    """Evaluate employee performance using weighted criteria."""

    def __init__(self):
        self.weights = {
            "project_completion": 0.50,
            "teamwork": 0.30,
            "attendance": 0.20,
        }

    def validate_score(self, value, name):
        if not 0 <= value <= 100:
            raise ValueError(f"{name} must be between 0 and 100.")

    def describe_weight_balance(self):
        """Return a structured explanation of why the weights are balanced."""
        return {
            "project_completion": "50%: Project completion most directly reflects output, delivery quality, and goal achievement.",
            "teamwork": "30%: Teamwork is essential because collaboration and communication influence project success and workplace culture.",
            "attendance": "20%: Attendance matters for reliability and commitment, but it should not outweigh actual contribution and results.",
            "summary": "Overall, these weights prioritize performance outcomes while still recognizing teamwork and dependable attendance.",
        }

    def calculate_overall_score(self, project_completion, teamwork_score, attendance):
        self.validate_score(project_completion, "Project completion")
        self.validate_score(teamwork_score, "Teamwork score")
        self.validate_score(attendance, "Attendance")

        overall_score = (
            project_completion * self.weights["project_completion"]
            + teamwork_score * self.weights["teamwork"]
            + attendance * self.weights["attendance"]
        )
        return round(overall_score, 2)

    def evaluate(self, project_completion, teamwork_score, attendance):
        score = self.calculate_overall_score(project_completion, teamwork_score, attendance)

        if score >= 85:
            rating = "Excellent"
        elif score >= 70:
            rating = "Good"
        elif score >= 55:
            rating = "Satisfactory"
        else:
            rating = "Needs Improvement"

        return {
            "project_completion": project_completion,
            "teamwork_score": teamwork_score,
            "attendance": attendance,
            "overall_score": score,
            "rating": rating,
        }


# Example usage
if __name__ == "__main__":
    evaluator = EmployeePerformanceEvaluation()
    employee_result = evaluator.evaluate(90, 80, 95)
    print("Employee evaluation:")
    for key, value in employee_result.items():
        print(f"{key}: {value}")

    print("\nWhy these weights are balanced and justifiable:")
    analysis = evaluator.describe_weight_balance()
    for criterion, explanation in analysis.items():
        if criterion != "summary":
            print(f"- {criterion.replace('_', ' ').title()}: {explanation}")
    print(analysis["summary"])
