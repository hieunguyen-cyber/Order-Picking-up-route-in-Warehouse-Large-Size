# Order-Picking-up-route-in-Warehouse-Large-Size
Dưới đây là nội dung đã được chuyển sang định dạng Markdown:

# Problem

## Statement

---

### **Mô tả**

Có **M** kệ hàng trong một kho lớn, được đánh số từ 1, 2, …, M, trong đó kệ số **j** nằm tại vị trí **j** trong kho (j = 1, …, M).

Có **N** loại sản phẩm, được đánh số từ 1, 2, …, N. Số lượng sản phẩm **i** tại kệ **j** là **Q[i][j]**.

Nhân viên kho bắt đầu từ cửa kho (vị trí 0), và muốn ghé thăm một số kệ (mỗi kệ chỉ được ghé tối đa một lần và không nhất thiết đi qua tất cả các kệ) rồi quay lại cửa kho để lấy các sản phẩm theo **đơn hàng của khách hàng**, trong đó tổng số lượng sản phẩm **i** cần lấy là **q[i]** (với i = 1, 2, …, N).

Khoảng cách di chuyển từ vị trí **i** đến vị trí **j** là **d(i,j)** (với 0 ≤ i, j ≤ M).

**Yêu cầu**: Tìm ra trình tự các kệ cần ghé thăm sao cho tổng khoảng cách di chuyển là **nhỏ nhất**.

---

### **Đầu vào (Input)**

- Dòng 1: hai số nguyên dương **N** và **M** (1 ≤ N ≤ 50, 1 ≤ M ≤ 1000)  
- Dòng 2 đến N+1: mỗi dòng là một hàng của ma trận **Q**  
- Dòng N+2 đến N+M+2: mỗi dòng là một hàng của ma trận khoảng cách **d**  
- Dòng N+M+3: chứa các giá trị **q[1], q[2], …, q[N]**

---

**Một lời giải được biểu diễn bằng một dãy các số nguyên dương x₁, x₂, …, xₙ đại diện cho thứ tự các kệ cần ghé thăm.**

---

### **Đầu ra (Output)**

- Dòng 1: một số nguyên dương **n** (số lượng kệ cần ghé)  
- Dòng 2: n số nguyên dương **x₁, x₂, …, xₙ** (thứ tự các kệ)

---

### **Ví dụ**

#### **Input**
```
6 5
3 2 2 4 2
4 3 7 3 5
6 7 2 5 4
2 3 3 2 1
2 5 7 6 1
7 2 1 6 5
0 16 10 13 13 19
16 0 8 3 19 5
10 8 0 7 23 11
13 3 7 0 16 6
13 19 23 16 0 22
19 5 11 6 22 0
8 7 4 8 11 13
```
#### **Output**
```
4
2 3 1 5
```
#### **Giải thích**  
Lộ trình của nhân viên kho là: ```0 → 2 → 3 → 1 → 5 → 0```
