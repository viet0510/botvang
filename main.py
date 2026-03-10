import telegram
import asyncio
from datetime import datetime, timedelta
import sxtwl
import matplotlib.pyplot as plt
import io

# --- ĐIỀN THÔNG TIN CỦA BÁC ---
TOKEN = 'ĐIỀN_TOKEN_VÀO_ĐÂY'
CHAT_ID = 'ĐIỀN_ID_VÀO_ĐÂY'

NGU_HANH = {
    'Giáp': 'Mộc', 'Ất': 'Mộc', 'Bính': 'Hỏa', 'Đinh': 'Hỏa', 'Mậu': 'Thổ', 'Kỷ': 'Thổ', 'Canh': 'Kim', 'Tân': 'Kim', 'Nhâm': 'Thủy', 'Quý': 'Thủy',
    'Tý': 'Thủy', 'Sửu': 'Thổ', 'Dần': 'Mộc', 'Mão': 'Mộc', 'Thìn': 'Thổ', 'Tỵ': 'Hỏa', 'Ngọ': 'Hỏa', 'Mùi': 'Thổ', 'Thân': 'Kim', 'Dậu': 'Kim', 'Tuất': 'Thổ', 'Hợi': 'Thủy'
}

NAP_AM = {
    "Giáp Tý": "Hải Trung Kim", "Ất Sửu": "Hải Trung Kim", "Bính Dần": "Lô Trung Hỏa", "Đinh Mão": "Lô Trung Hỏa",
    "Mậu Thìn": "Đại Lâm Mộc", "Kỷ Tỵ": "Đại Lâm Mộc", "Canh Ngọ": "Lộ Bàng Thổ", "Tân Mùi": "Lộ Bàng Thổ",
    "Nhâm Thân": "Kiếm Phong Kim", "Quý Dậu": "Kiếm Phong Kim", "Giáp Tuất": "Sơn Đầu Hỏa", "Ất Hợi": "Sơn Đầu Hỏa",
    "Bính Tý": "Giản Hạ Thủy", "Đinh Sửu": "Giản Hạ Thủy", "Mậu Dần": "Thành Đầu Thổ", "Kỷ Mão": "Thành Đầu Thổ",
    "Canh Thìn": "Bạch Lạp Kim", "Tân Tỵ": "Bạch Lạp Kim", "Nhâm Ngọ": "Dương Liễu Mộc", "Quý Mùi": "Dương Liễu Mộc",
    "Giáp Thân": "Tuyền Trung Thủy", "Ất Dậu": "Tuyền Trung Thủy", "Bính Tuất": "Ốc Thượng Thổ", "Đinh Hợi": "Ốc Thượng Thổ",
    "Mậu Tý": "Phích Lịch Hỏa", "Kỷ Sửu": "Phích Lịch Hỏa", "Canh Dần": "Tùng Bách Mộc", "Tân Mão": "Tùng Bách Mộc",
    "Nhâm Thìn": "Trường Lưu Thủy", "Quý Tỵ": "Trường Lưu Thủy", "Giáp Ngọ": "Sa Trung Kim", "Ất Mùi": "Sa Trung Kim",
    "Bính Thân": "Sơn Hạ Hỏa", "Đinh Dậu": "Sơn Hạ Hỏa", "Mậu Tuất": "Bình Địa Mộc", "Kỷ Hợi": "Bình Địa Mộc",
    "Canh Tý": "Bích Thượng Thổ", "Tân Sửu": "Bích Thượng Thổ", "Nhâm Dần": "Kim Bạch Kim", "Quý Mão": "Kim Bạch Kim",
    "Giáp Thìn": "Phú Đăng Hỏa", "Ất Tỵ": "Phú Đăng Hỏa", "Bính Ngọ": "Thiên Hà Thủy", "Đinh Mùi": "Thiên Hà Thủy",
    "Mậu Thân": "Đại Trạch Thổ", "Kỷ Dậu": "Đại Trạch Thổ", "Canh Tuất": "Thoa Xuyến Kim", "Tân Hợi": "Thoa Xuyến Kim",
    "Nhâm Tý": "Tang Đố Mộc", "Quý Sửu": "Tang Đố Mộc", "Giáp Dần": "Đại Khê Thủy", "Ất Mão": "Đại Khê Thủy",
    "Bính Thìn": "Sa Trung Thổ", "Đinh Tỵ": "Sa Trung Thổ", "Mậu Ngọ": "Thiên Thượng Hỏa", "Kỷ Mùi": "Thiên Thượng Hỏa",
    "Canh Thân": "Thạch Lựu Mộc", "Tân Dậu": "Thạch Lựu Mộc", "Nhâm Tuất": "Đại Hải Thủy", "Quý Hợi": "Đại Hải Thủy"
}

