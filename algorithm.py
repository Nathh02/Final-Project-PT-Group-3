def _build_result(name: str, sequence: list[int], queue: list[int]) -> dict:
    queue_set = set(queue)
    initial_head = sequence[0]
    steps = []
    total_movement = 0

    for idx in range(len(sequence) - 1):
        start_cyl = sequence[idx]
        end_cyl = sequence[idx + 1]
        movement = abs(end_cyl - start_cyl)
        total_movement += movement

        is_boundary = end_cyl not in queue_set and end_cyl != initial_head
        to_label = f"{end_cyl} (boundary)" if is_boundary else str(end_cyl)

        steps.append(
            {
                "step": idx + 1,
                "from": start_cyl,
                "to": to_label,
                "calc": f"|{end_cyl} - {start_cyl}|",
                "movement": movement,
            }
        )

    avg_seek = total_movement / len(queue) if queue else 0.0

    return {
        "name": name,
        "sequence": sequence,
        "steps": steps,
        "total_movement": total_movement,
        "avg_seek": avg_seek,
    }


def simulate_fcfs(head: int, queue: list[int]) -> dict:
    sequence = [head] + list(queue)
    return _build_result("FCFS", sequence, queue)


def simulate_sstf(head: int, queue: list[int]) -> dict:
    remaining = list(queue)
    current = head
    sequence = [head]

    while remaining:
        closest = min(remaining, key=lambda cyl: (abs(cyl - current), cyl))
        sequence.append(closest)
        remaining.remove(closest)
        current = closest

    return _build_result("SSTF", sequence, queue)


def simulate_scan(
    head: int,
    queue: list[int],
    disk_min: int,
    disk_max: int,
    direction: str,
) -> dict:
    left = sorted([cyl for cyl in queue if cyl < head], reverse=True)
    right = sorted([cyl for cyl in queue if cyl >= head])
    sequence = [head]

    if direction == "right":
        sequence.extend(right)
        if left:
            if sequence[-1] != disk_max:
                sequence.append(disk_max)
            sequence.extend(left)
    else:
        sequence.extend(left)
        if right:
            if sequence[-1] != disk_min:
                sequence.append(disk_min)
            sequence.extend(right)

    return _build_result("SCAN (Elevator)", sequence, queue)


def run_all_algorithms(
    head: int,
    queue: list[int],
    disk_min: int,
    disk_max: int,
    direction: str,
) -> dict[str, dict]:
    return {
        "FCFS": simulate_fcfs(head, queue),
        "SSTF": simulate_sstf(head, queue),
        "SCAN (Elevator)": simulate_scan(head, queue, disk_min, disk_max, direction),
    }