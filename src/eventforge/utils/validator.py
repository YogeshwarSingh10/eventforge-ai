def deduplicate(items, key):
    seen = set()
    unique = []

    for item in items:
        val = getattr(item, key)
        if val in seen:
            continue
        seen.add(val)
        unique.append(item)

    return unique


def clean_speakers(speakers):
    speakers = deduplicate(speakers, "name")
    return [s for s in speakers if len(s.name.split()) >= 2]


def clean_exhibitors(exhibitors):
    cleaned = []

    for e in exhibitors:
        name = e.name.lower()

        if any(x in name for x in ["police", "gov", "department"]):
            continue
        if len(e.name) < 3:
            continue
        if any(c in e.name for c in ["\x1a", "�"]):
            continue

        cleaned.append(e)

    return cleaned


def clean_venues(venues, audience_size):
    # cleaned = []

    # for v in venues:
    #     name = v.name.lower()
        
    #     if v.capacity < audience_size or any(x in v.name.lower() for x in ["group", "solutions"]):
    #         continue

    # return cleaned
    return venues