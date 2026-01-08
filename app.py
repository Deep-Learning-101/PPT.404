import gradio as gr
import os
import tempfile
import zipfile
import shutil
import base64
from pdf2image import convert_from_path
from PIL import Image
from dotenv import load_dotenv

# 使用 Google 新版 SDK
from google import genai
from google.genai import types

load_dotenv()

class NotebookLMTool:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def set_key(self, user_key):
        if user_key and user_key.strip():
            self.api_key = user_key.strip()
            self.client = genai.Client(api_key=self.api_key)
            return "✅ API Key 已更新！"
        return "⚠️ Key 無效"

    def process_pdf(self, pdf_file, progress=gr.Progress()):
        if not self.client:
            raise ValueError("請先輸入 Google API Key！")
        
        if pdf_file is None:
            return None, None, None

        # 1. 準備暫存目錄
        temp_dir = tempfile.mkdtemp()
        img_output_dir = os.path.join(temp_dir, "cleaned_images")
        os.makedirs(img_output_dir, exist_ok=True)
        
        # 2. PDF 轉圖片
        progress(0.1, desc="正在將 PDF 轉為圖片...")
        try:
            images = convert_from_path(pdf_file)
        except Exception as e:
            raise ValueError(f"PDF 轉換失敗 (請確認 packages.txt 有加入 poppler-utils): {str(e)}")

        full_text = ""
        cleaned_images_paths = []
        gallery_preview = []

        # 3. 逐頁處理
        for i, img in enumerate(images):
            progress(0.1 + (0.8 * (i / len(images))), desc=f"AI 正在處理第 {i+1}/{len(images)} 頁...")
            
            # --- 步驟 A: 提取文字 (OCR) ---
            # 使用標準 Flash 模型處理文字，速度最快
            try:
                resp_text = self.client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=["Extract all text content from this slide strictly.", img]
                )
                page_content = resp_text.text if resp_text.text else "[No Text Found]"
            except Exception as e:
                page_content = f"[OCR Error: {e}]"
            
            full_text += f"=== Page {i+1} ===\n{page_content}\n\n"

            # --- 步驟 B: 圖片去字 (Image Generation) ---
            # 關鍵修改：必須使用 'gemini-2.0-flash-exp' 且該模型目前才支援 IMAGE 輸出
            save_name = f"slide_{i+1:02d}.png"
            final_path = os.path.join(img_output_dir, save_name)
            
            try:
                resp_img = self.client.models.generate_content(
                    model="gemini-2.5-flash-image",  # ✅ 修正：使用支援圖片輸出的實驗模型
                    contents=[
                        "Remove all text from this image. Fill the gaps using the surrounding background texture to make it look clean and natural. Output ONLY the image.", 
                        img
                    ],
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"] # ✅ 修正：明確告知需要圖片模態
                    )
                )
                
                # 處理圖片回傳 (解析 SDK 回應)
                image_data = None
                
                # 檢查 inline_data (Base64)
                if hasattr(resp_img, 'parts') and resp_img.parts:
                    for part in resp_img.parts:
                        if part.inline_data:
                            image_data = part.inline_data.data
                            break
                
                # 部分 SDK 版本可能直接放在 bytes
                if image_data is None and hasattr(resp_img, 'bytes') and resp_img.bytes:
                    image_data = resp_img.bytes

                if image_data:
                    # 如果是 Base64 字串，需要解碼
                    if isinstance(image_data, str): 
                        image_data = base64.b64decode(image_data)
                    
                    with open(final_path, "wb") as f:
                        f.write(image_data)
                    
                    cleaned_images_paths.append(final_path)
                    gallery_preview.append((final_path, f"Page {i+1} (Cleaned)"))
                    print(f"Page {i+1}: Image generated successfully.")
                else:
                    # 失敗回退：保留原圖並標記
                    print(f"Page {i+1} Failed: No image data. Text: {resp_img.text if hasattr(resp_img, 'text') else 'Unknown'}")
                    img.save(final_path)
                    gallery_preview.append((final_path, f"Page {i+1} (Original - Gen Failed)"))

            except Exception as e:
                print(f"Page {i+1} Error: {str(e)}")
                img.save(final_path)
                gallery_preview.append((final_path, f"Page {i+1} (Original - Error)"))
        
        # 4. 打包結果
        progress(0.9, desc="正在打包 ZIP...")
        
        txt_path = os.path.join(temp_dir, "extracted_text.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        zip_path = os.path.join(temp_dir, "notebooklm_pack.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(txt_path, "content.txt")
            for img_path in cleaned_images_paths:
                zf.write(img_path, os.path.join("cleaned_slides", os.path.basename(img_path)))

        return zip_path, full_text, gallery_preview

# Init
tool = NotebookLMTool()

# --- Gradio UI ---
with gr.Blocks(title="NotebookLM Slide Decomposer", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛠️ NotebookLM 投影片 PDF 拆解神器")
    gr.Markdown("""
    <div align="center">
    
    # 🛠️ 上傳 NotebookLM 投影片 PDF，AI 自動幫你：**1. 抓出所有文字** | **2. 重繪乾淨背景圖**  
    👉 歡迎 Star [GitHub](https://github.com/Deep-Learning-101/) ⭐ 覺得不錯 👈  
    <h3>🧠 補腦專區：<a href="https://deep-learning-101.github.io/" target="_blank">Deep Learning 101</a></h3>  
    
    | 🔥 技術傳送門 (Tech Stack) | 📚 必讀心法 (Must Read) |
    | :--- | :--- |
    | 🤖 [**大語言模型 (LLM)**](https://deep-learning-101.github.io/Large-Language-Model) | 🏹 [**策略篇：企業入門策略**](https://deep-learning-101.github.io/Blog/AIBeginner) |
    | 📝 [**自然語言處理 (NLP)**](https://deep-learning-101.github.io/Natural-Language-Processing) | 📊 [**評測篇：臺灣 LLM 分析**](https://deep-learning-101.github.io/Blog/TW-LLM-Benchmark) |
    | 👁️ [**電腦視覺 (CV)**](https://deep-learning-101.github.io//Computer-Vision) | 🛠️ [**實戰篇：打造高精準 RAG**](https://deep-learning-101.github.io/RAG) |
    | 🎤 [**語音處理 (Speech)**](https://deep-learning-101.github.io/Speech-Processing) | 🕳️ [**避坑篇：AI Agent 開發陷阱**](https://deep-learning-101.github.io/agent) |
    </div>
    """)
    
    with gr.Row():
        with gr.Column():
            api_input = gr.Textbox(label="Google API Key", type="password", placeholder="貼上你的 Gemini API Key")
            btn_set_key = gr.Button("設定 Key")
            status_msg = gr.Markdown("")
            
            gr.Markdown("---")
            pdf_input = gr.File(label="上傳 PDF")
            btn_process = gr.Button("🚀 開始拆解", variant="primary")
        
        with gr.Column():
            out_zip = gr.File(label="📦 下載懶人包 (ZIP)")
            out_text = gr.Textbox(label="📝 文字內容預覽", lines=8)
    
    gr.Markdown("### 🖼️ 處理結果預覽")
    out_gallery = gr.Gallery(columns=4)

    btn_set_key.click(tool.set_key, inputs=api_input, outputs=status_msg)
    
    btn_process.click(
        tool.process_pdf,
        inputs=[pdf_input],
        outputs=[out_zip, out_text, out_gallery]
    )

if __name__ == "__main__":
    demo.launch()
