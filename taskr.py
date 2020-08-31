#!/usr/bin/python
import sys  #to parse args passed 
import pickle #for persistent storage 
from datetime import date
import os

def getDailyTasks():
    '''
    Input: No input
    Output: daily tasks object (a list)
    '''
    if os.path.isfile('./dailytasks.pk'):
        with open('dailytasks.pk', 'rb') as f:
            daily_tasks = pickle.load(f)
    else:
        daily_tasks = []
    return daily_tasks

def getTasks():
    '''
    Input: No input
    Output: tasks object (a dictionary)
    '''
     
    if os.path.isfile('./tasks.pk'):       #if tasks.pk already exists 
        with open('tasks.pk', 'rb') as f:
            tasks = pickle.load(f)
    else:                                  #otherwise initialize tasks as an empty dict
        tasks = {}
        tasks[date] = []

    if checkNewDay():                      #add daily tasks if it is a new day
        for task in daily_tasks:
            tasks[date].append(task)
        with open('tasks.pk', 'wb') as f:  #save the object
            pickle.dump(tasks, f)
 
    return tasks

def getDate():                         #get the current date
    '''
    Input: No input
    Output: Today's date (a datetime object)
    '''
    return date.today() 

def checkNewDay():
    '''
    Input: No input
    Output: True/False depending if date has changed
    '''
    if os.path.isfile('./stored_date.pk'):             #load the stored_date
        with open('stored_date.pk', 'rb') as f:
            stored_date = pickle.load(f)
    else:
        stored_date = getDate()                 
    if stored_date != date:                     #if the date has changed, save the new date and return true
        with open('stored_date.pk', 'wb') as f:
            pickle.dump(date, f)
        return True
    else:
        return False

def getProgress():
    '''
    Input: No input. 
    Output: progress (a dictionary)
    '''
    if os.path.isfile('./progress.pk'):
        with open('progress.pk', 'rb') as f:
            progress = pickle.load(f)
    else:
        progress = {}

    if date not in progress.keys():
        progress[date] = 0

    return progress
            
def push(task):                        #add a task to today's list
    '''
    Input: task (a string)
    Output: No output. Pushes task to list of tasks for today's date.
    '''
    if date in tasks.keys():           #add task to list of tasks if a list of tasks already exists
        tasks[date].append(task)
    else:
        tasks[date] = [task]            #add task as a list if no tasks exists for that date 
    with open('tasks.pk', 'wb') as f:       #save
        pickle.dump(tasks, f)

def addDailyTask(task):
    '''
    Input: task (a string)
    Output: No output. Pushes task to the list of daily tasks.
    '''
    daily_tasks.append(task)            #add task to the daily_tasks object
    tasks[date].append(task)            #also add task to the tasks object
    with open('dailytasks.pk', 'wb') as f:
        pickle.dump(daily_tasks, f)
    with open('tasks.pk', 'wb') as f:
        pickle.dump(tasks, f)

def listTasks():
    '''
    Input: No input. 
    Output: No output. Prints the lists of tasks for today.
    '''
    if not tasks:                       #handles a tasks with no keys
        return
    i = 1 
    if len(tasks[date]) == 0: 
       print('There are no tasks to complete!')

    for specific_task in tasks[date]:
        print(str(i) + '.' + ' ' + specific_task + '\n')
        i += 1

def listDailyTasks():
    '''
    Input: No input.
    Output: No output. Prints the list of daily tasks.
    '''
    i = 1
    for task in daily_tasks:
        print(str(i) + '. ' + task)
        i += 1

def finished(index):
    '''
    Input: The index of task completed (an int)
    Output: No output. Removes task from today's lists of tasks.
    '''
    del tasks[date][index - 1]          #subtract from one to get 0-based index of task
    progress[date] += 1                 #add one to the progress for today

    with open('tasks.pk', 'wb') as f:
        pickle.dump(tasks, f)

    with open('progress.pk', 'wb') as f:
        pickle.dump(progress, f)
   
if __name__ == "__main__":
    
    #Get the data we need into global scope
    daily_tasks = getDailyTasks()
    tasks = getTasks()
    date = getDate()
    progress = getProgress()


    if len(sys.argv) == 1: #if the user simply puts taskr
        print('taskr is a command line task tracking tool')

    elif sys.argv[1] == 'push':  #if the user is pushing a task
        push(sys.argv[2])

    elif sys.argv[1] == 'list':  #list the tasks
        listTasks()
   
    elif sys.argv[1] == 'finished':
        finished(int(sys.argv[2]))
    
    elif sys.argv[1] == 'progress':
        tasks_completed = progress[date]
        tasks_left = len(tasks[date]) 
        if tasks_left > 0 :
            print(str(tasks_completed) + ' task completed, ' + str(tasks_left) + ' left.')
        else:
            print('Good job, you finished all your tasks!')
    
    elif sys.argv[1] == 'add-daily-task':
        addDailyTask(sys.argv[2])
    
    elif sys.argv[1] == 'list-daily-tasks':
        listDailyTasks()
