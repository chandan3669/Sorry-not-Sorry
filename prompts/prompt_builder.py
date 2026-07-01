from schemas.excuse_schema import ExcuseRequest


def build_excuse_prompt(request: ExcuseRequest) -> str:
    category = request.category.strip().lower()
    audience = request.audience.strip().lower()
    tone = request.tone.strip().lower()
    length = request.length.strip().lower()

    return (
        f"Generate a believable {tone} excuse for {category} for a {audience}. "
        f"Keep it {length} length. Return only the excuse text, with no labels."
    )
