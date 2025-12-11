# Nguyên Lý Và Thuật Toán Starfield Simulation

<p align="center">
  <a href="./README.md">English</a> &nbsp;|&nbsp; <b>Tiếng Việt</b>
</p>

Tài liệu này giải thích chi tiết cơ chế hoạt động của hiệu ứng Starfield Simulation (Mô phỏng trường sao). Đây là bài toán kinh điển trong đồ họa máy tính để tạo ảo giác chiều sâu 3D trên màn hình phẳng 2D.

## 1. Khái Niệm Cơ Bản

Mục tiêu của hiệu ứng này là mô phỏng góc nhìn của một camera đang di chuyển với tốc độ cao xuyên qua một đám mây sao. Thực tế, camera đứng yên, và các ngôi sao di chuyển về phía camera.

Để làm được điều này, ta cần:

- Một không gian 3 chiều ảo.

- Một công thức để "chiếu" (project) các điểm từ không gian 3 chiều đó lên màn hình 2 chiều.

## 2. Hệ Tọa Độ Giả Lập

Chúng ta tưởng tượng một chiếc hộp không gian với gốc tọa độ $(0,0,0)$ nằm ở tâm màn hình hoặc tại vị trí mắt người xem.

Mỗi ngôi sao là một điểm dữ liệu gồm 3 biến số:

- X (Ngang): Vị trí trái/phải so với tâm.

- Y (Dọc): Vị trí trên/dưới so với tâm.

- Z (Độ sâu): Khoảng cách từ ngôi sao đến mắt người xem.

Quy ước: Trục Z dương hướng vào trong màn hình (xa dần). Khi Z giảm nghĩa là ngôi sao đang bay lại gần bạn.

## 3. Công Thức "Perspective Projection" (Phép Chiếu Phối Cảnh)

Đây là "trái tim" của thuật toán. Để biến tọa độ 3D $(x, y, z)$ thành tọa độ màn hình 2D $(sx, sy)$, ta sử dụng nguyên lý tam giác đồng dạng.

Công thức cốt lõi:

$$sx = \frac{x}{z} \times FOV + center_{x}$$

$$sy = \frac{y}{z} \times FOV + center_{y}$$

Giải thích tham số:

- $x / z$ và $y / z$: Đây là phép chia quan trọng nhất.

  - Khi $z$ lớn (sao ở xa): Kết quả phép chia nhỏ $\rightarrow$ Sao nằm gần tâm màn hình.

  - Khi $z$ nhỏ (sao ở gần): Kết quả phép chia lớn $\rightarrow$ Sao bị đẩy dạt ra phía rìa màn hình.

  - Sự thay đổi này tạo ra ảo giác ngôi sao đang lao về phía bạn.

- FOV (Field of View): Hệ số phóng đại. Giá trị này quyết định "độ rộng" của ống kính. FOV càng lớn, góc nhìn càng hẹp và cảm giác tốc độ càng cao.

- Center Offset: Vì gốc tọa độ màn hình máy tính thường là góc trên-trái $(0,0)$, ta cần cộng thêm một nửa chiều rộng/chiều cao màn hình để dời gốc tọa độ ảo về chính giữa.

## 4. Quy Trình Thuật Toán (Logic Loop)

Để chương trình hoạt động, bạn cần thiết lập một vòng lặp vô tận (Game Loop) với các bước sau cho từng ngôi sao:

### Bước 1: Khởi Tạo (Initialization)

Tạo ra một mảng chứa $N$ ngôi sao. Mỗi ngôi sao được gán giá trị ngẫu nhiên cho $x, y$ và $z$.

- $x$: Random trong khoảng chiều rộng ảo.

- $y$: Random trong khoảng chiều cao ảo.

- $z$: Random từ 0 đến độ sâu tối đa (Max Depth).

### Bước 2: Cập Nhật (Update - Vật Lý)

Trong mỗi khung hình, thực hiện với từng ngôi sao:

1. Di chuyển: Giảm giá trị $z$ của sao một lượng bằng speed ($z = z - speed$).

2. Kiểm tra biên (Respawn):

- Nếu $z \le 0$ (sao đã bay qua mặt camera), ngôi sao đó coi như biến mất.

- Ta lập tức "tái sinh" nó bằng cách:

  - Đặt lại $z$ về vị trí xa nhất (Max Depth).

  - Chọn lại $x, y$ ngẫu nhiên mới.

  - Mẹo: Đặt lại $x, y$ mới giúp sao không bị lặp lại quỹ đạo cũ, tạo cảm giác vũ trụ vô tận.

### Bước 3: Hiển Thị (Render - Đồ Họa)

Sau khi cập nhật vị trí $z$, ta tính toán để vẽ:

1. Áp dụng công thức Perspective Projection ở mục 3 để tìm tọa độ màn hình $(sx, sy)$.

2. Tính kích thước: Sao càng gần ($z$ nhỏ) thì vẽ kích thước càng lớn để tăng tính chân thực.

3. Vẽ: Vẽ một hình tròn hoặc điểm sáng tại $(sx, sy)$.

## 5. Các Kỹ Thuật Nâng Cao

Để hiệu ứng đẹp mắt hơn (giống screensaver Windows), bạn có thể thêm các logic sau:

- Hiệu ứng Vệt (Star Trails):

  - Thay vì vẽ một điểm, hãy lưu lại vị trí $z$ của khung hình trước đó ($old\_z$).

  - Tính tọa độ màn hình cho cả $z$ hiện tại và $old\_z$.

  - Vẽ một đường thẳng nối hai điểm này. Sao càng gần, đường thẳng càng dài, tạo hiệu ứng "Warp Speed".

- Độ sáng theo khoảng cách: Sao ở xa ($z$ lớn) thì vẽ màu tối/mờ. Sao lại gần thì sáng dần lên trắng tinh.

- Tương tác: Gán biến speed hoặc tọa độ tâm (center_x, center_y) theo vị trí chuột để giả lập việc bẻ lái phi thuyền.
