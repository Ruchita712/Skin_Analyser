import random

def predict_skin(img_path):

    conditions=[
        "Acne",
        "Dry",
        "Oily",
        "Pigmentation",
        "Wrinkles",
        "Normal"
    ]

    condition=random.choice(conditions)

    confidence=random.randint(75,98)

    return condition,confidence