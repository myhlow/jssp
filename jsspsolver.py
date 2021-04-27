import collections

# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print("Objective function: ",self.ObjectiveValue())

    def solution_count(self):
        return self.__solution_count

def MinimalJobshopSat(jobs_data, makespan):
    """Minimal jobshop problem."""
    # Create the model.
    model = cp_model.CpModel()

    #jobs_data = [  # task = (machine_id, processing_time).
    #    [(0, 3), (1, 2), (2, 2)],  # Job0
    #    [(0, 2), (2, 1), (1, 4)],  # Job1
    #    [(1, 4), (2, 3)]  # Job2
    #]

    #WSC data
    #jobs_data = [
    #  [(0,3),(1,5),(2,2)],
    #  [(2,2),(0,3),(1,2)],
    #  [(2,5),(0,6),(1,3)]
    #]

    # FTP06
    #jobs_data = [
    #[(2, 1), (0, 3), (1,  6), (3,  7),  (5,  3),  (4,  6)],
    #[(1, 8), (2, 5), (4, 10), (5, 10),  (0, 10),  (3,  4)],
    #[(2, 5), (3, 4), (5,  8), (0,  9),  (1, 10),  (4,  7)],
    #[(1, 5), (0, 5), (2,  5), (3,  3),  (4,  8),  (5,  9)],
    #[(2, 9), (1, 3), (4,  5), (5,  4),  (0,  3),  (3,  1)],
    #[(1, 3), (3, 3), (5,  9), (0, 10),  (4,  4),  (2,  1)]
    #]
    
    machines_count = 1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)

    # Computes horizon dynamically as the sum of all durations.
    #horizon = sum(task[1] for job in jobs_data for task in job)
    horizon = makespan

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple('task_type', 'start end interval')
    # Named tuple to manipulate solution information.
    assigned_task_type = collections.namedtuple('assigned_task_type',
                                                'start job index duration')

    # Creates job intervals and add to the corresponding machine lists.
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine = task[0]
            duration = task[1]
            suffix = '_%i_%i' % (job_id, task_id)
            start_var = model.NewIntVar(0, horizon, 'start' + suffix)
            end_var = model.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                                'interval' + suffix)
            all_tasks[job_id, task_id] = task_type(start=start_var,
                                                   end=end_var,
                                                   interval=interval_var)
            machine_to_intervals[machine].append(interval_var)

    # Create and add disjunctive constraints.
    for machine in all_machines:
        model.AddNoOverlap(machine_to_intervals[machine])

    # Precedences inside a job.
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(all_tasks[job_id, task_id +
                                1].start >= all_tasks[job_id, task_id].end)

    # Makespan objective.
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [
        all_tasks[job_id, len(job) - 1].end
        for job_id, job in enumerate(jobs_data)
    ])
    model.Minimize(obj_var)

    # Solve model.
    solver = cp_model.CpSolver()
    #status = solver.Solve(model)

    solution_printer = VarArraySolutionPrinter()
    status = solver.SolveWithSolutionCallback(model, solution_printer)

    if status == cp_model.OPTIMAL:
        # Create one list of assigned tasks per machine.
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(start=solver.Value(
                        all_tasks[job_id, task_id].start),
                                       job=job_id,
                                       index=task_id,
                                       duration=task[1]))

        # Create per machine output lines.
        output = ''
        for machine in all_machines:
            # Sort by starting time.
            assigned_jobs[machine].sort()
            sol_line_tasks = 'Machine ' + str(machine) + ': '
            sol_line = '           '

            for assigned_task in assigned_jobs[machine]:
                name = 'job_%i_%i' % (assigned_task.job, assigned_task.index)
                # Add spaces to output to align columns.
                sol_line_tasks += '%-10s' % name

                start = assigned_task.start
                duration = assigned_task.duration
                sol_tmp = '[%i,%i]' % (start, start + duration)
                # Add spaces to output to align columns.
                sol_line += '%-10s' % sol_tmp

            sol_line += '\n'
            sol_line_tasks += '\n'
            output += sol_line_tasks
            output += sol_line

        # Finally print the solution found.
        print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
        print(output)

#for x in JSSPBenchmark.problems:
#  factory1=Factory()
#  factory1.readProblem('problems/'+x)
  #factory1.show()
#  print(x, JSSPBenchmark.problems[x])
  #MinimalJobshopSat(factory1.get_google_jssp())
