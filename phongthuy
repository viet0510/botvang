import telegram
import asyncio
from datetime import datetime, timedelta
import sxtwl
import matplotlib.pyplot as plt
import io

# --- ĐIỀN THÔNG TIN ---
TOKEN = '8667795071:AAEQ9CF6xhXIDsPUeVUvHZU-HOUDU6fpLv4'
CHAT_ID = '1176585769'

NGU_HANH = {
    'Giáp': 'Mộc', 'Ất': 'Mộc', 'Bính': 'Hỏa', 'Đinh': 'Hỏa', 'Mậu': 'Thổ', 'Kỷ': 'Thổ', 'Canh': 'Kim', 'Tân': 'Kim', 'Nhâm': 'Thủy', 'Quý': 'Thủy',
    'Tý': 'Thủy', 'Sửu': 'Thổ', 'Dần': 'Mộc', 'Mão': 'Mộc', 'Thìn': 'Thổ', 'Tỵ': 'Hỏa', 'Ngọ': 'Hỏa', 'Mùi': 'Thổ', 'Thân': 'Kim', 'Dậu': 'Kim', 'Tuất': 'Thổ', 'Hợi': 'Thủy'
}

NAP_AM = {
    # ... (Giữ nguyên danh sách NAP_AM 60 cặp như các bản trước) ...
    "Canh Thân": "Thạch Lựu Mộc", "Tân Dậu": "Thạch Lựu Mộc", "Nhâm Tuất": "Đại Hải Thủy", "Quý Hợi": "Đại Hải Thủy"
}

def tinh_diem(can, chi, na_str):
    h_can, h_chi = NGU_HANH[can], NGU_HANH[chi]
    h_na = na_str.split()[-1]
    d_can = 1 if h_can in ['Kim', 'Thổ'] else -1
    d_chi = 2 if h_chi in ['Kim', 'Thổ'] else -2
    d_na = 1 if h_na in ['Kim', 'Thổ'] else -1
    return d_can + d_chi + d_na

async def main():
    bot = telegram.Bot(token=TOKEN)
    
    # Lấy ngày hôm sau (Vì 23h là bắt đầu tính cho ngày mới)
    target_day = datetime.now() + timedelta(hours=2) 
    lunar = sxtwl.fromSolar(target_day.year, target_day.month, target_day.day)
    
    can_list = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    chi_list = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    
    day_can = can_list[lunar.getDayGZ().tg]
    day_chi = chi_list[lunar.getDayGZ().dz]
    
    labels, scores = [], []
    start_tg_idx = {0:0, 5:0, 1:2, 6:2, 2:4, 7:4, 3:6, 8:6, 4:8, 9:8}[lunar.getDayGZ().tg]
    
    msg = f"📊 **PHÂN TÍCH NGÀY MỚI: {day_can} {day_chi}**\n(Bắt đầu từ giờ Tý 23h00 hôm nay)\n\n"
    
    for i in range(12):
        h_can = can_list[(start_tg_idx + i) % 10]
        h_chi = chi_list[i]
        na = NAP_AM.get(f"{h_can} {h_chi}", "N/A")
        sc = tinh_diem(h_can, h_chi, na)
        labels.append(h_chi)
        scores.append(sc)
        status = "🟢" if sc >= 2 else "🔴" if sc <= -2 else "🟡"
        msg += f"{status} Giờ **{h_chi}**: {sc}đ\n"

    # Vẽ biểu đồ
    plt.figure(figsize=(10, 6))
    colors = ['#2ecc71' if s >= 2 else '#e74c3c' if s <= -2 else '#f39c12' for s in scores]
    plt.bar(labels, scores, color=colors, edgecolor='black')
    plt.axhline(0, color='black', linewidth=1)
    plt.title(f"Năng lượng 12 giờ ngày {day_can} {day_chi}")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    await bot.send_photo(chat_id=CHAT_ID, photo=buf, caption=msg, parse_mode='Markdown')

if __name__ == "__main__":
    asyncio.run(main())
