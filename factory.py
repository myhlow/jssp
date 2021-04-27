import time
import heapq
import enum

class Factory:
  jobs=None
  machines=None
  dispatchingRule=None

  def __init__(self):
    self.jobs=[]
    self.machines=[]

  def addJobs(self,j):
    self.jobs.append(j)

  def addMachines(self,m):
    self.machines.append(m)

  def numJobs(self):
    return len(self.jobs)

  def numMachines(self):
    return len(self.machines)

  def getOp(self,jID,opID):
    return self.jobs[jID].ops[opID]

  def get_google_jssp(self):
    data = []
    for j in self.jobs:
      jj = []
      for o in j.ops:
        jj.append((o.machineID, o.processTime))
      data.append(jj)
    return data

  def reset(self):
    for j in self.jobs:
      j.reset()
    for m in self.machines:
      m.queue=[]

  def setDispatchingRule(self,d):
    self.dispatchingRule=d

  def readProblem(self,link):
    #open JSSP problem file and read
    f = open(link, "r")
    line = 0
    txt = f.readline()

    i=0
    while txt != "":
      if line == 4:
        #read in number of jobs and machines
        j, m = txt.split()
        numJobs = int(j)
        numMachines = int(m)
        for m in range(numMachines):
          self.machines.append(Machine(m,self))    
        for j in range(numJobs):
          self.jobs.append(Job(j,self))

        txt = f.readline()
        #print("Num Jobs",numJobs,"Num Machines",numMachines)
      elif line > 4:
        #read in operations for each job
        arr = [int(n) for n in txt.split()]
        machineTime = list(zip(arr[::2], arr[1::2]))
        self.jobs[i].ops=[Op(i,o, mt[0], mt[1], self) for o,mt in enumerate(machineTime)]
        txt = f.readline()
        i=i+1
      else:
        #skips the first three lines
        txt = f.readline()
      line += 1

class MachineStatus(enum.IntEnum):
  FREE = 1
  BUSY = 2

class EventType(enum.IntEnum):
  GENERIC = 1
  OPEND = 2
  OPARRIVAL = 3
  OPSTART = 4
  MACHFREE = 5

class Event:
  time=-1
  eType=-1

  def __init__(self,t):
    self.time=t
    self.eType=EventType.GENERIC

  def run(self):
    print("Running event!")

  def __lt__(self,o):
    if self.time==o.time:
      return self.eType<o.eType
    else:
      return self.time<o.time

class OpArrival(Event):
  op=None

  def __init__(self,t,o):
    self.op=o
    super().__init__(t)
    self.eType=EventType.OPARRIVAL

  def toString(self):
    print(f"T{self.time} OpArrival event",end=":")
    self.op.toString()

  def run(self,eq):
    #$$ self.toString()
    self.op.availableTime=self.time
    factory=self.op.factory
    m1 = factory.machines[self.op.machineID]
    #$$ m1.toString()
    #Only schedule a MachineFree event if the queue is empty
    #and the machine is free
    if len(m1.queue)==0 and m1.status==MachineStatus.FREE:
      mfe=MachFree(self.time,m1)
      #print("===> Scheduing new MechFee event")
      #mfe.toString()
      #print()
      eq.addEvent(mfe)
    factory.machines[self.op.machineID].addOp(self.op)
    #$$ print()
    
class MachFree(Event):
  mach=None

  def __init__(self,t,m):
    self.mach=m
    super().__init__(t)
    self.eType=EventType.MACHFREE

  def toString(self):
    print(f"T{self.time} MachFree event",end=":")
    self.mach.toString()

  def run(self,eq):
    self.mach.status=MachineStatus.FREE
    #$$ self.toString()
    factory = self.mach.factory
    if len(self.mach.queue)!=0:
      #run the dispatching rule
      factory.dispatchingRule.run(self.mach)
      #op1=heapq.heappop(self.mach.queue)
      op1=self.mach.queue.pop(0)
      op1.startTime=self.time
      op1.endTime=op1.startTime+op1.processTime
      self.mach.status=MachineStatus.BUSY
      #$$ print(f"===> Machine Processing Op: M{op1.machineID} J{op1.jobID} O{op1.opID}")
      if op1.opID!=factory.numMachines()-1:
        op2=factory.jobs[op1.jobID].ops[op1.opID+1]
        op2e=OpArrival(op1.endTime,op2)
        #print("===> Scheduing new OpArrival event")
        #op2e.toString()
        #print()
        eq.addEvent(op2e)
      mfe=MachFree(op1.endTime,self.mach)
      #print("===> Scheduing new MechFee event")
      #mfe.toString()
      #print()
      eq.addEvent(mfe)
    #$$ print()

class EventQueue:
  queue=None
  time=-1

  def __init__(self):
    self.queue=[]
    time=0

  def addEvent(self,e):
    heapq.heappush(self.queue,e)

  def run(self):
    while len(self.queue)!=0:
      e=heapq.heappop(self.queue)
      self.time=e.time
      #print("++++ Running new event ++++")
      e.run(self)

class Job:
  jobID = -1
  ops=[]
  facotry=None
  
  def __init__(self, j, f):
    self.jobID=j
    self.factory=f

  def reset(self):
    for o in self.ops:
      o.reset()

  def toString(self):
    print("Job", self.jobID)
    for o in self.ops:
      o.toString()
    print("")

  def getNumOps(self):
    return len(self.ops)

class Op:
  jobID=-1
  opID=-1
  processTime=-1
  availableTime=-1
  startTime=-1
  endTime=-1
  machineID=-1
  priority=-1
  factory=None

  def __init__(self, j, o, m, pt,f):
    self.jobID=j
    self.opID=o
    self.processTime=pt
    self.machineID=m
    self.next=None
    self.priority=-1
    self.factory=f

  def reset(self):
    self.availableTime=-1
    self.startTime=-1
    self.endTime=-1
    self.priority=-1

  def __lt__(self,o):
    if self.priority==o.priority:
      return self.processTime<o.processTime
    else:
      return self.priority<o.priority

  def toString(self):
    print(f"J{self.jobID} O{self.opID} M{self.machineID} AT={self.availableTime} PT={self.processTime}, ST={self.startTime},ET={self.endTime}, PR={self.priority}")

class Machine:
  machineID=-1
  queue = None
  status = -1
  factory = None

  def __init__(self, m, f):
    self.status=MachineStatus.FREE
    self.machineID=m
    self.queue=[]
    self.factory=f

  def addOp(self,o):
    #heapq.heappush(self.queue,o)
    self.queue.append(o)

  def toString(self):
    print("Machine",self.machineID, self.status, end=" [")
    for o in self.queue:
      print(f"(J{o.jobID} O{o.opID} A{o.availableTime} P{o.processTime})",end=" ")
    print("]")
