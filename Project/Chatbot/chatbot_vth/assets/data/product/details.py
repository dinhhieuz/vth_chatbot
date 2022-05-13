from pydoc import describe


# note: template có 80 kí tự giới hạn
#--> DỤNG CỤ
dung_cu = {
    'Bình Tưới Cây': 'Chất liệu PP với dung tích 1.5L, chống trầy',
    'Bình Xịt Áp Suất Cầm Tay': 'Chất liệu Nhựa PP có dung tích 2L',
    'Bình Xịt Tưới Cây 2 Lít': 'Dung tích 2L có nhựa HDPE (220x130x275mm)',
    'Bộ Cưa Tay Đa Năng Tiện Dụng 6 Lưỡi Cưa': 'Cả bộ cưa (30x21x3cm) với nhiều loại lưỡi, nặng 0.6kg',
    'Găng Tay Nông Nghiệp Có Móng Vuốt Chuyên Dụng Làm Vườn': 'Chất liệu Cao su Polyeste và Nhựa ABS',
    'Kéo Cắt Cỏ Cầm Tay': 'Từ Đức với lưỡi cắt 23cm có kích thước (373x154x42mm) nặng 296g',
    'Kéo Tỉa Cây Gardena': 'Từ Đức với lưỡi chống dính (750x220x50mm) nặng 1.305kg',
    'Kìm Cắt Tỉa Cành Gardena': 'Từ Đức với chất liệu kim loại, nhựa HDPE (245x110x25mn)',
    'Kìm Tỉa Cành Cán Dài Gardena': 'Từ Đức với tay cầm nhôm và nhựa HDPE (560x175x30mn)',
    'Lưới Làm Giàn Leo Cây': 'Sợ cưới HDPE dày 2mm có mặt lưới 14x14cm',
    'Tấm Lót Sàn Nhựa Ban Công 3T-Eco': 'Từ nhựa PVC dài 30x30 nặng 500g với nhiều màu sắc',
    'Xẻng Làm Vườn Không Gỉ Jpk': 'Chất liệu thép không gỉ (14x7x30cm)',
    'Xẻng Trồng Cây Mini Gardena': 'Với nhựa HDPE có trọng lượng nhẹ 240g (335x80x45mm)',
    'Xẻng Xới Đất Mini Thép Không Gỉ Cao Cấp': 'Tay cầm nhựa cao su dẽo (9x32cm)',
}

#--> HẠT GIỐNG CỦ QUẢ
cu_qua = {
    'Hạt Giống Bí Đỏ Hồ Lô': 'Thu hoạch trong 60-80 ngày 4-6 quả/cây với 1 trái 4, 5kg (Tỉ lệ nảy mầm: 70-85%)',
    'Hạt Giống Dưa Leo': 'Thu hoạch trong 30-50 ngày, thường trồng Đông Xuân (Tỉ lệ nảy mầm: 85-95%)',
    'Hạt Giống Khổ Qua': 'Thu hoạch trong 40-45 ngày. Quả dài 20-25cm nặng 200-350g (Tỉ lệ nảy mầm: 85-95%)',
    'Hạt Giống Mướp Ngọt': 'Thu hoạch trong 55-65 ngày, trồng quanh năm (Tỉ lệ nảy mầm: 80-90%)',
    'Hạt Giống Ớt Hiểm': 'Thu hoạch trong 70-80 ngày, diện tích trồng 50x50cm (Tỉ lệ nảy mầm: 75%) ',
}

#--> HẠT GIỐNG RAU XANH
rau_xanh = {
    'Hạt Giống Cây Cà Chua Bạch Tuộc': 'Thu hoạch trong 60-70 ngày, trái nặng 120-150g (Tỉ lệ nảy mầm: 85-96%)',
    'Hạt Giống Rau Cải Kale': 'Thu hoạch trong 30-40 ngày, cao tầm 20-25cm (Tỉ lệ nảy mầm: > 85%)',
    'Hạt Giống Rau Cải Ngọt': 'Thu hoạch trong 35-75 ngày, gốc Ấn và Trung (Tỉ lệ nảy mầm: > 75%)',
    'Hạt Giống Rau Càng Cua': 'Thu hoạch trong 35-40 ngày, rất dể trồng (Tỉ lệ nảy mầm: >85%)',
    'Hạt Giống Rau Dền Đỏ': 'Thu hoạch trong 25-30 ngày, cây chịu được khí hậu nắng (Tỉ lệ nảy mầm: >80%)',
    'Hạt Giống Rau Má': 'Thu hoạch trong 40-60 ngày, cây có sức sống mạnh, dễ trồng (Tỉ lệ nảy mầm: >85%)',
    'Hạt Giống Rau Mồng Tơi Lá To': 'Thu hoạch trong khoảng 30 ngày, (Tỉ lệ nảy mầm: 85-96%)',
    'Hạt Giống Rau Muống': 'Thu hoạch trong 60-70 ngày, (Tỉ lệ nảy mầm: 85-96%)',
    'Hạt Giống Rau Ngò Rí': 'Thu hoạch trong 60-70 ngày, (Tỉ lệ nảy mầm: 85-96%)',
}

#--> SEN ĐÁ
sen_da = {
    'Sen Đá Cánh Bướm': 'Cây có lá là những cặp xếp đối xứng nhau và là loài cây rất dễ chăm sóc.',
    'Sen Đá Chuỗi Ngọc': 'Cây mọc dạng chuỗi ra các chùm hạt tròn trĩnh và loài rất dễ chăm sóc.',
    'Sen Đá Đất Xanh': 'Cây cao từ 15-20cm, có thể nhân giống từ lá và rất dể chăm sóc',
    'Sen Đá Kim Cương': 'Cây lá mọng nước, dày và cứng cáp, tốc độ sinh trưởng nhanh và dễ chăm sóc',
    'Sen Đá Móng Rồng Sọc Trắng': 'Cây lá nhọn và vằn trắng có thể nhân giống bằng lá',
    'Sen Đá Ngọc Bích': 'Cây có màu xanh, có thể nhân giống và ưa ánh sáng không quá gắt',
    'Sen Đá Nhật Nguyệt': 'Cây Có thể nhân giống từ lá, ưa nắng không gắt, tưới cho sen đá 3 lần/ tuần',
}

#NOTE: tư vấn theo câu hỏi
# attribute = {
#     'Sen Đá Cánh Bướm' : {
#         "nơi trồng" : ["văn phòng", "gia đình", "bang công"],
#         "ý nghĩa" : "30",
#         "ánh sáng":["ẩm", "nắng gắt", "nắng nhẹ"]
#     },
#     'Sen Đá Chuỗi Ngọc' : [],
#     'Sen Đá Đất Xanh' : [],
#     'Sen Đá Kim Cương' : [],
#     'Sen Đá Móng Rồng Sọc Trắng' : [],
#     'Sen Đá Nhật Nguyệt' : [],

# }