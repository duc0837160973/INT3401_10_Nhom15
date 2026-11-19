# Pacman – Search & Multiagent Search

## Mô tả dự án

Dự án triển khai các thuật toán trí tuệ nhân tạo trong môi trường Pacman, dựa trên bộ bài tập UC Berkeley CS188, gồm hai phần:

- **Project 1 – Search:** Cài đặt DFS, BFS, UCS và A* để tìm đường đến đích, đi qua bốn góc và thu thập thức ăn. Xây dựng các heuristic hỗ trợ tìm kiếm hiệu quả.
- **Project 2 – Multiagent Search:** Cài đặt Reflex Agent, Minimax, Alpha–Beta và Expectimax để Pacman lựa chọn hành động khi có ma. Xây dựng hàm đánh giá trạng thái dựa trên thức ăn, viên năng lượng và khoảng cách tới ma.
### Project 1 – Search: Các câu hỏi

| Câu | Nội dung |
|---|---|
| **Q1 – DFS** | Cài đặt tìm kiếm theo chiều sâu để tìm đường từ vị trí ban đầu đến đích. |
| **Q2 – BFS** | Cài đặt tìm kiếm theo chiều rộng để tìm đường có số bước ít nhất. |
| **Q3 – UCS** | Cài đặt tìm kiếm theo chi phí đồng nhất để tìm đường có tổng chi phí nhỏ nhất khi chi phí di chuyển có thể khác nhau. |
| **Q4 – A\*** | Cài đặt A* kết hợp chi phí đã đi và heuristic ước lượng chi phí còn lại đến đích. |
| **Q5 – CornersProblem** | Xây dựng biểu diễn trạng thái và điều kiện đích cho bài toán Pacman đi qua cả bốn góc của mê cung. |
| **Q6 – Corners Heuristic** | Xây dựng heuristic cho CornersProblem để A* giảm số nút mở rộng mà vẫn tìm được lời giải tối ưu. |
| **Q7 – Food Heuristic** | Xây dựng heuristic cho bài toán thu thập toàn bộ thức ăn, sử dụng cùng A*. |
| **Q8 – Suboptimal Search** | Cài đặt agent liên tiếp tìm đường đến thức ăn gần nhất bằng BFS; thu thập hết thức ăn nhưng không bảo đảm đường đi tổng thể ngắn nhất. |

### Project 2 – Multiagent Search: Các câu hỏi

| Câu | Nội dung |
|---|---|
| **Q1 – Reflex Agent** | Thiết kế hàm đánh giá hành động dựa trên trạng thái sau khi di chuyển, xét thức ăn và ma để lựa chọn hành động phù hợp. |
| **Q2 – Minimax** | Cài đặt Minimax cho Pacman và nhiều ma: Pacman tối đa hóa giá trị, còn ma tối thiểu hóa giá trị của Pacman. |
| **Q3 – Alpha–Beta Pruning** | Bổ sung cắt tỉa Alpha–Beta để bỏ qua các nhánh không ảnh hưởng đến kết quả Minimax, giảm lượng tìm kiếm. |
| **Q4 – Expectimax** | Cài đặt Expectimax, coi ma chọn ngẫu nhiên đều giữa các hành động hợp lệ và sử dụng giá trị kỳ vọng để ra quyết định. |
| **Q5 – Better Evaluation Function** | Xây dựng hàm đánh giá trạng thái cải tiến, kết hợp điểm số, thức ăn, viên năng lượng, khoảng cách và trạng thái sợ của ma. |
## Hướng dẫn chạy lại chương trình

### 1. Chuẩn bị

Cài đặt **Python 3**, tải repository và giải nén. Giữ đầy đủ các tệp của bộ khung Pacman, bản đồ và bộ kiểm thử.

Mở terminal trong thư mục chứa `pacman.py` của project tương ứng. Nếu máy sử dụng lệnh `python3`, thay `python` bằng `python3` trong các lệnh dưới đây.

### 2. Project 1 – Search

Chạy lần lượt các thuật toán trên bản đồ `mediumMaze`:

```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

Chạy bài toán đi qua bốn góc:

```bash
python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p AStarCornersAgent
```

Chạy bài toán thu thập thức ăn:

```bash
python pacman.py -l trickySearch -p AStarFoodSearchAgent
python pacman.py -l bigSearch -p ClosestDotSearchAgent -z 0.5
```

### 3. Project 2 – Multiagent Search

Chạy demo Expectimax với hàm đánh giá cải tiến:

```bash
python pacman.py -p ExpectimaxAgent -a depth=2,evalFn=better -l smallClassic -k 1
```

Chạy lại thực nghiệm so sánh các agent, mỗi cấu hình gồm 10 ván:

```bash
python pacman.py -p ReflexAgent -l smallClassic -k 1 -n 10 -q -f
python pacman.py -p MinimaxAgent -a depth=2 -l smallClassic -k 1 -n 10 -q -f
python pacman.py -p AlphaBetaAgent -a depth=2 -l smallClassic -k 1 -n 10 -q -f
python pacman.py -p ExpectimaxAgent -a depth=2 -l smallClassic -k 1 -n 10 -q -f
python pacman.py -p ExpectimaxAgent -a depth=2,evalFn=better -l smallClassic -k 1 -n 10 -q -f
```

Trong các lệnh trên:
- `-l`: bản đồ sử dụng.
- `-p`: agent điều khiển Pacman.
- `-k 1`: một ma.
- `-n 10`: chạy 10 ván.
- `-q`: không hiển thị giao diện.
- `-f`: sử dụng seed ngẫu nhiên cố định.
- `depth=2`: độ sâu tìm kiếm bằng 2.
- `evalFn=better`: sử dụng hàm đánh giá cải tiến.

Bỏ `-q` nếu muốn xem giao diện trò chơi.

### 4. Kiểm thử tự động

Chạy lệnh sau trong thư mục của từng project:

```bash
python autograder.py --no-graphics
```

Để kiểm thử riêng một câu, ví dụ Q5:

```bash
python autograder.py -q q5 --no-graphics
```
