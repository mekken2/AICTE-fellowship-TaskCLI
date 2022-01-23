import sys

lst = sys.argv

if lst[0].casefold() == 'task.py' and len(lst) == 1 or lst[1].casefold() == 'help' and len(lst) > 1:
    usage = '''Usage :-
$ ./task add 2 "hello world"    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics'''
    sys.stdout.buffer.write(usage.encode('utf8'))

tasks_todo = []
tasks_complete = []

with open('task/task.txt') as file:
    for line in file:
        tasks_todo.append(line.rstrip())

max_pr = 0
for i in range(len(tasks_todo)):
    temp = []
    val = tasks_todo[i].split()
    temp.append(int(val[0]))
    if int(val[0]) > max_pr:
        max_pr = int(val[0])
    temp.append(' '.join(val[1:]))
    tasks_todo[i] = temp

# sys.stdout.buffer.write(tasks_todo.encode('utf8'))
# sys.stdout.buffer.write(max_pr.encode('utf8'))
priority_list = []
if len(lst) == 2:
    if lst[1].casefold() == 'add':
        sys.stdout.buffer.write(("Error: Missing tasks string. Nothing added!").encode('utf8'))
    if lst[1].casefold() == 'ls':
        k = 1
        for i in range(max_pr+1):
            for j in tasks_todo:
                if i == j[0]:
                    priority_list.append(j)
                    P1 = str(k)+". "+j[1]+" ["+str(j[0])+"]"+"\n"
                    sys.stdout.buffer.write(P1.encode('utf8'))
                    k += 1
        tasks_todo = priority_list

if len(lst) == 4:
    if lst[1].casefold() == 'add':
        temp_add = lst[3]
        temp_do = True
        for k in range(len(tasks_todo)):
            if tasks_todo[k][1] == temp_add:
                temp_do = False
                tasks_todo[k][0] = lst[2]
        if temp_do:
            with open('task/task.txt','a') as file:
                L = lst[2]+" "+lst[3]+"\n"
                file.writelines(L)
                T = [int(lst[2]),lst[3]]
                tasks_todo.append(T)
            with open('task/task.txt','w') as file:
                    for i in tasks_todo:
                        file.writelines(str(i[0])+" "+str(i[1])+"\n")

        if len(tasks_todo) > 1:
            P2 = "Added task: \""+lst[3]+"\" with priority "+str(lst[2])
        else:
            P2 = "Added task: \""+lst[3]+"\""
        sys.stdout.buffer.write(P2.encode('utf8'))

if len(lst) == 3:
    if lst[1].casefold() == 'del':
        if int(lst[2]) > len(tasks_todo) or int(lst[2]) == 0:
            sys.stdout.buffer.write(("Error: task with index #"+str(lst[2])+" does not exist. Nothing deleted.").encode('utf8'))
        else:
            tasks_todo.pop(int(lst[2])-1)
            with open('task/task.txt','w') as file:
                for i in tasks_todo:
                    file.writelines(str(i[0])+" "+str(i[1])+"\n")
            sys.stdout.buffer.write(("Deleted task #"+str(lst[2])).encode('utf8'))
        
if len(lst) == 3:
    if lst[1].casefold() == 'done':
        if int(lst[2]) > len(tasks_todo):
            sys.stdout.buffer.write(("Error: no incomplete item with index "+str(lst[2])+" exists.").encode('utf8'))
        else:
            #sys.stdout.buffer.write(tasks_todo.encode('utf8'))
            with open('task/completed.txt','a') as file:
                file.write(str(tasks_todo[int(lst[2])-1][0])+" "+str(tasks_todo[int(lst[2])-1][1])+"\n")
            sys.stdout.buffer.write(("Marked item as done.").encode('utf8'))
            tasks_todo.pop(int(lst[2])-1)
            with open('task/task.txt','w') as file:
                for i in tasks_todo:
                    file.writelines(str(i[0])+" "+str(i[1])+"\n")
            #sys.stdout.buffer.write("Deleted item with index "+str(lst[2]).encode('utf8'))

if len(lst) == 2:
    if lst[1].casefold() == 'report':
        sys.stdout.buffer.write(("Pending: "+str(len(tasks_todo))+"\n").encode('utf8'))
        for i in range(len(tasks_todo)):
            sys.stdout.buffer.write((str(i+1)+". "+tasks_todo[i][1]+" ["+str(tasks_todo[i][0])+"]\n").encode('utf8'))

        with open('task/completed.txt') as file:
            
            for line in file:
                tasks_complete.append(line.rstrip())

            for i in range(len(tasks_complete)):
                temp = []
                val = tasks_complete[i].split()
                temp.append(int(val[0]))
                if int(val[0]) > max_pr:
                    max_pr = int(val[0])
                temp.append(' '.join(val[1:]))
                tasks_complete[i] = temp

        sys.stdout.buffer.write(("Completed: "+str(len(tasks_complete))+"\n").encode('utf8'))
        for i in range(len(tasks_complete)):
            sys.stdout.buffer.write((str(i+1)+". "+tasks_complete[i][1]+" ["+str(tasks_complete[i][0])+"]\n").encode('utf8'))

if len(lst) > 4:
    sys.stdout.buffer.write(("Invalid Input, Please run \"help\" command for further info.").encode('utf8'))

