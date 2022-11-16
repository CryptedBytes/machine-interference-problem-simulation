from time import sleep
from threading import Thread
import os


queue = []
significantValues = [0]


repairmanBusy = False
const_repairTime = 5
const_operationalTime = 10
mc = 0
cl1 = 1
cl2 = 4
cl3 = 9
cl4 = "-"
n = 0





def main(simulationMode):
    global repairmanBusy, queue, mc, cl1,cl2,cl3,cl4,n
    os.system('cls' if os.name=='nt' else 'clear')
    print("**MACHINE INTERFERENCE PROBLEM SIMULATION**\n\n")
    if(simulationMode == 2):
        print("MC: Master Clock\nCL1: Arrival Event Clock 1\nCL2: Arrival Event Clock 2\nCL3: Arrival Event Clock 3\nCL4: Deperature Event Clock 4\nR: Indicates if repairman is busy")
        print("-------------")
    while True:
        sleep(0.4    if mc != 0 else 0)
        if(mc in getSignificantValues()):
           if(simulationMode == 2):
             print(f"mc: {mc}\t\tcl1: {cl1}\t\tcl2: {cl2}\t\tcl3: {cl3}\t\tcl4: {cl4}\t\tn: {n}\t\tr: {'busy' if repairmanBusy == True else 'idle'}".upper())

        mc+=1 # increment the master clock
       

       
        
       #initial arrival event clocks
        if(mc == cl1):
            machineBreaksDown(1,simulationMode)
        elif(mc == cl2):
            machineBreaksDown(2,simulationMode)
        elif(mc == cl3):
            machineBreaksDown(3,simulationMode)



def machineBreaksDown(machineID, simulationMode):
    global repairmanBusy, queue, mc, cl1,cl2,cl3,cl4,n

    print(f"A machine breaks down at time {mc}\n" if simulationMode == 1 else "", end = "")
    #increment n
    n += 1
    print(f"n = n + 1\n" if simulationMode == 1 else "", end = "")

    if(mc == cl1):
        cl1 = "-"
    elif(mc == cl2):
        cl2 = "-"
    elif(mc == cl3):
        cl3 = "-"


    print(f"(?) Repairman is busy?\n" if simulationMode == 1 else "", end = "")
    if (repairmanBusy):
        queue.append(machineID)
        print(f"YES. Repairman is busy, join the queue\n" if simulationMode == 1 else "", end = "")
        #print(f"Queue: {queue}")
    else:
        print(f"NO. Repairman is IDLE\n" if simulationMode == 1 else "", end = "")
        repairmanBusy = True
        print(f"Repairman becomes busy\n" if simulationMode == 1 else "", end = "")
        cl4 = mc + const_repairTime
        Thread(target=startRepair, args=(machineID,simulationMode,)).start()


def startRepair(machineID,simulationMode):
    global repairmanBusy, queue, mc, cl1,cl2,cl3,cl4,n
    print(f"Repair starts\n" if simulationMode == 1 else "", end = "")
    
    while(True):
        sleep(0.01)
        if(cl4 == mc):
            repairComplete(machineID,simulationMode)
            break

    


def repairComplete(machineID,simulationMode):
    global repairmanBusy, queue, mc, cl1,cl2,cl3,cl4,n
    print(f"A machine is repaired at time {mc}\n" if simulationMode == 1 else "", end = "")
    n -= 1
    print(f"n = n - 1\n" if simulationMode == 1 else "", end = "")

    if(machineID == 1):
        cl1 = mc + const_operationalTime
    elif(machineID == 2):
        cl2 = mc + const_operationalTime
    elif(machineID == 3):
        cl3 = mc + const_operationalTime

    print(f"(?) Another machine waits on the queue?\n" if simulationMode == 1 else "", end = "")
    if(n > 0): #if another machine waits on the queue
        #print(f"Queue is not empty. Next machine (no: {queue[0]}) in the queue will be repaired now.")
        print(f"YES. Another machine waits on the queue\n" if simulationMode == 1 else "", end = "")
        #generate new service
        #startRepair(queue.pop(0))
        cl4 = mc + const_repairTime
        print(f"Generate new service\n" if simulationMode == 1 else "", end = "")
        Thread(target=startRepair, args=(queue.pop(0),simulationMode,)).start()
      

    else: #queue is empty
        repairmanBusy = False;
        print(f"NO. Queue is empty.\n" if simulationMode == 1 else "", end = "")
        print(f"Repairman is now IDLE\n" if simulationMode == 1 else "", end = "")




def getSignificantValues():
    CL_list = []
    if(cl1 != "-"):
        CL_list.append(cl1)
    if(cl2 != "-"):
        CL_list.append(cl2)
    if(cl3 != "-"):
        CL_list.append(cl3)
    if(cl4 != "-"):
        CL_list.append(cl4)

   

    significantValues.append(min(CL_list))
    return significantValues





def simulationModeSelection(question: str) -> int:
    reply = None
    errorCount = 0
    while reply not in ("1", "2"):
        if(reply != None):
            errorCount = errorCount + 1
            if(errorCount == 3):
                print("Too many incorrect inputs, running default mode (event output)")
                main(1)
            else:
                print("Error. Please input 1 or 2 and then press enter.")
        reply = input(f"{question} (1 or 2): ").lower()
    return reply



# I was planning to make two different programs to show the events and the timetable. But then I merged them in a single application. 
# When running, please input 1 or 2 to select the simulation output mode.
if __name__ == "__main__":

    print("**MACHINE INTERFERENCE PROBLEM SIMULATION**\n")
    print("Please select the simulation output\n--Enter 1 for printing events as they happen\n--Enter 2 for printing simulation time table with event occurance times")

    simulationMode = simulationModeSelection("Please type 1 or 2 on terminal and then press enter key to continue with the selection")

    if(simulationMode == "1"):
        main(1)
    else:
        main(2)
    
#main()
