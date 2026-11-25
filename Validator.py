def parse_queue(raw_queue: str) -> tuple[list[int] | None, str | None]:
    tokens = raw_queue.replace(",", " ").split()
    if not tokens:
        return None, "Please enter at least one cylinder request."

    queue: list[int] = []
    for token in tokens:
        try:
            queue.append(int(token))
        except ValueError:
            return None, f"Invalid cylinder value '{token}'. Enter whole integers only."

    return queue, None


def validate_disk_inputs(
    raw_min: str,
    raw_max: str,
    raw_head: str,
    raw_queue: str,
    raw_direction: str,
) -> tuple[tuple[int, int, int, list[int], str] | None, str | None]:
    try:
        disk_min = int(raw_min.strip())
        disk_max = int(raw_max.strip())
        head = int(raw_head.strip())
    except ValueError:
        return None, "Disk minimum, disk maximum, and initial head must be valid integers."

    if disk_min < 0 or disk_min >= disk_max:
        return None, "Disk minimum must be >= 0 and strictly less than disk maximum."

    if not (disk_min <= head <= disk_max):
        return None, f"Initial head position must be within [{disk_min}, {disk_max}]."

    queue, queue_err = parse_queue(raw_queue)
    if queue_err or queue is None:
        return None, queue_err

    out_of_bounds = [cyl for cyl in queue if not (disk_min <= cyl <= disk_max)]
    if out_of_bounds:
        return None, f"Cylinders {out_of_bounds} are outside disk range [{disk_min}, {disk_max}]."

    direction = raw_direction.strip().lower()
    if direction not in ("left", "right"):
        return None, "SCAN direction must be 'left' or 'right'."

    return (disk_min, disk_max, head, queue, direction), None