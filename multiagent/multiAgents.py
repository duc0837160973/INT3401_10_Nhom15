# multiAgents.py - Project 2: Multi-Agent Search (Pacman, UC Berkeley CS188)
#
# Thay thế multiAgents.py trong bộ khung bằng file này.

from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent
from pacman import GameState


# ---------------------------------------------------------------------------
# Q1: Reflex Agent
# ---------------------------------------------------------------------------
class ReflexAgent(Agent):
    """
    Agent phản xạ: chọn hành động tốt nhất dựa trên evaluationFunction
    áp dụng cho trạng thái kế tiếp.
    """

    def getAction(self, gameState: GameState):
        legalMoves = gameState.getLegalActions()
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [i for i in range(len(scores)) if scores[i] == bestScore]
        chosenIndex = random.choice(bestIndices)  # chọn ngẫu nhiên giữa các hành động tốt nhất
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        successor = currentGameState.generatePacmanSuccessor(action)
        newPos = successor.getPacmanPosition()
        newFood = successor.getFood()
        newGhostStates = successor.getGhostStates()
        newScaredTimes = [g.scaredTimer for g in newGhostStates]

        score = successor.getScore()

        # Thức ăn: càng gần viên gần nhất càng tốt, càng ít thức ăn càng tốt
        foodList = newFood.asList()
        if foodList:
            nearestFood = min(manhattanDistance(newPos, f) for f in foodList)
            score += 10.0 / nearestFood if nearestFood > 0 else 10.0
        score -= 4 * len(foodList)

        # Ma
        for ghost, scared in zip(newGhostStates, newScaredTimes):
            d = manhattanDistance(newPos, ghost.getPosition())
            if scared > d:
                score += 20.0 / (d + 1)      # ma đang sợ: đuổi theo
            elif d <= 1:
                score -= 500                  # ma sát bên: rất nguy hiểm
            else:
                score -= 2.0 / d

        # Không khuyến khích đứng yên
        if action == Directions.STOP:
            score -= 10

        return score


def scoreEvaluationFunction(currentGameState: GameState):
    """Hàm đánh giá mặc định: chỉ trả về điểm số hiện tại."""
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    Lớp cha cho MinimaxAgent, AlphaBetaAgent, ExpectimaxAgent.
    depth: độ sâu tìm kiếm (1 tầng = Pacman đi + mọi con ma đi).
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman luôn là agent 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


# ---------------------------------------------------------------------------
# Q2: Minimax
# ---------------------------------------------------------------------------
class MinimaxAgent(MultiAgentSearchAgent):
    """Minimax với nhiều con ma (mỗi ma là một tầng MIN)."""

    def getAction(self, gameState: GameState):
        numAgents = gameState.getNumAgents()

        def minimax(state, agent, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            nextAgent = (agent + 1) % numAgents
            nextDepth = depth + 1 if nextAgent == 0 else depth

            values = [minimax(state.generateSuccessor(agent, a), nextAgent, nextDepth)
                      for a in state.getLegalActions(agent)]
            return max(values) if agent == 0 else min(values)

        bestValue, bestAction = float('-inf'), None
        for action in gameState.getLegalActions(0):
            value = minimax(gameState.generateSuccessor(0, action),
                            1 % numAgents, 1 if numAgents == 1 else 0)
            if value > bestValue:
                bestValue, bestAction = value, action
        return bestAction


# ---------------------------------------------------------------------------
# Q3: Alpha-Beta Pruning
# ---------------------------------------------------------------------------
class AlphaBetaAgent(MultiAgentSearchAgent):
    """Minimax có cắt tỉa alpha-beta."""

    def getAction(self, gameState: GameState):
        numAgents = gameState.getNumAgents()

        def value(state, agent, depth, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            nextAgent = (agent + 1) % numAgents
            nextDepth = depth + 1 if nextAgent == 0 else depth
            actions = state.getLegalActions(agent)

            if agent == 0:  # MAX
                v = float('-inf')
                for a in actions:
                    v = max(v, value(state.generateSuccessor(agent, a),
                                     nextAgent, nextDepth, alpha, beta))
                    if v > beta:      # chỉ cắt khi LỚN HƠN hẳn (không cắt khi bằng)
                        return v
                    alpha = max(alpha, v)
                return v
            else:           # MIN
                v = float('inf')
                for a in actions:
                    v = min(v, value(state.generateSuccessor(agent, a),
                                     nextAgent, nextDepth, alpha, beta))
                    if v < alpha:     # chỉ cắt khi NHỎ HƠN hẳn
                        return v
                    beta = min(beta, v)
                return v

        alpha, beta = float('-inf'), float('inf')
        bestValue, bestAction = float('-inf'), None
        for action in gameState.getLegalActions(0):
            v = value(gameState.generateSuccessor(0, action),
                      1 % numAgents, 1 if numAgents == 1 else 0, alpha, beta)
            if v > bestValue:
                bestValue, bestAction = v, action
            alpha = max(alpha, bestValue)   # không cắt tỉa ở nút gốc
        return bestAction


# ---------------------------------------------------------------------------
# Q4: Expectimax
# ---------------------------------------------------------------------------
class ExpectimaxAgent(MultiAgentSearchAgent):
    """Expectimax: các con ma chọn hành động ngẫu nhiên đều (uniform)."""

    def getAction(self, gameState: GameState):
        numAgents = gameState.getNumAgents()

        def expectimax(state, agent, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            nextAgent = (agent + 1) % numAgents
            nextDepth = depth + 1 if nextAgent == 0 else depth
            values = [expectimax(state.generateSuccessor(agent, a), nextAgent, nextDepth)
                      for a in state.getLegalActions(agent)]

            if agent == 0:
                return max(values)
            return sum(values) / len(values)   # kỳ vọng với xác suất đều

        bestValue, bestAction = float('-inf'), None
        for action in gameState.getLegalActions(0):
            v = expectimax(gameState.generateSuccessor(0, action),
                           1 % numAgents, 1 if numAgents == 1 else 0)
            if v > bestValue:
                bestValue, bestAction = v, action
        return bestAction


# ---------------------------------------------------------------------------
# Q5: Better Evaluation Function
# ---------------------------------------------------------------------------
def betterEvaluationFunction(currentGameState: GameState):
    """
    Hàm đánh giá trạng thái hiện tại (không phải hành động) gồm:
      - điểm số hiện tại
      - thưởng khi gần viên thức ăn gần nhất, phạt theo số thức ăn còn lại
      - phạt theo số viên capsule còn lại (khuyến khích ăn) + thưởng khi gần capsule
      - tránh ma bình thường, đuổi ma đang sợ (còn đủ thời gian)
    """
    if currentGameState.isWin() or currentGameState.isLose():
        return currentGameState.getScore()

    pos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()

    score = currentGameState.getScore()

    # Thức ăn
    if foodList:
        nearestFood = min(manhattanDistance(pos, f) for f in foodList)
        score += 10.0 / nearestFood if nearestFood > 0 else 10.0
    score -= 4 * len(foodList)

    # Capsule
    score -= 15 * len(capsules)
    if capsules:
        nearestCap = min(manhattanDistance(pos, c) for c in capsules)
        score += 5.0 / (nearestCap + 1)

    # Ma
    for ghost in ghostStates:
        d = manhattanDistance(pos, ghost.getPosition())
        if ghost.scaredTimer > d:
            score += 25.0 / (d + 1)        # có thể ăn ma
        elif d <= 1:
            score -= 500                    # sắp bị ma bắt
        else:
            score -= 3.0 / d

    return score


# Viết tắt
better = betterEvaluationFunction
