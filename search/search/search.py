"""
search.py - Project 1: Search (Pacman, UC Berkeley CS188)

Cài đặt các thuật toán tìm kiếm tổng quát: DFS, BFS, UCS, A*.
File này thay thế search.py trong bộ khung của project.
"""

import util


class SearchProblem:
    """
    Lớp trừu tượng mô tả một bài toán tìm kiếm.
    KHÔNG cần sửa lớp này.
    """

    def getStartState(self):
        """Trả về trạng thái bắt đầu."""
        util.raiseNotDefined()

    def isGoalState(self, state):
        """Trả về True nếu state là trạng thái đích."""
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        Trả về danh sách bộ ba (successor, action, stepCost):
        successor là trạng thái kế tiếp, action là hành động để tới đó,
        stepCost là chi phí của bước đi đó.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """Trả về tổng chi phí của một dãy hành động hợp lệ."""
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """Lời giải cứng cho tinyMaze, chỉ dùng để thử nghiệm."""
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


# ---------------------------------------------------------------------------
# Q1: Depth First Search
# ---------------------------------------------------------------------------
def depthFirstSearch(problem):
    """
    Tìm kiếm theo chiều sâu (graph search): mở rộng nút sâu nhất trước.
    Dùng Stack (LIFO) làm frontier. Trả về danh sách các hành động.
    """
    frontier = util.Stack()
    frontier.push((problem.getStartState(), []))
    explored = set()

    while not frontier.isEmpty():
        state, path = frontier.pop()

        if problem.isGoalState(state):
            return path

        if state in explored:
            continue
        explored.add(state)

        for successor, action, _ in problem.getSuccessors(state):
            if successor not in explored:
                frontier.push((successor, path + [action]))

    return []


# ---------------------------------------------------------------------------
# Q2: Breadth First Search
# ---------------------------------------------------------------------------
def breadthFirstSearch(problem):
    """
    Tìm kiếm theo chiều rộng (graph search): mở rộng nút nông nhất trước.
    Dùng Queue (FIFO) làm frontier.
    """
    frontier = util.Queue()
    start = problem.getStartState()
    frontier.push((start, []))
    explored = set()

    while not frontier.isEmpty():
        state, path = frontier.pop()

        if problem.isGoalState(state):
            return path

        if state in explored:
            continue
        explored.add(state)

        for successor, action, _ in problem.getSuccessors(state):
            if successor not in explored:
                frontier.push((successor, path + [action]))

    return []


# ---------------------------------------------------------------------------
# Q3: Uniform Cost Search
# ---------------------------------------------------------------------------
def uniformCostSearch(problem):
    """
    Mở rộng nút có tổng chi phí đường đi g(n) nhỏ nhất.
    Dùng PriorityQueue với độ ưu tiên = chi phí tích lũy.
    """
    frontier = util.PriorityQueue()
    frontier.push((problem.getStartState(), [], 0), 0)
    explored = set()

    while not frontier.isEmpty():
        state, path, cost = frontier.pop()

        if problem.isGoalState(state):
            return path

        if state in explored:
            continue
        explored.add(state)

        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in explored:
                newCost = cost + stepCost
                frontier.push((successor, path + [action], newCost), newCost)

    return []


def nullHeuristic(state, problem=None):
    """Heuristic tầm thường: luôn trả về 0 (khi đó A* = UCS)."""
    return 0


# ---------------------------------------------------------------------------
# Q4: A* Search
# ---------------------------------------------------------------------------
def aStarSearch(problem, heuristic=nullHeuristic):
    """
    A*: mở rộng nút có f(n) = g(n) + h(n) nhỏ nhất.
    Heuristic cần admissible (và consistent để graph search tối ưu).

    Lưu chi phí g tốt nhất của mỗi trạng thái đã mở rộng. Nếu sau này tìm được
    đường rẻ hơn tới cùng trạng thái đó thì mở rộng lại, nhờ vậy A* vẫn cho
    kết quả tối ưu kể cả khi heuristic chỉ admissible mà không consistent.
    """
    frontier = util.PriorityQueue()
    start = problem.getStartState()
    frontier.push((start, [], 0), heuristic(start, problem))
    bestCost = {}  # trạng thái -> chi phí g thấp nhất đã mở rộng

    while not frontier.isEmpty():
        state, path, cost = frontier.pop()

        if problem.isGoalState(state):
            return path

        # Bỏ qua nếu đã mở rộng trạng thái này với chi phí không tệ hơn
        if state in bestCost and bestCost[state] <= cost:
            continue
        bestCost[state] = cost

        for successor, action, stepCost in problem.getSuccessors(state):
            newCost = cost + stepCost
            if successor in bestCost and bestCost[successor] <= newCost:
                continue
            priority = newCost + heuristic(successor, problem)
            frontier.push((successor, path + [action], newCost), priority)

    return []


# Viết tắt
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
