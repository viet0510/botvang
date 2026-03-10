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

    # 1. XÂY DỰNG NỘI DUNG TIN NHẮN VĂN BẢN (Tách riêng để không bị giới hạn ký tự)
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

    # 2. VẼ BIỂU ĐỒ
    plt.figure(figsize=(10, 6))
    colors = ['#2ecc71' if s >= 2 else '#e74c3c' if s <= -2 else '#f39c12' for s in scores]
    plt.bar(labels, scores, color=colors, edgecolor='black')
    plt.axhline(0, color='black', linewidth=1)
    plt.title(f"Năng lượng 12 giờ ngày {d_can} {d_chi}")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    # 3. GỬI ẢNH TRƯỚC, GỬI CHỮ SAU
    await bot.send_photo(chat_id=CHAT_ID, photo=buf)
    await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
