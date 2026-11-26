# Mini NPU Simulator
# MAC(곱하고 더하기) 연산으로 패턴을 판별하는 콘솔 프로그램

import time

EPSILON = 1e-9
REPEAT = 10


def print_section(title):
    print()
    print("#" + "-" * 39)
    print("# " + title)
    print("#" + "-" * 39)


def select_mode():
    while True:
        print()
        print("[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        choice = input("선택: ").strip()

        if choice == "1" or choice == "2":
            return choice

        print("입력 오류: 1 또는 2를 입력하세요.")


def input_matrix(name, size):
    print(name + " (" + str(size) + "줄 입력, 공백 구분)")
    matrix = []

    while len(matrix) < size:
        parts = input().split()

        if len(parts) != size:
            print("입력 형식 오류: 각 줄에 " + str(size) + "개의 숫자를 공백으로 구분해 입력하세요.")
            continue

        row = []
        try:
            for part in parts:
                row.append(float(part))
        except ValueError:
            print("입력 형식 오류: 숫자만 입력하세요.")
            continue

        matrix.append(row)

    return matrix


def mac(pattern, filter_matrix):
    size = len(pattern)
    total = 0.0

    for i in range(size):
        for j in range(size):
            total += pattern[i][j] * filter_matrix[i][j]

    return total


def judge(score_a, score_b, label_a, label_b):
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"

    if score_a > score_b:
        return label_a

    return label_b


def measure_mac_ms(pattern, filter_matrix):
    start = time.perf_counter()

    for _ in range(REPEAT):
        mac(pattern, filter_matrix)

    end = time.perf_counter()
    return (end - start) * 1000 / REPEAT


def run_user_mode():
    size = 3

    print_section("[1] 필터 입력")
    filter_a = input_matrix("필터 A", size)
    print()
    filter_b = input_matrix("필터 B", size)
    print("✓ 필터 A, B 저장 완료")

    print_section("[2] 패턴 입력")
    pattern = input_matrix("패턴", size)
    print("✓ 패턴 저장 완료")

    print_section("[3] MAC 결과")
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    print("A 점수:", score_a)
    print("B 점수:", score_b)

    elapsed_ms = measure_mac_ms(pattern, filter_a)
    print(f"연산 시간(평균/{REPEAT}회): {elapsed_ms:.3f} ms")

    result = judge(score_a, score_b, "A", "B")
    if result == "UNDECIDED":
        print("판정: 판정 불가 (|A-B| < 1e-9)")
    else:
        print("판정:", result)


def run_json_mode():
    print_section("[1] 필터 로드")
    print("(준비 중) 다음 단계에서 만듭니다.")


def main():
    print("=== Mini NPU Simulator ===")
    mode = select_mode()

    if mode == "1":
        run_user_mode()
    else:
        run_json_mode()


try:
    main()
except (KeyboardInterrupt, EOFError):
    print()
    print("입력이 중단되었습니다. 프로그램을 종료합니다.")
