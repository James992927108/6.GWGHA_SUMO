# 如何取得測試資料

1. osm檔案從openstreetmap中擷取
<https://www.openstreetmap.org/>
2. 將 osm 檔案轉換成SUMO支援的 net.xml 檔案(地理資訊檔案)

    * python netconvert.py 輸入檔案 輸出檔案(輸出檔案名稱可以自定義)。

    例如 :
    python netconvert.py "map.osm.xml" "map.net.xml"
3. 產生路線檔案 rou.xml

    * python randomTrips.py -n 輸入檔案 -r 輸出檔案 -b 開始時間 -e 結束時間 -p 抵達率

    例如 :
    python randomTrips.py  -n kaohsiung.net.xml -r map.rou.xml -e 500 -p 0.2 --trip-attributes="departLane=\"best\" type=\"passenger\"" --additional-file type.add.xml

4. 檢查是否產生自定義書輛的車。

    * python check_car_num.py 數量

    例如:
    python check_car_num.py 500
5. 測試執行
    * python rum_sumo.py (0/1)
        * 0 表示以Terminal啟動
        * 1 表示以GUI啟動
