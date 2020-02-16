import math

# TODO tidy up this total mess

def attendance_score(cycle: int, attendance: int) -> float:
    def cycle1(att: int) -> float:
        if att >= 2:
            score = att ** 2 / 10
        else:
            score = 0
        return score

    def cycle2(att: int) -> float:
        if att >= 2:
            score = att ** 2.5
        else:
            score = 0
        return score

    if cycle == 1:
        return cycle1(attendance)
    else:
        return cycle2(attendance)


def notice_score(cycle: int, notice: int) -> float:
    return min([math.log(notice + 2, 93.5), 1])


def calculate_points(cycle: int, notice: int, attendance: int, days: float = 0) -> float:
    score = notice_score(cycle, notice) * attendance_score(cycle, attendance)
    day_adj = multi_day_adj(days, fract=0.69)
    score = score * day_adj
    if cycle == 1:
        score = round(score, 1)
    else:
        score = round(score, 0)
    return score


def multi_day_adj(days: float, fract: float) -> float:
    days = math.ceil(days)
    return sum([fract ** d for d in range(days)])


if __name__ == '__main__':
    att = 3
    noti = 0
    days = 2.1
    print(f"attendance: "
          f"{attendance_score(2, att)}, "
          f"notice: {notice_score(2, noti)}, "
          f"day adj: {multi_day_adj(days, 0.69)} "
          f"total score: {calculate_points(2, noti, att, days)}")

