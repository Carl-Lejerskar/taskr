#!/usr/bin/python
import sys  #to parse args passed 
import pickle #for persistent storage 
from datetime import date
import os


def getTasks():
    '''
    Input: No input
    Output: tasks object (a dictionary)
    '''
    if os.path.isfile('./tasks.pk'):       #if tasks.pk already exists 
        with open('tasks.pk', 'rb') as f:
            tasks = pickle.load(f)
    else:                                  #tasks is just a dict 
        tasks = {}
    return tasks


def getDate():                         #get the current date
    '''
    Input: No input
    Output: Today's date (a datetime object)
    '''
    return date.today() 

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

def listTasks():
    '''
    Input: No input. 
    Output: No output. Prints the lists of tasks for today.
    '''
    if not tasks:                       #handles a tasks with no keys
        return
    i = 1 
    if date not in tasks.keys():        #check for tasks
       print('There are no tasks for today!')

    for specific_task in tasks[date]:
        print(str(i) + '.' + ' ' + specific_task + '\n')
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
        print(str(tasks_completed) + ' task completed, ' + str(tasks_left) + ' left.')
