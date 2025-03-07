import asyncio
import aiohttp
import gradio as gr
import io
import os
import re
import nest_asyncio
from tavily import TavilyClient
from together import Together
from openai import OpenAI
from gradio.components import File
from io import BytesIO

nest_asyncio.apply()

# ===============================================
# Configuration Constants
# ===============================================
from dotenv import load_dotenv

load_dotenv()  # Load biến môi trường từ file .env

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("MY_OPENAI_API_KEY")

print(f"TOGETHER_API_KEY: {TOGETHER_API_KEY}") 
print(f"TAVILY_API: {TAVILY_API_KEY}") 
print(f"OPENAI_API_KEY: {OPENAI_API_KEY}") 

DEFAULT_MODEL_TOGETHER = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
FINAL_REPORT_MODEL_OPENAI = "o1-mini"  # Supports up to ~65k tokens for completion

# Lựa chọn chunk size & limit
MAX_LINKS_PER_ITERATION = 30
MAX_TOKENS_INPUT = 40000  # Tăng/giảm tùy ý, 40k an toàn
CHUNK_SIZE = 24000        # Mỗi chunk < 24k chars
SUMMARIZE_COMPLETION_TOKENS = 2000  # Summarize chunk
FINAL_COMPLETION_TOKENS = 64000     # <= 65536 limit

