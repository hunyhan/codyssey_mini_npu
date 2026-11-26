# 크기별 성능 분석 표 (PR #8)

[← README로 돌아가기](../README.md)

3×3, 5×5, 13×13, 25×25 크기별로 10회 평균 시간과 연산 횟수(N²)를 표로 보여 줍니다.

## 브랜치, 성능 표 코드, 실행

![실행 ①: 모드 1, 패턴 입력 중 1 0은 개수 오류 후 다시 받음, A 1.0, B 5.0, 판정 B, [4] 성능 분석 (평균/10회) 표에 3x3 0.001 9](images/72-run-mode1-perf.png)

*실행 ①: 모드 1, 패턴 입력 중 1 0은 개수 오류 후 다시 받음, A 1.0, B 5.0, 판정 B, [4] 성능 분석 (평균/10회) 표에 3x3 0.001 9*

![실행 ②: 모드 2, 패턴 분석 6개 아래 [3] 성능 분석 (평균/10회) 표에 3x3 0.001 9, 5x5 0.002 25, 13x13 0.007 169, 25x25 0.023 625](images/72-run-mode2-perf.png)

*실행 ②: 모드 2, 패턴 분석 6개 아래 [3] 성능 분석 (평균/10회) 표에 3x3 0.001 9, 5x5 0.002 25, 13x13 0.007 169, 25x25 0.023 625*

## 커밋, push, PR, 정리

![git pull로 c1cdb70..e11c4cf Fast-forward main.py 27 insertions, branch -d, fetch --prune의 - [deleted], 그래프 e11c4cf Merge pull request #8, 5532866 Feat: 크기별 성능 분석 표 구현](images/72-merge-log.png)

*git pull로 c1cdb70..e11c4cf Fast-forward main.py 27 insertions, branch -d, fetch --prune의 - [deleted], 그래프 e11c4cf Merge pull request #8, 5532866 Feat: 크기별 성능 분석 표 구현*
