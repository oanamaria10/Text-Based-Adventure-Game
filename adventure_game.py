#functia care citeste din fisier si memoreaza datele intr-un dictionar
def load_file(file_name):
  file=file_name
  f=open(file, "r") #deschidere pt read
  d={} #initializare dictionar vid
  ok=0
  start=[]
  final_states=[]
  for line in f:
      line=line.strip() #scoatem \n
      if line[0]!="#": #ignoram comentariile
            if line not in d and ok==0:
                  d[line]=[]
                  value=line
                  ok+=1
            else:
                  if line == "End": #ajungem la capat de sectiune
                        ok=0 #reluam cu ok=0 pt urm sectiune
                  else:
                        if len(line.split(','))==3:
                              s1, s2, s3 = line.split(',')
                              if s2=='S':
                                d[value].append(s1)
                                start.append(s1)
                                final_states.append(s1)
                              elif s2=='F':
                                state1,f,st=line.split(',')
                                d[value].append(s1)
                                start.append(s1)
                                final_states.append(s1)
                              else:
                                s=[s1,s3,s2]
                                d[value].append(s)
                        elif len(line.split(','))==2:
                                state,s=line.split(',')
                                if s== 'S':
                                    start.append(state)
                                elif s== 'F':
                                    final_states.append(state)
                                d[value].append(state)
                        elif len(line.split(',')) == 6:
                            state1, input, symbol1, state2, symbol2, symbol3 = line.split(',')
                            s = [state1, input, symbol1, state2, symbol2, symbol3]
                            d[value].append(s)
                        elif line.endswith('.'): #pentru descrieri
                            room,description=line.split(':')
                            r=[room,description]
                            d[value].append(r)
                        else:
                            d[value].append(line)
  f.close() #inchidere fisier
  return (d,start,final_states)
res=load_file("LA_ex3.in")
def add_epsilon(d):
    d['Symbols:'].append('e') # adaugam simbolul care nu face nimic
    return d

