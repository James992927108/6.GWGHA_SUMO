# 資料夾內容即為測試資料

1. 總共有 5 張測試地圖
    1. alameda
    2. rivadavia
    3. kaohiung
    4. taichung
    5. taipei
2. 可以自行選擇是否呈現 GUI 畫面。

## 如何執行

執行script.sh即可

指令如下:
    python 程式.py 是否開gui 地圖 路線 原始或優化後交通號誌燈檔案
    python run_sumo.py (gui/no_gui) (alameda/rivadavia/kaohiung/taichung/taipei) 500 (original/optimize)

註:

1. 不同路線代表不同的測試資料，同一個測試可以有不同的測試路線。
2. optimize 檔案目前是用 GWGHA_075 的結果，可以自行替換。
