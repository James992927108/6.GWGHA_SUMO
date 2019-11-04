# 檔案結構說明

* 首先，資料夾的順序是對應碩論章節

|                               | 章節  |
|-------------------------------|-------|
| 1.gwgha_exchange-parameter    | 4.4.1 |
| 2.gwgha_025-population        | 4.4.3 |
| 3.gwo-gwo_m                   | 4.5.1 |
| 4.gwogoaha_exchange-parameter | 4.5.2 |
| 5.single                      | 無    |
| 6.all                         | 4.6.1 |
| 7.time                        | 無    |
| 8.gwgha-auto-test             | 4.4.2 |

* 實驗資料夾命名規則

    第一個數字代表測試幾個 round

    第二個數字代表測試幾個 iteration

    第三個數字代表測試幾個 population

例如 :

資料夾 30-750-40 代表底下實驗結果皆為經過 30 round、750 iteration和演算法群體個數設定為 40 pupulation。

* 說明資料夾內容:

1. 資料夾 1.gwgha_exchange-parameter: 使用不同固定交換參數測試結果。在不同實驗資料夾下有在透過不同的資料夾區分參數結果。
2. 資料夾 2.gwgha_025-population: 每個實驗都是 30000 evaluations。
3. 資料夾 3.gwo-gwo_m: 比較原版灰狼與改本灰狼的差別，在碩論所提出的方法(GWGHA)使用改版灰狼。
4. 資料夾 4.gwogoaha_exchange-parameter: 測試原版GWO與GOA結合後交換參數的作用。
5. 資料夾 5.single: 測試單執行序與多執行序效能的差異。
6. 資料夾下 6.all:包含與其他演算法測試結果。
在每個實驗資料夾，先以測試地圖區分，在以不同路線區分。
    * 若有新的測試資料，可以直接放進相對應的資料夾下，直接執行在 6.all 下面的 script.sh 檔案，即可產生比較的收斂圖。
7. 目前沒有使用。
8. 新增加自動改變交換參數的實驗。

備註:

1. 資料夾 7.time 時間不準確，實驗結果**未**放進碩論，只用來預測大約會花多久時間。所記錄的時間數值為測試跑1個round的時間並乘上**30**倍。
2. 資料夾 5.single 時間是準確的，但結果僅在口試中使用。
3. GWOGOAHA 與 GWGHA 不同。

    * 原版 GWO x GOA -> GWOGOAHA
    * 改版 GWO x GOA -> GWGHA