def LA (command,current_room, d, final_states,inventory): #functia recursiva care verifica daca cuvantul este valid
    #daca jucatorul a ajuns la final
    if current_room in final_states:
        print("Congratulations! You discover the Secret Exit!")
        return
    #daca jucatorul a renuntat
    elif command[0]=="quit":
        print("Maybe next time it'll be better!")
        return
    else:
        #parcurgem tranzitiile in functie de comanda
        # comanda go <room>
        if command[0]=='go':
            for k in range(0, len(d['Transitions:'])):
                if command[0]==d['Transitions:'][k][1] and current_room==d['Transitions:'][k][0]:#cautam tranzitia pentru camera curenta si camera in care vrem sa ajungem
                    if command[1]==d['Transitions:'][k][3]:  #verificam daca jucatorul poate ajunge in camera dorita
                        if d['Transitions:'][k][2]!='e' and d['Transitions:'][k][2] in inventory: #verificam daca jucatorul are obiectul necesar pentru a intra in camera dorita
                              print(f"Congratulations! You enter in {command[1]}!")
                              current_room=command[1] #modificam current room cu cea in care a intrat jucatorul
                              command = input("Please enter a command:").split(maxsplit=1) #citim urmatoarea comanda
                              return LA(command, current_room, d, final_states, inventory) #continuam jocul
                        elif d['Transitions:'][k][2]=='e' and command[1]=="Dining Room": #pentru Dining Room nu are nevoie de un obiect specific
                              print(f"Congratulations! You enter in {command[1]}!")
                              current_room=command[1] #modificam current room cu cea in care a intrat jucatorul
                              command = input("Please enter a command:").split(maxsplit=1) #citim urmatoarea comanda
                              return LA(command, current_room, d, final_states, inventory) #continuam jocul
                        else: #jucatorul nu are obiectul necesar
                            print("Sorry! You don't have the specific item to enter in this room.")
                            # current room nu se modifica
                            command = input("Please enter a command:").split(maxsplit=1)  # citim urmatoarea comanda
                            return LA(command, current_room, d, final_states, inventory)
                            break
            else: #pentru comanda de go, daca iesim din for inseamna ca nu puteam ajunge din camera curenta in cea dorita de jucator
                print(f"Sorry! You can't go in this room from {current_room}.")
                # current room nu se modifica
                command = input("Please enter a command:").split(maxsplit=1)  # citim urmatoarea comanda
                return LA(command, current_room, d, final_states, inventory)  # continuam jocul
        # comanda de look
        elif command[0] == "look":
            for k in range(0, len(d['Transitions:'])):
                #cautam descrierea specifica pentru current_room
                if d['Transitions:'][k][0]==current_room:
                    for i in range(0, len(d['Descriptions:'])):
                        if d['Descriptions:'][i][0]==d['Transitions:'][k][0]:
                            print(d['Descriptions:'][i][1])
                            break
                    #current room nu se modifica
                    command = input("Please enter a command:").split(maxsplit=1) #citim urmatoarea comanda
                    return LA(command, current_room, d, final_states, inventory)
        # comanda de take<item>
        elif command[0] == "take":
            # un obiect poate fi lasat in camera in urma unei comenzi de drop, de aceea vom lua verifica functiile de drop pentru a vedea daca a fost lasat vreun obiect
            for i in range(0, len(d['Transitions:'])):  # cautam daca in camera curenta s-a dat drop la obiect
                if d['Transitions:'][i][1] == 'drop' and command[1] in d['Transitions:'][i][4] and d['Transitions:'][i][0] == current_room:
                    if command[1] not in inventory:
                        # am gasit un obiect in urma unei comenzi de drop
                        inventory.append(command[1])
                        print(f"The {command[1]} was added!")
                        # eliminam din tranzitia de drop obiectul care a fost luat din camera curenta
                        d['Transitions:'][i][4].remove(command[1])  # eliminam obiectul din camera
                        if d['Transitions:'][i][4]==[]:
                            d['Transitions:'][i][4] =''.join('e') # modificam in tranzitii cu e(nu mai avem obiecte straine in camera)
                    elif command[1] in inventory:
                        print(f"You already have {command[1]} in your inventory")
                        break
            for k in range(0, len(d['Transitions:'])):
                if command[0]==d['Transitions:'][k][1] and d['Transitions:'][k][0]==current_room:
                    #verificam ca obiectul sa fie in current_room pentru a-l putea adauga in inventar
                    if command[1]==d['Transitions:'][k][2]: #obiectul se afla in camera
                        if command[1] not in inventory and d['Transitions:'][k][5]!='e': ##fara duplicate
                            inventory.append(d['Transitions:'][k][5])
                            print(f"The {command[1]} was added!")
                            break
                        elif command[1] in inventory:
                            print(f"You already have {command[1]} in inventory")
                            break
            else: #am iesit din for, nu am gasit obiectul
                print(f"Sorry! The {command[1]} is not available in this room!")
            #current room nu se modifica
            command = input("Please enter a command:").split(maxsplit=1)  # citim urmatoarea comanda
            return LA(command, current_room, d, final_states, inventory)
        #comanda de drop<item>
        elif command[0]=="drop":
            if len(inventory)==0:
                print("Your inventory is empty!")
            else:
                for k in range(0, len(d['Transitions:'])):
                    #cand dam drop unui obiect, jucatorul se poate afla intr-o camera in care nu se gaseste obiectul respectiv, de aceea vom trata acest caz
                    if command[0]==d['Transitions:'][k][1] and d['Transitions:'][k][0] == current_room:#stergem obiectul din camera curenta
                        if command[1] in inventory and command[1]==d['Transitions:'][k][2]: #suntem in camera in care se gasea obiectul in initial setup, nu ii mai dam drop in camera pentru ca oricum il vom gasi
                            inventory.remove(command[1])
                            print(f"We drop the {command[1]} from inventory.")
                            break
                        elif command[1] in inventory and command[1] not in d['Transitions:'][k][4]: ## stergem daca obiectul este in inventar si nu i-am dat deja drop
                            if(d['Transitions:'][k][4]=='e'): #actualizam tranzitia de drop
                                d['Transitions:'][k][4]=[command[1]]
                            else:
                                d['Transitions:'][k][4].append(command[1])
                            inventory.remove(command[1])
                            print(f"We drop the {command[1]} from inventory.")
                            break
                        else:
                            print(f"We couldn't find the {command[1]} in your inventory.")
                            break
            #current room nu se modifica
            command = input("Please enter a command:").split(maxsplit=1)  # citim urmatoarea comanda
            return LA(command, current_room, d, final_states, inventory)
        #comanda inventory
        elif command[0]=='inventory':
            if len(inventory)==0:
                print("Your inventory is empty!")
            else:
                print("Your inventory contains: ",end="")
                for i in range(len(inventory)-1):
                    print(inventory[i],end=", ")
                print(*inventory[len(inventory)-1:],".",sep='')
            # current room nu se modifica
            command = input("Please enter a command:").split(maxsplit=1)  # citim urmatoarea comanda
            return LA(command, current_room, d, final_states, inventory)
    print("Your command is invalid! Please give a proper command!")
    #current room nu se modifica
    command = input("Please enter a command:").split(maxsplit=1)  # citim urmatoarea comanda
    return LA(command, current_room, d, final_states, inventory)

#pornim jocul
d=res[0]
current_state=res[1] #reprezinta camera din care incepem jocul
current_state=current_state[0]
final_states=res[2] #reprezinta camera in care trebuie sa ajunga jucatorul pentru a castiga
d=add_epsilon(d)
"""
D contine:
-Sigma: comenzile jocului
-States: camerele prin care merge jucatorul
-Symbols: obiectele
-Transitions: functiile de tranzitie asociate fiecarei comenzi
-Descriptions: descrierile camerelor+camerele in care jucatorul poate intra din camera curenta
"""
inventory=[]
#descrierea jocului
print("Hello! In this adventure game, you play the role of an adventurer trapped in the mystifying ”Castle of Illusions”. Each room within the castle contains unique challenges and rewards. Your ultimate goal is to discover the secret exit that leads to the outside world. However, navigating through the castle isn’t as easy as it may seem - certain rooms are accessible only if you possess specific items.")
print('''Here are the commands that you can use to interact with the game world:
• go [room name]: Moves the player to the specified room if it is adjacent and the necessary conditions (e.g. having a certain item) are met.
• look: Provides a description of the current room and the adjacent rooms.
• inventory: Shows the items currently in the player’s possession.
• take [item]: Allows the player to pick up an item found in a room.
• drop [item]: Allows the player to drop an item from their inventory into the current room''')
print("Your adventure start from Entrance Hall! Good luck!")
print('Whenever you want to quit, please enter "quit".')
command=input("Enter your first command:")
if command=="quit": #jucatorul a renuntat
    print("Maybe next time it'll be better!")
else:
    command=command.split(maxsplit=1)
    LA(command,current_state,d,final_states,inventory)


