from dataclasses import dataclass

@dataclass
class RoadmapWeek:
    label: str
    slugs: list[str]

def build_roadmap(ordered_slugs: list[str], hours_per_week: int, hours_map: dict[str, int]) -> list[RoadmapWeek]:
    # same logic as your JS, but deterministic & testable
    weeks: list[RoadmapWeek] = []
    curr: list[str] = []
    w_hrs = 0
    w_num = 1

    cap = max(1, hours_per_week) * 2  # pack 2-week blocks like your UI
    for slug in ordered_slugs:
        sh = max(1, int(hours_map.get(slug, 6)))
        if w_hrs + sh > cap and curr:
            weeks.append(RoadmapWeek(label=f"Week {w_num}–{w_num+1}", slugs=curr))
            w_num += 2
            curr = [slug]
            w_hrs = sh
        else:
            curr.append(slug)
            w_hrs += sh

    if curr:
        weeks.append(RoadmapWeek(label=f"Week {w_num}–{w_num+1}", slugs=curr))

    return weeks