# 📚 Bài tập code tự chấm với test case

## 🎯 Mục đích

Cho phép giáo viên tạo bài tập code với các test case, học viên nộp code và hệ thống tự động chấm điểm dựa trên kết quả test.

## 📝 Cách hoạt động

### 1. Giáo viên tạo bài tập

**Ví dụ bài tập:**
- **Đề bài:** "Viết hàm `tong(a, b)` để tính tổng 2 số nguyên"
- **Test case 1:**
  - Input: `a=2, b=3`
  - Output mong đợi: `5`
- **Test case 2:**
  - Input: `a=-1, b=1`
  - Output mong đợi: `0`
- **Test case 3:**
  - Input: `a=100, b=200`
  - Output mong đợi: `300`

### 2. Học viên viết code

```python
def tong(a, b):
    return a + b
```

### 3. Hệ thống tự động chấm

1. Chạy code của học viên với từng test case
2. So sánh output với kết quả mong đợi
3. Tính điểm:
   - Test case 1: ✅ Pass → +33 điểm
   - Test case 2: ✅ Pass → +33 điểm
   - Test case 3: ✅ Pass → +34 điểm
   - **Tổng: 100 điểm**

## 💡 Ví dụ thực tế

Các platform tương tự:
- **LeetCode**: Submit code → Auto judge với test cases
- **HackerRank**: Code challenge → Auto grading
- **Codeforces**: Contest problem → Auto test
- **Codewars**: Kata → Auto verify

## ✅ Lợi ích

- ✅ Giáo viên không cần chấm thủ công
- ✅ Học viên biết kết quả ngay lập tức
- ✅ Công bằng, khách quan
- ✅ Tiết kiệm thời gian
- ✅ Học viên có thể thử lại nhiều lần

## 🔧 Công nghệ có thể dùng

1. **Judge0 API** (miễn phí, dễ tích hợp)
   - API service có sẵn để chạy code
   - Hỗ trợ nhiều ngôn ngữ
   - Có rate limit

2. **Custom solution** (tự build)
   - Dùng Docker container để chạy code an toàn
   - Tự kiểm soát hoàn toàn
   - Tốn chi phí server

3. **Hybrid**
   - Dùng code execution API đã có (Coding Playground)
   - Thêm logic so sánh output với test case
   - Đơn giản, không cần API bên ngoài

## 📋 Luồng hoạt động chi tiết

```
Giáo viên tạo bài tập
    ↓
Định nghĩa test cases (input + expected output)
    ↓
Học viên xem đề bài
    ↓
Học viên viết code và submit
    ↓
Hệ thống chạy code với từng test case
    ↓
So sánh output với expected output
    ↓
Tính điểm và hiển thị kết quả
    ↓
Lưu điểm vào database
```

## 🎨 UI/UX đề xuất

**Trang bài tập code:**
- Hiển thị đề bài
- Code editor (như Coding Playground)
- Nút "Submit" để nộp bài
- Hiển thị kết quả:
  - ✅ Test case 1: Pass
  - ✅ Test case 2: Pass
  - ❌ Test case 3: Fail (Expected: 300, Got: 299)
  - **Điểm: 66/100**

