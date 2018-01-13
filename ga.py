""" 
Name : Prateek Vachher
Student ID : 5392364
X500 : vachh007
Email ID : vachh007@umn.edu
Class : CSCI 1133
Lecturer : Dr. Amy Larson

"""

##############    Import Statement     ##############

import maze, maze_samples, math, copy, random

##############    Genetic Algorithm Class Definition     ##############

class ga:
  def __init__(self,maze):        ### Constructor
    self.maze = maze
    self.mouse = []
    self.cheese = []
    self.pointer = []
    self.find_position()

  def find_position(self):        ### Finds Position of Cheese and Mouse
    maze = self.maze
    for y in range(len(maze)):
        for x in range(len(maze[y])):
          if maze[y][x] == 'M':
            self.mouse = [x,y]
            self.pointer = [x,y]
          elif maze[y][x] == 'C':
            self.cheese = [x,y]

  def distance_cheese_mouse(self,mouse,cheese):       ### Finds Euclidean Distance between Mouse and Cheese
    return (math.sqrt(((mouse[0]-cheese[0])**2) + ((mouse[1]-cheese[1])**2)))

  def fitness_function(self,moves):         ### Calculates Fitness Score for a set of moves
    maze = copy.deepcopy(self.maze)
    position_mouse = copy.deepcopy(self.pointer)
    fitness_points = 0
    for k in range(len(moves)):
      if moves[k] == 'U':
        if position_mouse[1] == 0 or maze[position_mouse[1]-1][position_mouse[0]] == 'x':
          pass
        else:
          position_mouse[1] -= 1
          fitness_points += 1

      elif moves[k] == 'D':
        if position_mouse[1] == len(maze)-1 or maze[position_mouse[1]+1][position_mouse[0]] == 'x':
          pass
        else:
          position_mouse[1] += 1
          fitness_points += 1

      elif moves[k] == 'L':
        if position_mouse[0] == 0 or maze[position_mouse[1]][position_mouse[0]-1] == 'x':
          pass
        else:
          position_mouse[0] -= 1
          fitness_points += 1

      elif moves[k] == 'R':
        if position_mouse[0] == len(maze[0])-1 or maze[position_mouse[1]][position_mouse[0]+1] == 'x':
          pass
        else:
          position_mouse[0] += 1
          fitness_points += 1
      else:
        pass
      
      if maze[position_mouse[1]][position_mouse[0]] == 'C':
        fitness_points += 100000
        moves = moves[:k+1]
        break
      elif position_mouse == self.mouse:
        fitness_points = 0
    fitness_points -= self.distance_cheese_mouse(self.pointer,self.cheese)
    return [fitness_points,moves]


##############    Individual Class Definition     ##############

class individual:
  def __init__(self,move):      ### Constructor
    self.move = move
    self.fitness = 0

  def cross_breed(self,parent1,parent2):      ### CrossBreeding between 2 Parents
    break_point = random.randint(1,min(len(parent1.move),len(parent2.move))-1)
    child1 = individual(parent1.move[:break_point] + parent2.move[break_point:])
    child2 = individual(parent2.move[:break_point] + parent1.move[break_point:])
    return [child1,child2]

  def mutate(self,individual1):       ### Mutate Individual
    individual1 = list(individual1.move)
    mutate_rate = 90      ### Mutation Rate out of 100
    if random.randint(0,100) < mutate_rate:
      idx = random.randint(0,len(individual1)-1)
      m = random.randint(1,4)
      to_be_mutated = ""
      if m == 1:
        to_be_mutated = 'U'
      elif m == 2:
        to_be_mutated = 'D'
      elif m == 3:
        to_be_mutated = 'L'
      elif m == 4:
        to_be_mutated = 'R'
      individual1[idx] = to_be_mutated
    return individual(''.join(individual1))

  def SetWeightsForMonteCarloSelection(self,values):    ### Setting Weights for Monte Carlo Selection
    normalized_values = [int(v/sum(values)*100+.5) for v in values]
    accum = 0
    selection_weights = []
    for w in normalized_values:
      accum += w
      selection_weights.append(accum)
    return selection_weights

  def MonteCarloSelection(self,selection_weights):       ### Monte Carlo Selection
    selection = random.randint(0,selection_weights[-1])
    for i,w in enumerate(selection_weights):
      if selection <= w:
        return i

  def generate_random(self,length):       ### Random Generation of First Generation Individuals
      final = ""
      for x in range(length):
          num = random.randint(0,400)
          letter = ""
          if num <= 100:
              letter = 'U'
          elif num <= 200:
              letter = 'L'
          elif num <= 300:
              letter = 'D'
          else:
              letter = 'R'
          final += letter
      return final

def main():
  test_case = 0           ###  Test_Case for Maze
  sample_individual = individual('UDLR')    ### Sample Instance for Class Individual 

  number_of_population = 1000     ### Number of Population
  generations_of_population = 5  ### Generation of Population

  population = [individual(sample_individual.generate_random(maze_samples.string_length[test_case])) for x in range(number_of_population)]      ### Create an array of population of first generation
  gmap = ga(maze_samples.maze[test_case][::-1])     ### Initializing Grid Map
  M = maze.Maze(maze_samples.maze[test_case])
  M.Visualize()

  while generations_of_population > 1:
    generations_of_population -= 1
    
    for p in population:
      p.fitness = gmap.fitness_function(p.move)[0]      ### Calculating Fitness Score for each individual of Population
    
    new_generation = []               ### Blank List for New Generation

    L = [y.fitness for y in population]     ### List of Fitness Scores of Population

    S = sample_individual.SetWeightsForMonteCarloSelection(L)     ### Setting Weights for Monte Carlo Selection

    for p in range(len(population)//2):
      p1 = sample_individual.MonteCarloSelection(S)         ### 1st Parent from Monte Carlo Selection 
      p2 = sample_individual.MonteCarloSelection(S)         ### 2nd Parent from Monte Carlo Selection
      p3 = sample_individual.cross_breed(population[p1],population[p2])     ### Cross Breeding Parent1 and Parent2
      new_generation.extend([sample_individual.mutate(x) for x in p3])      ### Adding New Population to New_Generation

    random.shuffle(new_generation)    ### Shuffling New_Generation Array

    if max([x.fitness for x in population]) > 100:        ### If Fitness Score of any element is Greater than 100, Break
      for x in range(len(population)):
        if population[x].fitness > 200:
          p1 = gmap.fitness_function(population[x].move)[1]
          sample_individual = population[x]
          break
      break

    else:
      for x in range(len(population)):                          #### Calculating Maximum Fitness Score in Population
        if population[x].fitness > sample_individual.fitness:
          sample_individual = population[x]

    population = new_generation         ### New_Generaton is now Population
  M.RunMaze(gmap.fitness_function(sample_individual.move)[1])     ### Simulates Run Maze with Maximum Fitness Score in all population and generations

if __name__=='__main__' :
  main()        ### Executing Main Function
  input()       ### Input statement such that code doesnt crash and break before seeing the result