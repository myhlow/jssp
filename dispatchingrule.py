class DispatchingRule:
  factory=None

  def __init__(self,f):
    self.factory=f

  def run(self,m):
    machine=m
    m.queue=sorted(m.queue, key=lambda x:x.processTime)

class NN_Rule(DispatchingRule):
  def __init__(self,f):
    super().__init__(f)

  def run(self,m):
    m.queue=sorted(m.queue, key=lambda x:x.priority)

class NN_SPT_Rule(DispatchingRule):
  def __init__(self,f):
    super().__init__(f)

  def run(self,m):
    m.queue=sorted(m.queue, key=lambda x:(x.priority,x.processTime))

class SPT_Rule(DispatchingRule):
  def __init__(self,f):
    super().__init__(f)

  def run(self,m):
    m.queue=sorted(m.queue, key=lambda x:x.processTime)

class NN_WINQ_Rule(DispatchingRule):
  def __init__(self,f):
    super().__init__(f)

  def getWINQ(self,o):
    job=self.factory.jobs[o.jobID]
    if o.opID==job.getNumOps()-1:
      return 0
    else:
      nextMachineID = job.ops[o.opID+1].machineID 
      m = self.factory.machines[nextMachineID]
      remainingTime=0
      for o1 in m.queue:
        remainingTime=remainingTime+o1.processTime
      return remainingTime

class WINQ_Rule(DispatchingRule):
  def __init__(self,f):
    super().__init__(f)

  def getWINQ(self,o):
    job=self.factory.jobs[o.jobID]
    if o.opID==job.getNumOps()-1:
      return 0
    else:
      nextMachineID = job.ops[o.opID+1].machineID 
      m = self.factory.machines[nextMachineID]
      remainingTime=0
      for o1 in m.queue:
        remainingTime=remainingTime+o1.processTime
      return remainingTime
     
  def run(self,m):
    m.queue=sorted(m.queue, key=lambda x:self.getWINQ(x))

class NN_SPTWINQ_Rule(DispatchingRule):
  def __init__(self,f):
    super().__init__(f)

  def getWINQ(self,o):
    job=self.factory.jobs[o.jobID]
    if o.opID==job.getNumOps()-1:
      return 0
    else:
      nextMachineID = job.ops[o.opID+1].machineID 
      m = self.factory.machines[nextMachineID]
      remainingTime=0
      for o1 in m.queue:
        remainingTime=remainingTime+o1.processTime
      return remainingTime
  
  def run(self,m):
    m.queue=sorted(m.queue, key=lambda x:(x.priority,x.processTime+self.getWINQ(x)))

class SPTWINQ_Rule(DispatchingRule):
  def __init__(self,f):
    super().__init__(f)

  def getWINQ(self,o):
    job=self.factory.jobs[o.jobID]
    if o.opID==job.getNumOps()-1:
      return 0
    else:
      nextMachineID = job.ops[o.opID+1].machineID 
      m = self.factory.machines[nextMachineID]
      remainingTime=0
      for o1 in m.queue:
        remainingTime=remainingTime+o1.processTime
      return remainingTime
  
  def run(self,m):
    m.queue=sorted(m.queue, key=lambda x:x.processTime+self.getWINQ(x))

class NN_MTWR_Rule(DispatchingRule):
  def __init__(self,f):
    super().__init__(f)

  def getMTWR(self,o):
    remainingTime=0
    job=self.factory.jobs[o.jobID]
    for i in range(o.opID,job.getNumOps()):
      remainingTime=remainingTime+job.ops[i].processTime
    return remainingTime

  def run(self,m):
    m.queue=sorted(m.queue, key=lambda x:self.getMTWR(x), reverse=True)
    m.queue=sorted(m.queue, key=lambda x:x.priority)

class MTWR_Rule(DispatchingRule):
  def __init__(self,f):
    super().__init__(f)

  def getMTWR(self,o):
    remainingTime=0
    job=self.factory.jobs[o.jobID]
    for i in range(o.opID,job.getNumOps()):
      remainingTime=remainingTime+job.ops[i].processTime
    return remainingTime

  def run(self,m):
    m.queue=sorted(m.queue, key=lambda x:self.getMTWR(x), reverse=True)

class NN_FDDMTWR_Rule(DispatchingRule):
  def __init__(self,f):
    super().__init__(f)

  def getFDDMTWR(self,o):
    remainingTime=0
    fdd=0
    job=self.factory.jobs[o.jobID]
    for i in range(job.getNumOps()):
      fdd=fdd+job.ops[i].processTime
    for i in range(o.opID,job.getNumOps()):
      remainingTime=remainingTime+job.ops[i].processTime
    return fdd/remainingTime

  def run(self,m):
    m.queue=sorted(m.queue, key=lambda x:self.getFDDMTWR(x))
    m.queue=sorted(m.queue, key=lambda x:x.priority)

class FDDMTWR_Rule(DispatchingRule):
  def __init__(self,f):
    super().__init__(f)

  def getFDDMTWR(self,o):
    remainingTime=0
    fdd=0
    job=self.factory.jobs[o.jobID]
    for i in range(job.getNumOps()):
      fdd=fdd+job.ops[i].processTime
    for i in range(o.opID,job.getNumOps()):
      remainingTime=remainingTime+job.ops[i].processTime
    return fdd/remainingTime

  def run(self,m):
    m.queue=sorted(m.queue, key=lambda x:self.getFDDMTWR(x))
