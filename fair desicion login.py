"""Transparent, fairness-aware scholarship eligibility checker.

Academic score and family income use the same published thresholds for every
applicant. Location is retained only as optional context for human review and
cannot exclude an applicant or lower the academic standard. In production,
thresholds and reasons should be published, outcomes should be audited by
location and income band, and applicants should have an appeal process.
"""


def check_scholarship_eligibility(
	academic_score: float,
	family_income: float,
	location: str,
	*,
	minimum_score: float = 70.0,
	maximum_income: float = 60000.0,
	disadvantaged_locations: set[str] | None = None,
) -> tuple[bool, str]:
	"""Return eligibility and a transparent explanation."""
	if not 0 <= academic_score <= 100:
		raise ValueError("academic_score must be between 0 and 100")
	if family_income < 0:
		raise ValueError("family_income cannot be negative")
	if not location.strip():
		raise ValueError("location is required")
	if not 0 <= minimum_score <= 100:
		raise ValueError("minimum_score must be between 0 and 100")
	if maximum_income < 0:
		raise ValueError("maximum_income cannot be negative")

	disadvantaged_locations = {
		item.strip().casefold()
		for item in (disadvantaged_locations or set())
		if item.strip()
	}
	location_key = location.strip().casefold()
	income_eligible = family_income <= maximum_income
	score_eligible = academic_score >= minimum_score

	if income_eligible and score_eligible:
		if location_key in disadvantaged_locations:
			return True, (
				"Eligible based on academic score and family income; "
				"location recorded for contextual monitoring only."
			)
		return True, "Eligible based on academic score and family income."

	reasons = []
	if not score_eligible:
		reasons.append(f"score is below {minimum_score}")
	if not income_eligible:
		reasons.append(f"income exceeds {maximum_income}")
	context = (
		" Contextual review may be available, but location did not change this decision."
		if location_key in disadvantaged_locations
		else ""
	)
	return False, "Not eligible: " + " and ".join(reasons) + "." + context


if __name__ == "__main__":
	eligible, explanation = check_scholarship_eligibility(
		academic_score=85,
		family_income=45000,
		location="Example region",
	)
	print("Eligible" if eligible else "Not eligible")
	print(explanation)