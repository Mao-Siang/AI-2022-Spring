from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        '''
        terminate condition: gameState is loss or win or we reach the target depth,
        then return the evaluated score.
        First get the legalActions of current gameState.
        If current agent is Pacman(maxPlayer), we get the score by calling function for all possible next action 
        until we reach the terminate states and get the corresponding score.
        Because the next player after pacman is the No.1 ghost, we set the agent to 1 and maxPlayer=False.
        then we return the max score and the corresponding action(May have more than one, randomly choose one)

        If current agent is ghost, call function for all possible next action 
        until we reach the terminate states and get the score.
        For the last ghost, because the next agent is Pacman, we set the next agent = Pacman and maxPlayer=True
        For the other ghosts, set the next agent = current agent number + 1 and maxPlayer=False.
        then we return the minimum score and the correspoding action(May have more than one, randomly choose one)
        '''
        def minimaxAction(gameState, agent, depth, maxPlayer = True):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), Directions.STOP
            
            legalActions = gameState.getLegalActions(agent)
            if maxPlayer:
                scores = [minimaxAction(gameState.getNextState(agent, action), 1, depth, False)[0] for action in legalActions]
                bestScore = max(scores)
                bestIndex = [index for index in range(len(scores)) if scores[index] == bestScore]
                return bestScore, legalActions[random.choice(bestIndex)]
            else:
                scores = []
                if agent == gameState.getNumAgents() - 1:
                    scores = [minimaxAction(gameState.getNextState(agent, action), 0, depth - 1,True)[0] for action in legalActions]
                else :
                    scores = [minimaxAction(gameState.getNextState(agent, action), agent + 1, depth, False)[0] for action in legalActions]
                bestScore = min(scores)
                bestIndex = [index for index in range(len(scores)) if scores[index] == bestScore]
                return bestScore, legalActions[random.choice(bestIndex)]

            

        return minimaxAction(gameState, 0, self.depth, True)[1]
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        '''
        terminate condition: gameState is loss or win or we reach the target depth,
        then return the evaluated score.
        First get the legalActions of current gameState.
        If current agent is Pacman(maxPlayer), we get the score by calling function for all possible next action 
        until we reach the terminate states and get the corresponding score.
        If we found a score that is bigger than the Min's best option, we do the pruning.
        Because the next player after pacman is the No.1 ghost, we set the agent to 1 and maxPlayer=False.
        then we return the max score and the corresponding action(May have more than one, randomly choose one)

        If current agent is ghost, call function for all possible next action 
        until we reach the terminate states and get the score.
        If we found a score that is smaller than the Max's best option, we do the pruning.
        For the last ghost, because the next agent is Pacman, we set the next agent = Pacman and maxPlayer=True
        For the other ghosts, set the next agent = current agent number + 1 and maxPlayer=False.
        then we return the minimum score and the correspoding action(May have more than one, randomly choose one)
        '''
        def alphabetaAction(gameState, agent, depth, a, b, maxPlayer = True):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), Directions.STOP
            
            legalActions = gameState.getLegalActions(agent)
            if maxPlayer:
                maxScore = -1e100
                candidateActions = []
                for action in legalActions:
                    curScore = alphabetaAction(gameState.getNextState(agent, action), 1, depth, a,b,False)[0]
                    a = max(a, curScore)
                    if  curScore > maxScore:
                        maxScore = curScore
                        candidateActions = [action]
                    elif curScore == maxScore:
                        candidateActions.append(action)

                    if maxScore > b: break
                return maxScore, random.choice(candidateActions)
            else:
                minScore = 1e100
                candidateActions = []
                legalActions = gameState.getLegalActions(agent)
                if agent == gameState.getNumAgents() - 1:
                    for action in legalActions:
                        curScore = alphabetaAction(gameState.getNextState(agent, action), 0, depth - 1, a, b, True)[0]
                        b = min(b, curScore)
                        if curScore < minScore:
                           minScore = curScore
                           candidateActions = [action]
                        elif curScore == minScore:
                            candidateActions.append(action)
                        if minScore < a : break
                    return minScore, random.choice(candidateActions)
                else :
                    for action in legalActions:
                        curScore = alphabetaAction(gameState.getNextState(agent, action), agent + 1, depth, a, b, False)[0]
                        b = min(b, curScore)
                        if curScore < minScore:
                           minScore = curScore
                           candidateActions = [action]
                        elif curScore == minScore:
                            candidateActions.append(action)
                        if minScore < a : break
                    return minScore, random.choice(candidateActions)
               

            

        return alphabetaAction(gameState, 0, self.depth, -1e100, 1e100, True)[1]
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        '''
        terminate condition: gameState is loss or win or we reach the target depth,
        then return the evaluated score.
        First get the legalActions of current gameState.
        
        If current agent is Pacman(maxPlayer), we get the score by calling function for all possible next action 
        until we reach the terminate states and get the corresponding score.
        Because the next player after pacman is the No.1 ghost, we set the agent to 1 and maxPlayer=False.
        then we return the max score and the corresponding action(May have more than one, randomly choose one)

        If current agent is ghost, call function for all possible next action 
        until we reach the terminate states and get the score.
        For the last ghost, because the next agent is Pacman, we set the next agent = Pacman and maxPlayer=True
        For the other ghosts, set the next agent = current agent number + 1 and maxPlayer=False.
        then we return the average score as expected value and Direction.STOP
        
        '''
        def expectmax(gameState, agent, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState), Directions.STOP

            legalAction = gameState.getLegalActions(agent)
            if agent == 0:
                scores = [expectmax(gameState.getNextState(agent, action), 1, depth)[0] for action in legalAction]
                bestScore = max(scores)
                bestIndex = [index for index in range(len(scores)) if scores[index] == bestScore]
                return bestScore, legalAction[random.choice(bestIndex)]
            else:   
                scores = []
                if agent == gameState.getNumAgents() - 1:
                    scores = [expectmax(gameState.getNextState(agent, action), 0, depth - 1)[0] for action in legalAction]
                    return sum(scores)/len(scores), Directions.STOP
                else:
                    scores = [expectmax(gameState.getNextState(agent, action), agent + 1, depth)[0] for action in legalAction]
                    return sum(scores)/len(scores), Directions.STOP

        return expectmax(gameState, 0, self.depth)[1]
                
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    '''
    calculate number of foods whose manhatten distance < 20 and store in foodnum
    calculate number of ghosts whose manhatten distance < 8 and store in ghostnum

    closestFood() return the distance of closest food 
    closestGhost() return the distance of closest ghost
    closestCapsule() return the distance of closest capsule
    scaredtime stores ghoststate.scaredtimer for all ghosts

    score += foodnum*3 (make pacman close to foods)
    if the distance to closest ghost is less than 5 or ghostnum > 2,
    score += len(currentGameState.getLegalActions()) * 7 make pacman stay at intersection
    which is easier to escape

    score -= closestCapsule(pacmanPos, capsulePos) * 11 make pacman stay closer to capsule
    
    if minimum of scaretime > closestGhost, score -= closestGhost(pacmanPos, ghostPos) * 8
    to chase the closest ghost and eat it.

    if the max scaretime < 5, the chance to chase over the ghost is lower, so we focus on food and
    capsule by 
        score -= closestFood(pacmanPos, foodPos)
        score -= closestCapsule(pacmanPos, capsulePos)*2

    if the ghost is very close (distance < 4) to us and it is still scared for a while, we chase it by 
        score -= closestGhost(pacmanPos, ghostPos)

    As a consequence, the pacman will stay near capsule and intersection when there are more than
    two ghost nearby or the nearest ghost is too close.
    '''
    def closestFood(pacmanPos, foodPos):
        dis = []
        for pos in foodPos:
            dis.append(manhattanDistance(pacmanPos, pos))
        return min(dis) if len(dis) > 0 else 1

    def closestGhost(pacmanPos, ghostPos):
        dis = []
        for pos in ghostPos:
            dis.append(manhattanDistance(pacmanPos, pos))
        return min(dis) if len(dis) > 0 else 1
    def closestCapsule(pacmanPos, capsulePos):
        dis = []
        for pos in capsulePos:
            dis.append(manhattanDistance(pacmanPos, pos))
        return min(dis) if len(dis) > 0 else 0
    pacmanPos = currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood().asList()
    ghostPos = currentGameState.getGhostPositions()
    capsulePos = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    scaredtime = [i.scaredTimer for i in ghostStates]
    score = currentGameState.getScore()
    ghostnum = 0
    foodnum = 0

    for ghost in ghostPos:
        if manhattanDistance(pacmanPos, ghost) < 20:
            ghostnum += 1

    for food in foodPos:
        if manhattanDistance(pacmanPos, food) < 8:
            foodnum += 1
    
    score += foodnum * 3
    
    if max(scaredtime) < 5 :
        score -= closestFood(pacmanPos, foodPos)
        score -= closestCapsule(pacmanPos, capsulePos)*2

    if min(scaredtime) > closestGhost(pacmanPos, ghostPos) + 5:
        score -= closestGhost(pacmanPos, ghostPos) * 8

    if closestGhost(pacmanPos, ghostPos) < 5 or ghostnum >= 2:
        if max(scaredtime) == 0: score += closestGhost(pacmanPos, ghostPos)*0.35
        score += len(currentGameState.getLegalActions()) * 7 # * 10
        score -= closestCapsule(pacmanPos, capsulePos) * 11

    if closestGhost(pacmanPos, ghostPos) < 4 and min(scaredtime) > 2:
        score -= closestGhost(pacmanPos, ghostPos)
    return score

    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
