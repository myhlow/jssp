# Importing the matplotlb.pyplot 
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.patches import Patch
from matplotlib.lines import Line2D 
import random

def plotChart(factory): 

  plt.style.use('seaborn-white')
  makespan=max([j.ops[factory.numMachines()-1].endTime for j in factory.jobs])

  xlim = makespan

  # Declaring a figure "gnt" 
  #fig,gnt = plt.subplots() 
  #ax = fig.add_subplot(122)
  figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

  hspace=6

  ax1 = plt.subplot2grid((1,10),(0,0),rowspan=1,colspan=8)
  ax2 = plt.subplot2grid((1,10),(0,8),rowspan=1,colspan=2)
  ax2.axes.get_yaxis().set_visible(False)
  ax2.axes.get_xaxis().set_visible(False)
  ax2.spines["top"].set_visible(False)
  ax2.spines["left"].set_visible(False)
  ax2.spines["right"].set_visible(False)
  ax2.spines["bottom"].set_visible(False)
  
  # Setting Y-axis limits 
  ax1.set_ylim(0, (factory.numMachines()+1)*hspace) 
  
  # Setting X-axis limits 
  ax1.set_xlim(0, xlim) 
         
  ax1.set_title("Hello World")
  print("Hello World")
  # Setting labels for x-axis and y-axis 
  ax1.set_xlabel('Time') 
  ax1.set_ylabel('Machines') 
    
  # Setting ticks on y-axis 
  ax1.set_yticks([hspace*x for x in range(1,factory.numMachines()+1)]) 
  # Labelling tickes of y-axis 
  ax1.set_yticklabels([x for x in range(factory.numMachines())]) 

  #gnt.set_xticks([x for x in range(0,xlim,20)]) 
  #gnt.set_xticklabels([x for x in range(0,xlim,20)]) 

  r = lambda: random.randint(0, 255)
  #color=['#%02X%02X%02X' % (r(), r(), r()) for x in range(factory.numJobs())]  
  #print(color)
  color=['#%02X%02X%02X' % (x, r(), r()) for x in range(0,255,int(255/factory.numJobs()))]  
  # Setting graph attribute 
  ax1.grid(True) 
    
  # Declaring a bar in schedule 
  for j in range(factory.numJobs()):
    for o in factory.jobs[j].ops:
      ax1.broken_barh([(o.startTime, o.processTime)], ((o.machineID+1)*hspace-(hspace/2)+1, hspace-2), facecolors =(color[j]), edgecolors=('tab:grey')) 
 
  legend_elements = [Patch(facecolor=color[x], edgecolor='r',label='Job'+str(x)) for x in range(factory.numJobs())] 

  ax2.legend(handles=legend_elements, loc='lower right')
  #ax.axis("off")
  #ax.autoscale()
  #gnt.autoscale()
  plt.savefig("gantt1.png") 

#plotChart(factory1)
