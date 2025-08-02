import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def get_article_ids_from_hidden_links(page_number=1):
    url = f"https://www.daai.tv/news/history?p={page_number}"
    print(f"🌐 正在抓取第 {page_number} 頁：{url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    hidden_div = soup.select_one('div[style="display:none"]')
    if not hidden_div:
        print("⚠️ 沒找到隱藏連結區塊")
        return []

    article_ids = []
    for a in hidden_div.find_all("a", href=True):
        match = re.search(r"/news/history/(\d{6})", a["href"])
        if match:
            article_ids.append(match.group(1))

    print(f"✅ 共抓到 {len(article_ids)} 則新聞 ID")
    return article_ids


def extract_news_from_article(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if not meta_tag or not meta_tag.get("content"):
        print(f"⚠️ 找不到 meta description：{article_url}")
        return None

    raw_text = meta_tag["content"]
    sections = re.split(r"\n?●", raw_text)
    sections = [s.strip() for s in sections if s.strip()]

    column_texts = []
    label = None
    for section in sections:
        match = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日\s+(.+?)\n", section)
        if match:
            year, month, day, title = match.groups()
            label = f"{int(month)}月{int(day)}號"
            full_title = f"●{year}年 {title}"
            content = section[match.end():].strip()
            content = re.sub(r"\s+", " ", content)
            combined = f"{full_title}\n{content}"
            column_texts.append(combined)
    if not column_texts:
        return None
    return label, column_texts


def run_scraper(page_number=1):
    article_ids = get_article_ids_from_hidden_links(page_number)

    all_rows = []
    for article_id in article_ids:
        url = f"https://www.daai.tv/news/history/{article_id}"
        print(f"📰 擷取文章：{url}")
        result = extract_news_from_article(url)
        if result:
            label, column_texts = result
            row = [label] + column_texts
            all_rows.append(row)

    if all_rows:
        max_len = max(len(r) for r in all_rows)
        for row in all_rows:
            while len(row) < max_len:
                row.append("")

        columns = ["日期"] + [f"新聞{i+1}" for i in range(max_len - 1)]
        df = pd.DataFrame(all_rows, columns=columns)

        output_path = f"大愛新聞_第{page_number}頁24則新聞.xlsx"
        df.to_excel(output_path, index=False)
        print(f"✅ 匯出完成：{output_path}")
    else:
        print("❌ 沒有成功擷取任何資料")


# === 抓多頁 ===
for page_number in range(5, 7):  
    print(f"\n📄 正在處理第 {page_number} 頁")
    run_scraper(page_number)
