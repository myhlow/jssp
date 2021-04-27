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
