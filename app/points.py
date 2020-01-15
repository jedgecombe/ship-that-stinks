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


def calculate_points(cycle: int, notice: int, attendance: int) -> float:
    score = notice_score(cycle, notice) * attendance_score(cycle, attendance)
    if cycle == 1:
        score = round(score, 1)
    else:
        score = round(score, 0)
    return score


if __name__ == '__main__':
    att = 3
    noti = 0
    print(f"attendance: {attendance_score(2, att)}, notice: {notice_score(2, noti)}, score: {calculate_points(2, noti, att)}")

