# PyADB - Thư viện Python để giao tiếp với ADB

PyADB là một thư viện Python giúp giao tiếp với ADB (Android Debug Bridge), cho phép bạn thực hiện các thao tác trên thiết bị Android từ mã Python, như cài đặt ứng dụng, chụp ảnh màn hình, gửi lệnh shell và nhiều chức năng khác.

## Cài đặt

```bash
pip install pyadb
```

## Yêu cầu

- Python 3.11 trở lên
- ADB được cài đặt trong PATH (hoặc chỉ định đường dẫn trực tiếp)

## Tính năng chính

- Quản lý kết nối ADB
- Thao tác với thiết bị Android (multi-device hỗ trợ)
- Cài đặt/gỡ cài đặt ứng dụng
- Truyền file giữa máy tính và thiết bị
- Shell commands
- Nhập liệu và thao tác UI
- Chụp ảnh và quay video màn hình
- Kiểm tra trạng thái thiết bị
- Các thao tác hệ thống (reboot, kết nối wifi, etc.)

## Cách sử dụng

### Kết nối và làm việc với ADB

```python
from pyadb import ADB

# Khởi tạo ADB
adb = ADB()  # Sử dụng ADB từ PATH
# HOẶC
adb = ADB(adb_path="/path/to/adb")  # Chỉ định đường dẫn cụ thể

# Liệt kê các thiết bị đã kết nối
devices = adb.devices()
print(devices)  # [{'serial': 'ABCD123', 'status': 'device'}, ...]

# Chạy lệnh ADB
output = adb.run_command("version")
print(output)

# Chạy lệnh Shell
output = adb.shell("ls", "-l", "/sdcard")
print(output)
```

### Làm việc với một thiết bị cụ thể

```python
from pyadb import Device

# Sử dụng thiết bị mặc định (thiết bị đầu tiên tìm thấy)
device = Device()

# HOẶC chỉ định thiết bị cụ thể
device = Device(serial="ABCD123")

# Thông tin thiết bị
model = device.get_model()
android_version = device.get_android_version()
api_level = device.get_api_level()

print(f"Thiết bị: {model}, Android {android_version}, API {api_level}")

# Thao tác tập tin
device.push("local_file.txt", "/sdcard/remote_file.txt")
device.pull("/sdcard/remote_file.txt", "local_copy.txt")

# Cài đặt/Gỡ cài đặt ứng dụng
device.adb.install("app.apk")
device.adb.uninstall("com.example.app")

# Làm việc với ứng dụng
device.start_app("com.example.app", ".MainActivity")
device.stop_app("com.example.app")
device.clear_app_data("com.example.app")

# Chụp ảnh màn hình
device.take_screenshot("screenshot.png")

# Quay video màn hình
device.record_screen("screen_recording.mp4", time_limit=10)

# Nhập và thao tác UI
device.input_text("Hello world")
device.tap(500, 500)  # Chạm vào tọa độ (500, 500)
device.swipe(100, 500, 400, 500)  # Vuốt từ trái sang phải
device.press_back()
device.press_home()

# Lấy thông tin hệ thống
battery_info = device.get_battery_info()
print(f"Pin: {battery_info.get('level')}%")

# Khởi động lại
device.reboot()  # Khởi động bình thường
device.reboot("recovery")  # Khởi động vào recovery mode

# Kết nối qua WiFi
ip = device.get_ip_address()
device.connect_wifi(ip)
```

## Xử lý lỗi

Thư viện cung cấp các lớp ngoại lệ để xử lý các lỗi có thể gặp phải:

```python
from pyadb import ADB, ADBError, DeviceNotFoundError

try:
    adb = ADB()
    device = adb.devices()
except DeviceNotFoundError:
    print("Không tìm thấy thiết bị nào được kết nối!")
except ADBError as e:
    print(f"Lỗi ADB: {e}")
```

## Tham khảo

Tài liệu về ADB: [https://developer.android.com/tools/adb](https://developer.android.com/tools/adb)