import math


def attendance_score(attendance: int) -> float:
    if attendance >= 2:
        score = attendance**2 / 10
    else:
        score = 0
    return score


def notice_score(notice: int) -> float:
    return min([math.log(notice+2, 93.5), 1])


def calculate_points(notice: int, attendance: int) -> float:
    n = notice_score(notice)
    a = attendance_score(attendance)
    return round(a * n, 1)


if __name__ == '__main__':
    att = 5
    noti = 1
    print(f"attendance: {att}, notice: {noti}, score: {calculate_points(noti, att)}")
    print(notice_score(1))
