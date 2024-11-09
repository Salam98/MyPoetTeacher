import requests
from bs4 import BeautifulSoup
import time

# استخراج النص من صفحة معينة
def extract_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print(response.status_code)
        # استخراج النص من الفقرات <p>
        paragraphs = soup.find_all('p')
        text = ""
        for p in paragraphs:
            text += p.get_text(separator=" ") + "\n"
        return text.strip()
    else:
        print(response.status_code)
        return None

# توليد الرابط التالي بناءً على الرابط الحالي
def generate_next_url(current_url):
    # تقسيم الرابط للحصول على الجزء الأخير
    parts = current_url.rsplit('/', 1)
    if len(parts) > 1:
        base_url = parts[0]
        last_part = parts[1]

        # إذا كان آخر جزء يحتوي على رقم
        if last_part.isdigit():
            next_part = str(int(last_part) + 1)
            return f"{base_url}/{next_part}"
        elif "#" in last_part:
            page_number = last_part.split('#')[0]
            next_part = str(int(page_number) + 1)
            return f"{base_url}/{next_part}"
    return None

# استخراج النص من الكتاب كاملاً من الروابط المتتابعة
def extract_text_from_book(start_url, max_pages=796, delay=2):
    current_url = start_url
    all_text = ""
    page_count = 0

    while current_url and page_count < max_pages:
        print(f"استخراج النص من: {current_url}")
        page_text = extract_text_from_url(current_url)

        if page_text:
            all_text += page_text + "\n\n"
        else:
            print(f"فشل استخراج النص من {current_url}")
            break

        # توليد الرابط التالي
        current_url = generate_next_url(current_url)
        page_count += 1

        # تأخير قبل الانتقال إلى الصفحة التالية
        time.sleep(delay)

    return all_text

# بداية استخراج النص
start_url = "https://shamela.ws/book/10018/15"

book_text = extract_text_from_book(start_url, max_pages=796)

# حفظ النص في ملف
with open("book_text.txt", "w", encoding="utf-8") as file:
    file.write(book_text)

print("استخراج النص انتهى وتم حفظه في ملف book_text.txt")
