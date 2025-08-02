# 大愛電視新聞爬蟲（DaAi News Scraper）

這是一個用來擷取大愛電視歷史新聞網站"歷史上的今天"的 Python 專案，能夠自動爬取每一頁新聞的內容，整理成 Excel 檔案，並依照日期進行彙整。

## 功能特色

- 可以自行設定要擷取的頁數
- 擷取每頁共 24 則新聞的完整文字段落
- 自動擷取 meta description 作為新聞內文
- 將新聞依照日期與內容整理成橫向展開格式
- 最終可輸出為 `.xlsx` 格式的 Excel 文件

## 使用套件

- `requests`
- `beautifulsoup4`
- `pandas`
- `openpyxl`
- `re`（Python 內建）

## 安裝與執行

   1. 建議使用虛擬環境：

        python -m venv .venv

        啟用虛擬環境：

        Windows：

        .venv\Scripts\activate
        
        macOS / Linux：

        source .venv/bin/activate

   2. 安裝依賴套件 
        
        pip install -r requirements.txt

   3. 執行爬蟲主程式
        python main.py

## 備註

本專案僅用於資料分析與個人學習用途，請勿用於商業重發或侵犯網站權益。