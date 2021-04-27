import time


class Scheduler:
  def schedule(factory, problemName, dispatchRule):
      starttime = time.clock()
           
      if (dispatchRule == 'NN'):
          dispatchRule=NN_Rule(factory)
          factory.setDispatchingRule(dispatchRule)

      elif (dispatchRule == 'NN_SPT'):
          dispatchRule=NN_SPT_Rule(factory)
          factory.setDispatchingRule(dispatchRule)

      elif (dispatchRule == 'NN_MTWR'):
          dispatchRule=NN_MTWR_Rule(factory)
          factory.setDispatchingRule(dispatchRule)

      elif (dispatchRule == 'NN_WINQ'):
          dispatchRule=NN_WINQ_Rule(factory)
          factory.setDispatchingRule(dispatchRule)

      # elif (dispatchRule == 'SPS'):
      #     print(Decoder.mlprintScheduleSPS(jobSchedule, re.split(r' |/|\\', problemName)[-1], "ft06Extended", numMachines,
      #                                      numJobs, numOperations, ganttChartOption))
      elif (dispatchRule == 'NN_FDD/MTWR'):
          dispatchRule=NN_FDDMTWR_Rule(factory)
          factory.setDispatchingRule(dispatchRule)

      elif (dispatchRule == 'NN_FDD/MTWR'):
          dispatchRule=NN_FDDMTWR_Rule(factory)
          factory.setDispatchingRule(dispatchRule)

      # elif (dispatchRule == 'OPFSLK/PT'):
      #     print(Decoder.mlprintScheduleOPFSLKPT(jobSchedule, re.split(r' |/|\\', problemName)[-1], "ft06Extended", numMachines,
      #                                           numJobs, numOperations, ganttChartOption))
      elif (dispatchRule == 'NN_SPT+WINQ'):
          dispatchRule=NN_SPTWINQ_Rule(factory)
          factory.setDispatchingRule(dispatchRule)

      elif (dispatchRule == 'SPT'):
          dispatchRule=SPT_Rule(factory)
          factory.setDispatchingRule(dispatchRule)

      elif (dispatchRule == 'MTWR'):
          dispatchRule=MTWR_Rule(factory)
          factory.setDispatchingRule(dispatchRule)

      elif (dispatchRule == 'WINQ'):
          dispatchRule=WINQ_Rule(factory)
          factory.setDispatchingRule(dispatchRule)

      # elif (dispatchRule == 'SPS'):
      #     print(Decoder.mlprintScheduleSPS(jobSchedule, re.split(r' |/|\\', problemName)[-1], "ft06Extended", numMachines,
      #                                      numJobs, numOperations, ganttChartOption))
      elif (dispatchRule == 'FDD/MTWR'):
          dispatchRule=FDDMTWR_Rule(factory)
          factory.setDispatchingRule(dispatchRule)

      elif (dispatchRule == 'FDD/MTWR'):
          dispatchRule=FDDMTWR_Rule(factory)
          factory.setDispatchingRule(dispatchRule)

      # elif (dispatchRule == 'OPFSLK/PT'):
      #     print(Decoder.mlprintScheduleOPFSLKPT(jobSchedule, re.split(r' |/|\\', problemName)[-1], "ft06Extended", numMachines,
      #                                           numJobs, numOperations, ganttChartOption))
      elif (dispatchRule == 'SPT+WINQ'):
          dispatchRule=SPTWINQ_Rule(factory)
          factory.setDispatchingRule(dispatchRule)     
      # elif (dispatchRule == 'EDD/MOPNR'):
      #     print(Decoder.mlprintScheduleEDDMOPNR(jobSchedule, re.split(r' |/|\\', problemName)[-1], "ft06Extended", numMachines,
     #                                           numJobs, numOperations, ganttChartOption))
      else:
          print("No matching dispatching rule found!")
    
      eq=EventQueue()
      for j in factory.jobs:
        firstOp = j.ops[0]
        op1=OpArrival(0,firstOp)
        eq.addEvent(op1)
      eq.run()
      makespan=eq.time
      endtime = time.clock() 
      totaltime = endtime - starttime
      return makespan,totaltime
