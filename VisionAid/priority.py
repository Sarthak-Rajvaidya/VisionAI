# COCO has 80 classes. Most (toothbrush, cake, tie...) are useless for navigation.
# Only these are announced. You can add more later.
OBSTACLES = {
    "person", "bicycle", "car", "motorcycle", "bus", "truck",
    "chair", "couch", "bed", "dining table", "bench", "potted plant",
    "fire hydrant", "suitcase", "dog", "cat",
}


def describe(det, frame_w, frame_h):
    x1, y1, x2, y2 = det["box"]

    # Direction from the horizontal centre of the box
    cx = (x1 + x2) / 2 / frame_w
    if cx < 0.35:
        direction, zone = "on your left", "left"
    elif cx > 0.65:
        direction, zone = "on your right", "right"
    else:
        direction, zone = "ahead", "ahead"

    # Rough distance from how tall the box is (bigger box = closer).
    # These cut-offs are a first guess and we will calibrate them later.
    h = (y2 - y1) / frame_h
    if h > 0.6:
        level, dist = 3, "very close"
    elif h > 0.35:
        level, dist = 2, "close"
    elif h > 0.15:
        level, dist = 1, "a few steps away"
    else:
        level, dist = 0, "far"

    urgent = level == 3 and zone == "ahead"
    label = det["label"]
    text = f"Stop! {label} ahead, very close." if urgent else f"{label} {direction}, {dist}."
    score = level * 10 + (3 if zone == "ahead" else 0) + det["conf"]

    return {"label": label, "zone": zone, "level": level,
            "urgent": urgent, "text": text, "score": score}


def prioritise(detections, frame_w, frame_h):
    """Returns relevant, near-enough detections sorted most important first."""
    items = []
    for d in detections:
        if d["label"] not in OBSTACLES:
            continue
        info = describe(d, frame_w, frame_h)
        if info["level"] == 0:
            continue
        items.append(info)
    items.sort(key=lambda i: i["score"], reverse=True)
    return items