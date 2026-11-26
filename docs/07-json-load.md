# data.json 로드와 라벨 정규화 (PR #6)

[← README로 돌아가기](../README.md)

`data.json`의 필터를 크기별로 읽고, `cross`, `+`, `x` 같은 라벨을 `Cross`, `X`로 맞췄습니다. 파일이 없을 때는 안내 후 종료합니다.

## 브랜치, JSON 로드 코드, 실행

![실행 ①: 모드 2, ✓ size_5/size_13/size_25 필터 로드 완료 (Cross, X), [2] 라벨 정규화 확인에서 size_5_1 : x → X, size_5_2 : + → Cross 등 6줄](images/70-run-json-load.png)

*실행 ①: 모드 2, ✓ size_5/size_13/size_25 필터 로드 완료 (Cross, X), [2] 라벨 정규화 확인에서 size_5_1 : x → X, size_5_2 : + → Cross 등 6줄*

![실행 ②: data.json이 없을 때 data.json을 읽을 수 없습니다: [Errno 2] No such file or directory: 'data.json', Traceback 없이 끝남](images/70-run-no-file.png)

*실행 ②: data.json이 없을 때 data.json을 읽을 수 없습니다: [Errno 2] No such file or directory: 'data.json', Traceback 없이 끝남*

## 커밋, push, PR, 정리

![git checkout main, git pull로 dbe0a9c..48b7ec8 Fast-forward main.py 45 insertions 1 deletion, git branch -d feature/json-load (was 0270996), git fetch --prune으로 - [deleted] origin/feature/json-load, git --no-pager log --oneline --graph -6으로 48b7ec8 Merge pull request #6 등이 pager 없이 한 번에 출력](images/70-merge-log.png)

*git checkout main, git pull로 dbe0a9c..48b7ec8 Fast-forward main.py 45 insertions 1 deletion, git branch -d feature/json-load (was 0270996), git fetch --prune으로 - [deleted] origin/feature/json-load, git --no-pager log --oneline --graph -6으로 48b7ec8 Merge pull request #6 등이 pager 없이 한 번에 출력*
