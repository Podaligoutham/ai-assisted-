def get_choice(prompt, options):
    """Prompt the user to choose from a list of labeled options."""
    while True:
        print(prompt)
        for key, label in options.items():
            print(f"   {key}) {label}")

        choice = input("Enter your choice: ").strip()
        if choice in options:
            return choice, options[choice]
        print("Please select a valid option.")


def get_optional_text(prompt, empty_default="No response provided"):
    """Collect an optional free-text response."""
    response = input(prompt).strip()
    return response if response else empty_default


def get_feedback():
    """Collect inclusive user feedback with accessible prompts."""
    print("User Feedback Form")
    print("Please answer the questions below. You may choose an option or type your own response.")
    print("All questions are optional unless marked otherwise.")

    # Question 1: ease of use
    rating_choice, rating = get_choice(
        "\n1) How easy was it to complete this form?",
        {
            "1": "Very difficult",
            "2": "Difficult",
            "3": "Neutral",
            "4": "Easy",
            "5": "Very easy",
            "6": "Prefer not to answer",
        },
    )

    # Question 2: device used
    device_choice, device = get_choice(
        "\n2) What device did you use to access this form?",
        {
            "1": "Smartphone",
            "2": "Tablet",
            "3": "Laptop",
            "4": "Desktop computer",
            "5": "Other",
            "6": "Prefer not to answer",
        },
    )
    if device == "Other":
        device = get_optional_text("Please describe the device: ", "Other")
    elif device == "Prefer not to answer":
        device = "Prefer not to answer"

    # Question 3: accessibility support
    support_choice, support = get_choice(
        "\n3) Which support or adjustments helped you complete this form?",
        {
            "1": "Screen reader",
            "2": "Keyboard navigation",
            "3": "Magnification or zoom",
            "4": "Closed captions or transcript",
            "5": "No support needed",
            "6": "None of the above",
            "7": "Prefer not to answer",
            "8": "Other",
        },
    )
    if support == "Other":
        support = get_optional_text("Please describe the support or adjustment: ", "Other")

    # Question 4: open feedback
    print("\n4) What could we do to make this experience clearer, easier, or more inclusive?")
    suggestions = get_optional_text(
        "Type your response here (optional): ",
        "No additional comments provided",
    )

    # Question 5: context
    context_choice, context = get_choice(
        "\n5) Which option best describes your situation when using this service?",
        {
            "1": "Student",
            "2": "Employee",
            "3": "Parent or caregiver",
            "4": "Retired",
            "5": "Self-described",
            "6": "Prefer not to answer",
        },
    )
    if context == "Self-described":
        context = get_optional_text("Please describe your situation: ", "Self-described")

    # Question 6: follow-up preference
    follow_up_choice, follow_up = get_choice(
        "\n6) Would you like to be contacted about this feedback?",
        {
            "1": "Yes, I would like a follow-up",
            "2": "No, I do not want a follow-up",
            "3": "I prefer not to answer",
        },
    )

    feedback = {
        "ease_of_use": rating,
        "device_used": device,
        "accessibility_support": support,
        "feedback": suggestions,
        "context": context,
        "follow_up": follow_up,
    }

    print("\nThank you for your feedback.")
    for key, value in feedback.items():
        print(f"- {key.replace('_', ' ').title()}: {value}")

    return feedback


if __name__ == "__main__":
    get_feedback()
