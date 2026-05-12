import requests
from datetime import datetime, timezone, timedelta
import jpholiday

# URL API
URL = "https://kintaiplus.freee.co.jp/gateway/bprgateway"

# Mapping ID cho từng hành động
ACTION_ID_MAP = {
    "checkin": "qmXXCxw9WEWN3X/YrkMWuQ==",
    "checkout": "j8ekmJaw6W3M4w3i6hlSIQ=="
}

def get_payload(action):
    return {
        "id": ACTION_ID_MAP.get(action, ""),  # Lấy ID phù hợp với action
        "highAccuracyFlg": "false",
        "credential_code": "40",
        "user_token": "b+BjgLd9RK2CVLCb8s48zwlxm3rJhpFhokqAnSuDahg=",
        "unique_timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "version": "1.4.20",
        "token": "wBWKU5POmq0uUDp83Ua5gw==",
        "d_param": "1743584638214"
    }

def detect_action(now_jst):
    hour = now_jst.hour
    minute = now_jst.minute
    total_minutes = hour * 60 + minute

    # CHECKIN: 07:30 (450) – 09:00 (540)
    if 450 <= total_minutes <= 540:
        return "checkin"

    # CHECKOUT: 18:00 (1080) – 19:30 (1170)
    if 1090 <= total_minutes <= 1290:
        return "checkout"

    return None

def send_request(action, now_jst):
    today = now_jst.date()
    weekday = today.weekday()  # 0 = Monday, 6 = Sunday

    print(f"🕒 UTC Time: {datetime.now(timezone.utc)}")
    print(f"🕒 JST Time: {now_jst.strftime('%Y-%m-%d %H:%M:%S')} "
          f"({now_jst.hour * 60 + now_jst.minute} phút từ 0h)")

    # ⛔ Thứ Bảy / Chủ Nhật
    if weekday in [5, 6]:
        print(f"⏭ {action.upper()} bị bỏ qua "
              f"(Hôm nay là Thứ {'Bảy' if weekday == 5 else 'Chủ Nhật'})")
        return

    # ⛔ Ngày lễ Nhật Bản
    if jpholiday.is_holiday(today):
        holiday_name = jpholiday.is_holiday_name(today) or "Holiday"
        print(f"🎌 {action.upper()} bị bỏ qua "
              f"(Ngày lễ Nhật Bản: {holiday_name})")
        return

    # ✅ Gửi request
    payload = get_payload(action)
    print(f"📡 Sending {action.upper()} request with payload:")
    print(payload)

    response = requests.post(URL, data=payload)

    print("📨 HTTP Status Code:", response.status_code)
    print("📨 API Response:", response.text)

    if response.status_code == 200:
        print(f"✅ {action.upper()} thành công!")
    else:
        print(f"❌ {action.upper()} thất bại: "
              f"{response.status_code} - {response.text}")

if __name__ == "__main__":
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)

    action = detect_action(now)

    if action:
        print(f"🔍 Hành động xác định: {action.upper()}")
        send_request(action, now)
    else:
        print("⌛ Không nằm trong khung giờ check-in / check-out.")
        print("⏱️ Giờ chạy:", now.strftime("%Y-%m-%d %H:%M:%S (JST)"))
