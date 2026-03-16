# 🛠️ NotebookLM 投影片 PDF 拆解神器
_Powered by Google gemini-2.5-flash & gemini-2.5-flash-image_

<div align="center">

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/DeepLearning101/PPT.404)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by](https://img.shields.io/badge/Powered%20by-Gemini%202.0%20Flash-4285F4?logo=google)](https://deepmind.google/technologies/gemini/)

👉 歡迎 Star [![GitHub](https://img.shields.io/badge/GitHub-Repo-black)](https://github.com/Deep-Learning-101/) ⭐ 覺得不錯 👈

**專為 NotebookLM 生成的 PDF 講義設計的逆向工程工具** **一鍵上傳，自動分離「純文字內容」與「乾淨背景圖」，讓你的素材可以二次利用！** <h3>🧠 補腦專區：<a href="https://deep-learning-101.github.io/" target="_blank">Deep Learning 101</a></h3>

| 🔥 技術傳送門 (Tech Stack) | 📚 必讀心法 (Must Read) |
| :--- | :--- |
| 🤖 [**大語言模型 (LLM)**](https://deep-learning-101.github.io/Large-Language-Model) | 🏹 [**策略篇：企業入門策略**](https://deep-learning-101.github.io/Blog/AIBeginner) |
| 📝 [**自然語言處理 (NLP)**](https://deep-learning-101.github.io/Natural-Language-Processing) | 📊 [**評測篇：臺灣 LLM 分析**](https://deep-learning-101.github.io/Blog/TW-LLM-Benchmark) |
| 👁️ [**電腦視覺 (CV)**](https://deep-learning-101.github.io//Computer-Vision) | 🛠️ [**實戰篇：打造高精準 RAG**](https://deep-learning-101.github.io/RAG) |
| 🎤 [**語音處理 (Speech)**](https://deep-learning-101.github.io/Speech-Processing) | 🕳️ [**避坑篇：AI Agent 開發陷阱**](https://deep-learning-101.github.io/agent) |
    
</div>

---

## 🤔 為什麼你需要這個？

Google 的 NotebookLM 生成的 Audio Overview 講義與投影片非常精美，但往往我們拿到的是一份「死」的 PDF 檔。

* 📝 **想抓文字？** PDF 複製出來的格式常常跑掉，或者需要一頁一頁複製。
* 🖼️ **想用圖片？** 圖片上壓滿了文字，無法拿來當作自己的簡報背景。

**NotebookLM Slide Decomposer** 解決了這個痛點！利用 Google Gemini 最新的視覺模型，它能：

1.  **智慧 OCR (gemini-2.5-flash)**：精準抓取每一頁的文字內容，忽略排版干擾，直接給你純文字檔。
2.  **AI 圖片重繪 (gemini-2.5-flash-image)**：理解圖片背景結構，自動「移除文字」並「補全背景」，還原出乾淨的投影片底圖。
3.  **懶人包下載**：處理完畢後，直接打包成 ZIP，內含文字檔與所有乾淨圖片。

---

## 🚀 如何使用

### 線上直接使用 (Hugging Face Space)

1.  準備好你的 **Google Gemini API Key** ([點此申請](https://aistudio.google.com/app/apikey))。
2.  進入本 Space，在左上角輸入 API Key 並點擊「設定 Key」。
3.  上傳你的 PDF 檔案（建議頁數不要過多，以免等待太久）。
4.  點擊 **「🚀 開始拆解」**。
5.  等待處理完成，下載右側的 **ZIP 懶人包** 即可！

---

## 🛠️ 本地部署 (Local Development)

如果你想在自己的電腦上運行，請依照以下步驟：

### 1. 安裝系統依賴
本專案使用 `pdf2image`，需要安裝 `poppler`：
* **Mac**: `brew install poppler`
* **Linux**: `sudo apt-get install poppler-utils`
* **Windows**: 下載 Poppler binary 並加入 PATH 環境變數。

### 2. 下載專案與安裝套件
```bash
git clone [https://github.com/Deep-Learning-101/PPT-404.git](https://github.com/Deep-Learning-101/PPT-404.git)
cd PPT-404
pip install -r requirements.txt
