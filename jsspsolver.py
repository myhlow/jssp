import collections
from ortools.sat.python import cp_model
import time

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0
        self.start=t.perf_counter()
        self.x = []
        self.y = []

    def on_solution_callback(self):
        self.__solution_count += 1
        elapsed_time = t.perf_counter()-self.start 
        self.x.append(elapsed_time)
        self.y.append(self.ObjectiveValue())
        #plt.xlabel("makespan")
        #plt.ylabel("time(s)")
        #plt.grid(axis = 'both')
        #plt.plot(self.x,self.y, color="black")
        #plt.text(0.02, 0.5, "Hello", fontsize=14)
        #display.clear_output(wait=True)
        #display.display(plt.gcf())

        print("Time:", elapsed_time, " Objective function: ",self.ObjectiveValue())

    def solution_count(self):
        return self.__solution_count

def GoogleORSATSolver(factory1,horizon):
    """Showcases calling the solver to search for all solutions."""
    # Creates the model.
    model = cp_model.CpModel()

    # Creates job intervals and add to the corresponding machine lists.
    jobs = [ [] for j in range(factory1.numJobs()) ]
    machines = [ [] for m in range(factory1.numMachines()) ]

    for j in range(factory1.numJobs()):
      duration = 0
      for o in range(factory1.numMachines()):
        opString = 'J%iO%i' % (factory1.jobs[j].ops[o].jobID, factory1.jobs[j].ops[o].opID)
        start = model.NewIntVar(duration, horizon, 'start' + opString)
        end = model.NewIntVar(duration, horizon, 'end' + opString)
        interval = model.NewIntervalVar(start, factory1.jobs[j].ops[o].processTime, end,'interval' + opString)
        jobs[j].append([start,end])
        machines[factory1.jobs[j].ops[o].machineID].append(interval)
        duration=duration+factory1.jobs[j].ops[o].processTime
    
    # ensure that jobs processed by the same machine do not overlap
    for m in range(factory1.numMachines()):
      model.AddNoOverlap(machines[m])

    # ensure that operations within a job are precessed in order
    for j in range(factory1.numJobs()):
      for o in range(factory1.numMachines()-1):
        # ensure the start time of the next operation
        # is later or equal to the end time of the previous operation
        model.Add(jobs[j][o+1][0]>=jobs[j][o][1])

    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [jobs[j][factory1.numMachines()-1][1] for j in range(factory1.numJobs())])
    model.Minimize(obj_var)

    # Create a solver and solve.
    solver = cp_model.CpSolver()
    #status = solver.Solve(model)
  
    solution_printer = VarArraySolutionPrinter()
    status = solver.SolveWithSolutionCallback(model, solution_printer)

    print('Status = %s' % solver.StatusName(status))

    for m1 in factory1.machines:
      for j in range(factory1.numJobs()):
        for o in range(factory1.numMachines()):
          if factory1.jobs[j].ops[o].machineID==m1.machineID:
            factory1.jobs[j].ops[o].startTime = solver.Value(jobs[j][o][0])
            factory1.jobs[j].ops[o].endTime = solver.Value(jobs[j][o][1])
            #print(f"M{m1.machineID} J{j}{o} {solver.Value(jobs[j][o][0])} {solver.Value(jobs[j][o][1])} {factory1.jobs[j].ops[o].processTime}")
        
    print('Optimal Schedule Length: %i' % solver.ObjectiveValue())

#SearchForAllSolutionsSampleSat()