def check_noi_tai(can, chi):
    h_can, h_chi = NGU_HANH[can], NGU_HANH[chi]
    if h_can == h_chi: return "Tương Hòa"
    sinh = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
    khac = {'Mộc': 'Thổ', 'Thổ': 'Thủy', 'Thủy': 'Hỏa', 'Hỏa': 'Kim', 'Kim': 'Mộc'}
    if sinh[h_can] == h_chi: return f"{can} sinh {chi}"
    if sinh[h_chi] == h_can: return f"{chi} sinh {can}"
    if khac[h_can] == h_chi: return f"{can} khắc {chi}"
    if khac[h_chi] == h_can: return f"{chi} khắc {can}"
    return "Bình hòa"

def tinh_chi_tiet(can, chi, na_str):
    h_can, h_chi = NGU_HANH[can], NGU_HANH[chi]
    h_na = na_str.split()[-1]
    d_can = 1 if h_can in ['Kim', 'Thổ'] else -1
    d_chi = 2 if h_chi in ['Kim', 'Thổ'] else -2
    d_na = 1 if h_na in ['Kim', 'Thổ'] else -1
    return d_can, d_chi, d_na, (d_can + d_chi + d_na)

async def main():
    bot = telegram.Bot(token=TOKEN)
    # Lấy ngày mới (tính từ 23h đêm nay)
    target_day = datetime.now() + timedelta(hours=2) 
    lunar = sxtwl.fromSolar(target_day.year, target_day.month, target_day.day)
    
    can_list = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    chi_list = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    
    d_can, d_chi = can_list[lunar.getDayGZ().tg], chi_list[lunar.getDayGZ().dz]
    na_day = NAP_AM.get(f"{d_can} {d_chi}")
    dc_d, dchi_d, dna_d, t_day = tinh_chi_tiet(d_can, d_chi, na_day)

    # XÂY DỰNG NỘI DUNG TIN NHẮN CHI TIẾT
    msg = f"📊 **PHÂN TÍCH NGÀY MỚI: {d_can} {d_chi}**\n"
    msg += f"(Bắt đầu từ giờ Tý 23:00 hôm nay)\n\n"
    msg += f"• Thiên Can: {d_can} ➔ `{dc_d:+}đ`\n• Địa Chi: {d_chi} ➔ `{dchi_d:+}đ`\n• Nạp Âm: {na_day} ➔ `{dna_d:+}đ`\n"
    msg += f"• Nội tại Ngày: {check_noi_tai(d_can, d_chi)}\n"
    msg += f"➔ **TỔNG ĐIỂM NGÀY: {t_day:+}**\n"
    msg += "━━━━━━━━━━━━━━━\n\n"
    
    labels, scores = [], []
    start_tg_idx = {0:0, 5:0, 1:2, 6:2, 2:4, 7:4, 3:6, 8:6, 4:8, 9:8}[lunar.getDayGZ().tg]
    times = ["23:00-00:59", "01:00-02:59", "03:00-04:59", "05:00-06:59", "07:00-08:59", "09:00-10:59", "11:00-12:59", "13:00-14:59", "15:00-16:59", "17:00-18:59", "19:00-20:59", "21:00-22:59"]

    for i in range(12):
        h_can = can_list[(start_tg_idx + i) % 10]
        h_chi = chi_list[i]
        na = NAP_AM.get(f"{h_can} {h_chi}")
        c_g, chi_g, n_g, sc = tinh_chi_tiet(h_can, h_chi, na)
        
        labels.append(h_chi)
        scores.append(sc)
        
        icon = "🟢 BUY" if sc >= 2 else "🔴 SELL" if sc <= -2 else "🟡 ĐỨNG NGOÀI"
        msg += f"🕒 **{times[i]} ({h_can} {h_chi})**\n"
        msg += f"• C:{c_g:+} | Chi:{chi_g:+} | N.Âm:{n_g:+}\n"
        msg += f"• Nội tại: {check_noi_tai(h_can, h_chi)}\n"
        msg += f"➔ **Điểm Giờ: {sc:+}** | {icon}\n\n"

    # VẼ BIỂU ĐỒ TRỰC QUAN
    plt.figure(figsize=(10, 6))
    colors = ['#2ecc71' if s >= 2 else '#e74c3c' if s <= -2 else '#f39c12' for s in scores]
    plt.bar(labels, scores, color=colors, edgecolor='black')
    plt.axhline(0, color='black', linewidth=1)
    plt.title(f"Năng lượng 12 giờ ngày {d_can} {d_chi}")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    # GỬI CẢ ẢNH VÀ NỘI DUNG CHI TIẾT
    await bot.send_photo(chat_id=CHAT_ID, photo=buf, caption=msg, parse_mode='Markdown')

if __name__ == "__main__":
    asyncio.run(main())
