# services/receipt_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

# 設定路徑
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # 回到專案根目錄
FONT_PATH = os.path.join(BASE_DIR, "web", "static", "fonts", "kaiu.ttf")
OUTPUT_DIR = os.path.join("web", "static", "receipts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 註冊標楷體
pdfmetrics.registerFont(TTFont("Kaiu", FONT_PATH))

def generate_receipt(record) -> str:
    filename = f"{record.student.series_id}.pdf"
    path = os.path.join(OUTPUT_DIR, filename)
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    def draw_one_copy(offset_y):
        left = 15 * mm
        top = height - offset_y
        table_width = width - 30 * mm
        row_height = 7.5 * mm

        c.setFont("Kaiu", 9)

        # 標題
        c.setFont("Kaiu", 12)
        c.drawCentredString(width / 2, top, "國立華僑高級中等學校114學年度第1學期學雜費及代辦費收據")
        c.setFont("Kaiu", 9)

        # 學號、班級、序號、時間
        top_info_y = top - 14
        c.drawString(left, top_info_y, f"序號：{record.student.series_id}")
        c.drawString(left + 120, top_info_y, f"班級：{record.student.class_id or ''}")
        c.drawString(left + 220, top_info_y, f"學號：{record.student.student_id or ''}")
        c.drawString(left + 340, top_info_y, f"日期：{datetime.now().strftime('%Y/%m/%d %H:%M')}")

        # 表格資料
        items = [
            ["學費", "家長會費", "新生健檢費"],
            ["雜費", "學生團體保險費", "書籍費"],
            ["實習實驗費", "班級冷氣維護費", "模擬考費"],
            ["電腦及網路通訊使用費", "僑生健康保險費", "跑班冷氣費"],
            ["平時課輔費", "僑生保險費", ""],
            ["住宿費", "宿舍冷氣維護費", ""],
            ["班級費", "伙食費", ""]
        ]
        amount_dict = record.payment.items
        totals = [0, 0, 0]
        table_top = top - 30

        for i, row_items in enumerate(items):
            y = table_top - i * row_height
            for col in range(3):
                x = left + col * table_width / 3
                c.rect(x, y - row_height, table_width / 3, row_height, stroke=1, fill=0)
                c.drawString(x + 4, y - row_height + 3, row_items[col])
                amt = amount_dict.get(row_items[col], 0)
                if amt:
                    c.drawRightString(x + table_width / 3 - 4, y - row_height + 3, f"{amt:,.0f}")
                    totals[col] += amt

        # ✅ 合計列改為「只顯示總額」＋「收據編號」
        y = table_top - len(items) * row_height
        total_sum = sum(totals)
        for col in range(3):
            x = left + col * table_width / 3
            c.rect(x, y - row_height, table_width / 3, row_height, stroke=1, fill=0)

        # 左欄顯示總合計
        c.drawString(left + 4, y - row_height + 3, "合計：")
        c.drawRightString(left + table_width / 3 - 4, y - row_height + 3, f"{total_sum:,.0f}")

        # 右欄顯示收據編號
        c.drawRightString(left + table_width - 4, y - row_height + 3, f"收據編號：{record.student.series_id}")

        # 簽名欄
        c.drawString(left, y - row_height - 25, "經手人：")
        c.drawString(left + 90, y - row_height - 25, "主辦出納：鍾惠棻")
        c.drawString(left + 210, y - row_height - 25, "主辦會計：簡世洲")
        c.drawString(left + 330, y - row_height - 25, "校長：鄭文洋")

        # 分隔線
        c.setDash(3, 2)
        c.line(left, y - row_height - 35, width - left, y - row_height - 35)
        c.setDash()

    # 三聯印出
    draw_one_copy(30)
    draw_one_copy(310)
    draw_one_copy(590)

    c.save()
    print(f"[PDF] 收據儲存至：{path}")
    return path
