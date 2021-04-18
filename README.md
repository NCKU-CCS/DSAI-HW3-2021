# DSAI-HW3-2021

### Source

  - [Slide](https://docs.google.com/presentation/d/1JW27_5HXYZhqWmgvDhtXBaFTOfksO_dS/edit#slide=id.p1)
  - [Dashboard](https://docs.google.com/spreadsheets/d/1cjhQewnXT2IbmYkGXRYNC5PlGRafcbVprCjgSFyDAaU/edit?pli=1#gid=0)

### Framework

![Framework](https://imgur.com/x1UlliA.jpg)

### Rules

- 上傳

1. 壓縮檔案為 `zip` 檔
3. 檔名：{學號}-{版本號}.zip，例：`E11111111-v1.zip`
4. 兩人一組時，請以 student1 的學號上傳
5. 傳新檔案時請往上加版本號，程式會自動讀取最大版本
6. 請遵守上傳架構，進入點為 `main.py` ，隨意更改會讀不到您的程式
7. 請注意輸入的 `bidresult` 資料初始值為空
8. 請使用 `python 3.8` 版本
9. 程式每次執行只有 `120 秒`，請控制好您的檔案
10. 每天的交易量限制 `100 筆`，只要有超出會全部交易失敗，請控制輸出數量

- 下載

1. `information/` ：每次媒合會公佈交易資料可自行參考
    - 檔名：`info-{match_id}.csv`
2. `student/`：每位學生投標及帳單資料，只有成功上傳的才會在這裡輸出
    - 投標資料：`bidresult-{match_id}.csv`
    - 帳單資料：以日為單位，`bill-{match_id}.csv`
3. `training_data/`：2018-01-01 ~ 2018-08-31 用電及產電資料