together_client = Together(api_key=TOGETHER_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# ==================================
# Asynchronous Helper Functions
# ==================================

async def call_together_ai_async(messages, model=DEFAULT_MODEL_TOGETHER):
    """Gọi Together AI để tạo search queries."""
    try:
        response = await asyncio.to_thread(
            together_client.chat.completions.create,
            messages=messages,
            model=model,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Together AI Error:", e)
        return None

async def call_openai_async(messages, max_comp_tokens, model=FINAL_REPORT_MODEL_OPENAI):
    """
    Gửi yêu cầu đến OpenAI, tùy max_comp_tokens <= 65536.
    """
    try:
        response = await asyncio.to_thread(
            openai_client.chat.completions.create,
            model=model,
            messages=messages,
            max_completion_tokens=max_comp_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ OpenAI Error:", e)
        return None

# =============== Chunk Summarization =============

async def chunk_text(text, chunk_size=CHUNK_SIZE):
    """
    Chia text thành nhiều chunk < chunk_size.
    """
    for i in range(0, len(text), chunk_size):
        yield text[i: i+chunk_size]

async def summarize_chunk(session, chunk_text):
    """
    Tóm tắt 1 chunk, dùng OpenAI với SUMMARIZE_COMPLETION_TOKENS.
    """
    prompt = (
        "You are an AI summarizer. Summarize the text below into a concise overview, "
        "preserving key details but significantly reducing length.\n\nText:\n"
    )
    messages = [
        {"role": "assistant", "content": "You are a summarizer tool."},
        {"role": "user", "content": prompt + chunk_text}
    ]
    summary = await call_openai_async(messages, max_comp_tokens=SUMMARIZE_COMPLETION_TOKENS)
    return summary if summary else ""

# =============== Generate Search Queries =============
async def generate_search_queries_async(session, user_query):
    """
    Dùng Together AI để tạo query (tối đa 4).
    """
    prompt = (
        "You are an expert research assistant. Given the user's query, generate up to four distinct, "
        "precise search queries that would help gather comprehensive information on the topic. "
        "Return only a Python list of strings, for example: ['query1', 'query2', 'query3']."
    )
    messages = [
        {"role": "system", "content": "You are a helpful and precise research assistant."},
        {"role": "user", "content": f"User Query: {user_query}\n\n{prompt}"}
    ]
    resp = await call_together_ai_async(messages)
    if not resp:
        print("⚠️ No response from Together AI, fallback queries.")
        return [
            f"{user_query} overview",
            f"{user_query} in-depth analysis",
            f"{user_query} use cases",
            f"{user_query} latest developments"
        ]
    # clean <think>...
    resp_clean = re.sub(r"<think>.*?</think>", "", resp, flags=re.DOTALL).strip()
    try:
        if resp_clean.startswith("[") and resp_clean.endswith("]"):
            sq = eval(resp_clean)
            if isinstance(sq, list) and all(isinstance(q, str) for q in sq):
                return sq
    except Exception as e:
        print("⚠️ Error parsing search queries:", e, "\nResponse:", resp_clean)

    # fallback
    return [
        f"{user_query} overview",
        f"{user_query} in-depth analysis",
        f"{user_query} use cases",
        f"{user_query} latest developments"
    ]

# =============== Perform Search ===============
async def perform_search_async(session, query):
    """Tavily search, lọc youtube & deepseek."""
    try:
        resp = await asyncio.to_thread(
            tavily_client.search,
            query=query,
            max_results=10,
            include_raw_content=True,
            search_depth="advanced"
        )
        if not resp:
            return []
        links = [x.get("url") for x in resp.get("results", []) if "url" in x]
        valid_links = [u for u in links if "youtube.com" not in u.lower() and "deepseek.com" not in u.lower()]
        return valid_links
    except Exception as e:
        print("❌ Error performing Tavily search:", e)
        return []

# =============== Extract Webpage Text ===============
async def extract_webpage_text_async(url):
    """
    Trích xuất nội dung từ một trang web bằng Tavily.
    In ra độ dài ban đầu (raw_length) trước khi cắt còn MAX_TOKENS_INPUT.
    """
    try:
        response = await asyncio.to_thread(
            tavily_client.extract,
            urls=[url],
            include_images=False
        )
        if "results" in response and response["results"]:
            raw_text = response["results"][0].get("raw_content", "")
            raw_length = len(raw_text)
            print(f"Raw length for {url}: {raw_length} chars (before cutting)")

            # Cắt còn MAX_TOKENS_INPUT để tránh vượt context
            trimmed_text = raw_text[:MAX_TOKENS_INPUT]
            print(f"Trimmed length for {url}: {len(trimmed_text)} chars (after cutting)\n")
            return trimmed_text
        else:
            print(f"⚠️ No extraction result for URL: {url}")
            return ""
    except Exception as e:
        print(f"❌ Error extracting webpage text with Tavily for {url}: {e}")
        return ""

async def process_link(session, link, user_query, search_query):
    """Lấy text 1 link."""
    print(f"🔍 Fetching and extracting content from: {link}")
    text = await extract_webpage_text_async(link)
    return text if text else None

# =============== Generate Final Report ===============
async def generate_final_report_async(session, user_query, all_contexts):
    """
    Tạo báo cáo cuối cùng, chunk Summaries => final.
    """
    if not all_contexts:
        return f"⚠️ Limited information found for: {user_query}."

    # Gộp all context
    combined = "\n".join(all_contexts)
    if len(combined) <= CHUNK_SIZE:
        # Gọi thẳng
        print("✅ Single chunk (no chunk summarization needed).")
        long_prompt = (
            "You are an AI research assistant. Based on the following contexts and the user query, "
            "create a thoroughly detailed, long-form report. Use headings, bullet points, examples, references, etc. "
            f"Output can be up to {FINAL_COMPLETION_TOKENS} tokens if needed."
        )
        messages = [
            {"role": "assistant", "content": "You are a specialized long-form report writer."},
            {"role": "user", "content": f"User Query: {user_query}\n\nContexts:\n{combined}\n\n{long_prompt}"}
        ]
        final_report = await call_openai_async(messages, max_comp_tokens=FINAL_COMPLETION_TOKENS)
        return final_report if final_report else "⚠️ No significant data."

    # ...nếu text > chunk size => chunk summarization
    print("⚠️ Context too large, using chunk summarization...")

    # Summaries
    summaries = []
    async for chunk in chunk_text(combined, CHUNK_SIZE):
        summary = await summarize_chunk(session, chunk)
        summaries.append(summary)

    # Gom summaries
    summaries_combined = "\n\n".join(summaries)
    print(f"✅ Summaries combined length = {len(summaries_combined)} chars")

    # Gọi final
    final_prompt = (
        "You are an AI research assistant. The text below are chunk summaries. "
        "Please combine them into a single cohesive, multi-sectional, long-form report. "
        f"You may produce up to {FINAL_COMPLETION_TOKENS} tokens. Include references, headings, examples, etc."
    )
    messages = [
        {"role": "assistant", "content": "You are a specialized long-form report writer with no explicit token limit."},
        {
            "role": "user",
            "content": f"User Query: {user_query}\n\nSummaries:\n{summaries_combined}\n\n{final_prompt}"
        }
    ]
    final_report = await call_openai_async(messages, max_comp_tokens=FINAL_COMPLETION_TOKENS)
    return final_report if final_report else "⚠️ No final data."

# =========================
# Main Asynchronous Routine
# =========================

async def gradio_interface(user_query, iteration_limit=1):
    """Hàm chạy async_main() và hiển thị kết quả trên giao diện Gradio."""
    aggregated_contexts = []
    all_search_queries = []
    iteration = 0

    async with aiohttp.ClientSession() as session:
        new_search_queries = await generate_search_queries_async(session, user_query)
        if not new_search_queries:
            return "❌ Không tạo được truy vấn tìm kiếm."

        all_search_queries.extend(new_search_queries)

        while iteration < iteration_limit:
            search_tasks = [perform_search_async(session, query) for query in new_search_queries]
            search_results = await asyncio.gather(*search_tasks)

            unique_links = {}
            for idx, links in enumerate(search_results):
                query = new_search_queries[idx]
                for link in links:
                    if link and link not in unique_links:
                        unique_links[link] = query

            if not unique_links:
                iteration += 1
                continue

            link_tasks = [process_link(session, link, user_query, unique_links[link]) for link in unique_links]
            link_results = await asyncio.gather(*link_tasks)

            iteration_contexts = [res for res in link_results if res]
            aggregated_contexts.extend(iteration_contexts)

            if not iteration_contexts:
                iteration += 1
                continue

            new_search_queries = await generate_search_queries_async(session, user_query)
            if not new_search_queries:
                break

            all_search_queries.extend(new_search_queries)
            iteration += 1

        if not aggregated_contexts:
            return "❌ Không có nội dung phù hợp."

        final_report = await generate_final_report_async(session, user_query, aggregated_contexts)
        return final_report

def run_gradio(user_query, iteration_limit=1):
    """Hàm đồng bộ chạy async_main() để tích hợp vào Gradio."""
    return asyncio.run(gradio_interface(user_query, iteration_limit))

#=============================================================================
# Hàm tạo file Word
#=============================================================================

import pypandoc  # type: ignore
from io import BytesIO

def create_word_file(content, filename='report.docx'):
    file_stream = BytesIO()
    output = pypandoc.convert_text(content, 'docx', format='md', outputfile=filename)
    with open(filename, "rb") as f:
        file_stream.write(f.read())
    file_stream.seek(0)
    return file_stream, filename

#============================================================================
# Hàm tạo PDF
#============================================================================

from io import BytesIO
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from reportlab.lib.units import inch # type: ignore
from reportlab.pdfbase.pdfmetrics import stringWidth # type: ignore

def create_pdf_file(content, filename='report.pdf'):
    try:
        # Tạo một file PDF trong bộ nhớ
        file_stream = BytesIO()
        pdf = canvas.Canvas(file_stream, pagesize=letter)

        # Đặt font và kích thước
        font_name = "Times-Roman"
        font_size = 12
        pdf.setFont(font_name, font_size)

        # Giới hạn chiều rộng trang (trừ lề)
        page_width, page_height = letter
        margin = 30  # Lề trái & phải
        max_width = page_width - 2 * margin  # Chiều rộng khả dụng
        y_position = page_height - 50  # Vị trí bắt đầu

        # Xử lý xuống dòng tự động
        def split_text(text, max_width, font_name, font_size):
            words = text.split()
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + " " + word if current_line else word
                if stringWidth(test_line, font_name, font_size) <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

            return lines

        # Xử lý từng dòng văn bản
        text_lines = []
        for line in content.split("\n"):
            text_lines.extend(split_text(line, max_width, font_name, font_size))

        # Vẽ từng dòng lên trang PDF
        line_spacing = 14  # Khoảng cách dòng
        for line in text_lines:
            if y_position < 50:  # Nếu hết trang -> tạo trang mới
                pdf.showPage()
                pdf.setFont(font_name, font_size)
                y_position = page_height - 50

            pdf.drawString(margin, y_position, line)
            y_position -= line_spacing

        # Kết thúc trang và lưu file PDF
        pdf.showPage()
        pdf.save()

        # Đưa con trỏ về đầu file stream
        file_stream.seek(0)

        return file_stream, filename
    except Exception as e:
        print(f"Lỗi khi tạo file PDF: {str(e)}")
        raise e



# import pdfkit  # type: ignore
# from io import BytesIO

# def create_pdf_file(content, filename='report.pdf'):
#     options = {
#         'encoding': "UTF-8",
#         'quiet': ''
#     }
#     file_stream = BytesIO()
#     pdfkit.from_string(content, file_stream, options=options)
#     file_stream.seek(0)
#     return file_stream, filename

# ==============================================================================
# Giao diện Gradio
# ==============================================================================

# Hàm tải file
def download_report(content, file_type):
    """Tạo file tùy theo loại (Word hoặc PDF) và trả về để tải xuống."""
    if file_type == "doc":
        return create_word_file(content)
    elif file_type == "pdf":
        return create_pdf_file(content)
    else:
        raise ValueError("Loại file không hợp lệ. Chọn 'doc' hoặc 'pdf'.")

def run_gradio(user_query, iteration_limit=1):
    """Hàm đồng bộ chạy async_main() để tích hợp vào Gradio."""
    final_report = asyncio.run(gradio_interface(user_query, iteration_limit))
    return final_report

def main():
    """Hàm chính để khởi chạy giao diện Gradio."""
    with gr.Blocks() as demo:
        gr.Markdown("# 🔍 Open Deep Researcher - AI Research Assistant")

        with gr.Row():
            user_input = gr.Textbox(label="Nhập chủ đề nghiên cứu", placeholder="Nhập câu hỏi của bạn...")
            iter_input = gr.Number(label="Số vòng lặp tối đa", value=5)

        output_text = gr.Textbox(label="Kết quả nghiên cứu", lines=10)

        submit_btn = gr.Button("🔎 Bắt đầu tìm kiếm")
        submit_btn.click(run_gradio, inputs=[user_input, iter_input], outputs=output_text)

        with gr.Row():
            download_doc_btn = gr.Button("📥 Tải về file Word")
            download_pdf_btn = gr.Button("📥 Tải về file PDF")

        # Kết nối nút tải xuống với hàm xử lý
        download_doc_btn.click(
            fn=download_report,
            inputs=[output_text, gr.State("doc")],  # Truyền nội dung và loại file
            outputs=gr.File(label="Tải về file Word"),  # Đầu ra là file để tải xuống
        )
        download_pdf_btn.click(
            fn=download_report,
            inputs=[output_text, gr.State("pdf")],  # Truyền nội dung và loại file
            outputs=gr.File(label="Tải về file PDF"),  # Đầu ra là file để tải xuống
        )

    demo.queue() # Bật Queue để xử lý nhiều yêu cầu đồng thời
    demo.launch(share=True)

if __name__ == "__main__":
    main()