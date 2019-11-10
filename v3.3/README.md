# GWGHA-SUMO

主要介紹資料夾結構以及命名，若程式有問題，再詢問我。

* 作者以及連絡方式
    106 鄧子奇 james992927108@gmail.com
* 系統環境
    ubuntu 16.04、python 2.7
* 安裝方式
    參閱資料夾下"SUMO安裝方式.pdf"

* 資料夾結構
    1. algo中包含碩論中使用的演算法，目前有goa、spso2011、pso_TL、gwo、gwo_m、gwgha、gwogoaha。

        說明:
        1. gwgha 是碩士論文中提出的方法。
        2. gwogoaha 是原版gwo與原版goa相結合，與gwgha比較使用。
    2. input包含要啟動模擬的檔案， 我分為三個資料夾。
        * map 輸入的地圖
        * road 輸入的路線
        * addfile
            1. 演算法將solutiuon 寫入這份檔案中，啟動模擬器時，會複寫在map中的紅路燈資訊。
            2. 另外演算法都是群體類型，每次都有多個position，因此以multiprocess的方式啟動多個模擬器進行加速。

        註: 也是能改成一個一個soltion進行模擬，需要修改程式，就先不解釋。
    3. 當開始執行模擬，會產生兩個資料夾。
        * output 每個模擬結束會產生tripinfo
        * result 產生透過演算法優化後的結果
            * 資歷夾名稱 演算法-地圖簡稱-路線-roundtime-iteration-population-time
        * 在 run.py 的 def map_name_vs() 中設定。

        註: 地圖簡稱，程式中已預設好

        | city name | abb |
        |-----------|-----|
        | alameda   | a   |
        | rivadavia | r   |
        | kaohsiung | k   |
        | taichung  | tc  |
        | taipei    | tp  |
        * 資料夾下有 10 輸出檔案，有
        1. best_poition.txt: 在測試輸出最佳round的position.舉例，假設只測試2個round，第一個round最佳fitness為5，第二個round為4，此檔案記入第二個round的position。
        2. complete_veh_duration_time: 紀錄每一個evalution下，加總所有完成車輛的旅行時間
        3. complete_veh_num.txt: 每一個evaluation完成的車輛數量。
        4. convergence.txt: 平均fitness的收斂數值。假設有30個round，第一個數值是根據每一個round的第一個值加總後並除以30所得。
        5. incomplete_veh_duration_time.txt: 未完成車輛數量。
            **需要注意** 程式中預設總車輛數量為 500，若要測試更多的車輛，需手動修改，因為未完成數量是直接由500減去完成的車輛。
        6. Round_evaluation.txt: 大部分實驗檔案名稱為 Round，紀錄每一round中fitness收斂。
        7. Round_position: 每完成一個round之後會輸出最佳解的position。
        8. SimulateResult_List.txt: 目前沒有用到，記錄每一個evalution會使用到的數值，每一個round資料結構維2維陣列，因此有多個2維陣列，根據round得大小而定，在每一個二維陣列中，每一列分別有以下屬性:
            * fitness
            * 完成車輛數量
            * 完成車輛總旅程時間
            * 未完成車輛旅程時間
            * 總車輛旅程時間
            * 等待時間
        9. summary.txt: 最常使用到，會輸出所有round中
            * 最差
            * 平均
            * 最好
            * 標準差
            * 程式執行時間
        10. total_veh_duration_time.txt: 總車輛旅程時間
        11. waiting_time.txt: 所有車輛的等待時間
