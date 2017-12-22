# README.md
1. How to install needed library

```
pip install PyQt5
pip install PyQt5-tools
pip install pyinstaller
pip install pandas
```

2. How to convert pyqt designer .ui file to .py file.
```
pyuic5 selector.ui -o selectorUI.py
```

3. How to make exe file.
```
pyinstaller -F ImageTypeSelector.spec
```

# ImageTypeSelector.exe 사용법 v0.2.1 (per_patient)

1. ImageTypeSelector.exe를 더블클릭해 실행합니다.

2. 영상에 나타난 궤양의 종류를 마우스 클릭 또는 키보드 단축키(benign: b, cancer: c)를 통해 선택합니다.\
   만약 선택한 영상의 분류가 모호하다고 생각될 경우 Ambiguous 체크박스를 클릭 또는 키보드 단축키(a)를 통해 체크합니다.

3. 'Next Image' 버튼을 클릭하거나 키보드의 ↑ 방향키를 이용하여 다음 영상으로 넘어갈 수 있습니다.\
   'Prev Image' 버튼을 클릭하거나 키보드의 ↓ 방향키를 이용하여 이전 영상으로 돌아갈 수 있습니다.\
   마지막 영상에서 'Next Image' 버튼을 누르는 경우 첫번째 영상으로, 첫번째 영상에서 'Prev Image' 버튼을 누르는 경우 마지막 영상으로 이동합니다.

4. 'Next Patient' 버튼을 클릭하거나 키보드의 → 방향키를 이용해 다음 환자로 넘어갈 수 있습니다.\
   'Prev Patient' 버튼을 클릭하거나 키보드의 ← 방향키를 이용하여 이전 환자로 돌아갈 수 있습니다.

5. 현재 데이터셋의 환자들을 모두 분류하면 결과를 저장하고 다음 데이터셋으로 전환할지 묻는 창이 나타납니다.\
   'Yes'를 선택하면 결과가 저장되고 다음 데이터셋으로 전환됩니다. 전환 이후에는 이전 데이터셋을 더이상 수정할 수 없습니다. \
   수정이 필요하다고 생각될 경우 'No'를 클릭해주십시오.\
   데이터셋은 0~12번까지 총 13개가 있으며 각각의 데이터셋은 0~11: 30명, 12: 7명의 환자들의 영상을 포함하고 있습니다. \
   지금까지 작업한 환자의 수가 우측 상단에 표시됩니다.

6. 프로그램이 종료될 때 자동으로 현재까지의 작업이 저장되고, 프로그램이 다시 켜질 때 복구하여 이어서 작업할 수 있습니다.\
   현재까지의 작업내용은 backup.imagetypeselector에 저장됩니다. 이 파일이 사라지거나 변경될 경우 이어서 작업할 수 없으니 주의하십시오. 

7. 결과는 'results'라는 폴더 아래에 'result_(데이터셋 번호).csv'라는 파일에 저장됩니다. 이 파일들과 경로는 자동으로 생성됩니다.\
   작업을 완료하고 이 파일을 보내주시면 됩니다.

8. 프로그램을 초기화하고 싶은 경우,
    1) results 폴더를 삭제하고,
    2) backup.imagetypeselector라는 파일을 삭제한 다음 프로그램을 실행하면 됩니다.
