# Mini NPU Simulator
# MAC(곱하고 더하기) 연산으로 패턴을 판별하는 콘솔 프로그램


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


def run_user_mode():
    print_section("[1] 필터 입력")
    print("(준비 중) 다음 단계에서 만듭니다.")


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