import os
import glob
import json
import urllib.request

API_KEY = os.environ.get("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def collect_code():
    code_content = ""
    for file_path in glob.glob("*.c"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            code_content += f"\n--- File: {file_path} ---\n{f.read()}\n"
    return code_content

def grade_with_ai(code):
    system_prompt = (
        "Bạn là trợ giảng lập trình C kinh nghiệm. Hãy chấm điểm bài làm của sinh viên theo thang điểm 10.\n"
        "Yêu cầu:\n"
        "- Đánh giá tư duy thuật toán, cấu trúc rẽ nhánh / vòng lặp / tính toán.\n"
        "- BỎ QUA các lỗi format hiển thị nhỏ (như thừa thiếu dấu cách, câu lệnh printf khác mẫu đôi chút, buffer stdin).\n"
        "- Trừ điểm nếu sai logic tính toán hoặc lỗi cú pháp khiến chương trình không chạy đúng.\n"
        "- Xuất kết quả nhận xét rõ ràng: Điểm số (/10), Điểm cộng, Điểm trừ và Lời khuyên tối ưu code.\n"
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{system_prompt}\n\nMã nguồn sinh viên:\n{code}"}]
        }]
    }

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Không thể chấm bài bằng AI do lỗi kết nối: {str(e)}"

if __name__ == "__main__":
    code = collect_code()
    if not code.strip():
        print("Không tìm thấy file mã nguồn C.")
    else:
        feedback = grade_with_ai(code)
        with open("ai_feedback.md", "w", encoding="utf-8") as f:
            f.write(feedback)
        print("Đã hoàn thành chấm điểm AI.")
