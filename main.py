# Mini NPU Simulator
# MAC(곱하고 더하기) 연산으로 패턴을 판별하는 콘솔 프로그램

import json
import time

EPSILON = 1e-9
REPEAT = 10
DATA_FILE = "data.json"
PERF_SIZES = [3, 5, 13, 25]


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
        print("3. 패턴 생성기 (보너스)")
        choice = input("선택: ").strip()

        if choice == "1" or choice == "2" or choice == "3":
            return choice

        print("입력 오류: 1, 2, 3 중 하나를 입력하세요.")


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


def make_cross(size):
    center = size // 2
    matrix = []

    for i in range(size):
        row = []
        for j in range(size):
            if i == center or j == center:
                row.append(1.0)
            else:
                row.append(0.0)
        matrix.append(row)

    return matrix


def make_x(size):
    matrix = []

    for i in range(size):
        row = []
        for j in range(size):
            if i == j or i + j == size - 1:
                row.append(1.0)
            else:
                row.append(0.0)
        matrix.append(row)

    return matrix


def print_performance(number, sizes):
    print_section(f"[{number}] 성능 분석 (평균/{REPEAT}회)")
    print("크기       평균 시간(ms)    연산 횟수")
    print("-" * 38)

    for size in sizes:
        pattern = make_cross(size)
        filter_matrix = make_cross(size)
        elapsed_ms = measure_mac_ms(pattern, filter_matrix)
        label = f"{size}x{size}"
        print(f"{label:<10}{elapsed_ms:>14.3f}{size * size:>14}")


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

    print_performance(4, [3])


def normalize_label(label):
    text = label.strip().lower()

    if text == "+" or text == "cross":
        return "Cross"
    if text == "x":
        return "X"

    return None


def load_filters(data):
    filters = {}

    for size_key, labeled in data["filters"].items():
        size = int(size_key.split("_")[1])
        filters[size] = {}

        for label, matrix in labeled.items():
            standard = normalize_label(label)
            if standard is not None:
                filters[size][standard] = matrix

        names = ", ".join(filters[size].keys())
        print(f"✓ {size_key} 필터 로드 완료 ({names})")

    return filters


def is_square(matrix, size):
    if len(matrix) != size:
        return False

    for row in matrix:
        if len(row) != size:
            return False

    return True


def analyze_pattern(key, case, filters):
    print(f"--- {key} ---")

    try:
        size = int(key.split("_")[1])
    except (IndexError, ValueError):
        print("판정: FAIL (키 형식 오류)")
        return False, "키 형식 오류"

    if size not in filters:
        print(f"판정: FAIL (size_{size} 필터 없음)")
        return False, f"size_{size} 필터 없음"

    pattern = case["input"]
    if not is_square(pattern, size):
        print(f"판정: FAIL (패턴이 {size}x{size} 크기가 아님)")
        return False, "크기 불일치"

    expected = normalize_label(case["expected"])
    if expected is None:
        print("판정: FAIL (expected 라벨을 알 수 없음)")
        return False, "expected 라벨 오류"

    cross_score = mac(pattern, filters[size]["Cross"])
    x_score = mac(pattern, filters[size]["X"])
    result = judge(cross_score, x_score, "Cross", "X")

    print("Cross 점수:", cross_score)
    print("X 점수:", x_score)

    if result == expected:
        print(f"판정: {result} | expected: {expected} | PASS")
        return True, ""

    if result == "UNDECIDED":
        reason = "동점 규칙"
    else:
        reason = "판정 불일치"
    print(f"판정: {result} | expected: {expected} | FAIL ({reason})")
    return False, reason


def print_summary(results):
    print_section("[4] 결과 요약")

    passed_count = 0
    failed = []
    for key, passed, reason in results:
        if passed:
            passed_count += 1
        else:
            failed.append((key, reason))

    print(f"총 테스트: {len(results)}개")
    print(f"통과: {passed_count}개")
    print(f"실패: {len(failed)}개")

    if failed:
        print()
        print("실패 케이스:")
        for key, reason in failed:
            print(f"- {key}: {reason}")


def run_json_mode():
    print_section("[1] 필터 로드")

    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print("data.json을 읽을 수 없습니다:", error)
        return

    filters = load_filters(data)

    print_section("[2] 패턴 분석 (라벨 정규화 적용)")
    results = []
    for key, case in data["patterns"].items():
        passed, reason = analyze_pattern(key, case, filters)
        results.append((key, passed, reason))

    print_performance(3, PERF_SIZES)
    print_summary(results)


def print_matrix(matrix):
    for row in matrix:
        line = ""
        for value in row:
            if value == 1.0:
                line += "■ "
            else:
                line += "□ "
        print(line)


def input_odd_size():
    while True:
        text = input("크기 N (3 이상 홀수): ").strip()

        try:
            size = int(text)
        except ValueError:
            print("입력 오류: 숫자를 입력하세요.")
            continue

        if size >= 3 and size % 2 == 1:
            return size

        print("입력 오류: 3 이상의 홀수를 입력하세요.")


def run_generator_mode():
    print_section("[1] 패턴 생성")
    size = input_odd_size()
    cross = make_cross(size)
    x = make_x(size)

    print()
    print(f"Cross ({size}x{size})")
    print_matrix(cross)
    print()
    print(f"X ({size}x{size})")
    print_matrix(x)

    print_section("[2] MAC 확인 (패턴: 생성한 Cross)")
    cross_score = mac(cross, cross)
    x_score = mac(cross, x)
    print("Cross 필터 점수:", cross_score)
    print("X 필터 점수:", x_score)
    print("판정:", judge(cross_score, x_score, "Cross", "X"))

    print_performance(3, [size])


def main():
    print("╔════════════════════════════════════╗")
    print("║                                    ║")
    print("║         Mini NPU Simulator         ║")
    print("║                                    ║")
    print("╚════════════════════════════════════╝")
    mode = select_mode()

    if mode == "1":
        run_user_mode()
    elif mode == "2":
        run_json_mode()
    else:
        run_generator_mode()


try:
    main()
except (KeyboardInterrupt, EOFError):
    print()
    print("입력이 중단되었습니다. 프로그램을 종료합니다.")
