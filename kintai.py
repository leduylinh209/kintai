import requests
import argparse
from datetime import datetime, timezone, timedelta
import jpholiday  # Kiểm tra ngày lễ Nhật Bản

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

def send_request(action):
    # Đặt múi giờ Nhật Bản (UTC+9)
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    today = now.date()
    weekday = today.weekday()  # 0 = Monday, 6 = Sunday

    print(f"🕒 Giờ hệ thống (UTC): {datetime.now(timezone.utc)}")
    print(f"🕒 Giờ Nhật Bản (JST): {now}")

    # Kiểm tra nếu hôm nay là Thứ 7, Chủ Nhật hoặc ngày lễ
    if weekday in [5, 6]:  
        print(f"⏭ {action.upper()} bị bỏ qua (Hôm nay là Thứ {'Bảy' if weekday == 5 else 'Chủ Nhật'})")
        return
    
    if jpholiday.is_holiday(today):  
        print(f"🎌 {action.upper()} bị bỏ qua (Hôm nay là ngày lễ Nhật Bản: {jpholiday.holiday_name(today)})")
        return

    # Lấy payload phù hợp với action
    payload = get_payload(action)
    print(f"📡 Sending {action.upper()} request with payload: {payload}")

    response = requests.post(URL, data=payload)

    if response.status_code == 200:
        print(f"✅ {action.upper()} thành công!")
    else:
        print(f"❌ {action.upper()} thất bại:", response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["checkin", "checkout"], required=True)
    args = parser.parse_args()
    
    send_request(args.action)