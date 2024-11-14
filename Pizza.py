def givePizzaContents(pizza):
    contents = []
    for i in range(0,len(pizza.toppings)):
        contents.append(pizza.toppings[i].type)
    contents = sorted(contents)
    return contents

def buildPizza(myOptions,name):
    toppingsToAdd = []
    notDone = True
    while notDone:
        toppingToAdd = input("Enter topping name to add to pizza, otherwise enter 1 to create\n")
        if (toppingToAdd != "1"):
            toppingsToAdd.append(Topping(toppingToAdd))
        else:
            notDone = False
    newPizza = Pizza(toppingsToAdd,myOptions,name)
    return newPizza
    






class Topping:
    def __init__(self,type):
        self.type = type
    
 
class toppingOptions:
    def __init__(self,items):
        self.items = items

    def addItem(self,item):
        itemAlreadyExists = False
        for i in range(0,len(self.items)):
            if (item.type == self.items[i].type):
                itemAlreadyExists = True
        
        if (itemAlreadyExists == False):    
            self.items.append(item)
    
    def deleteItem(self,itemName):
        for i in range(0,len(self.items)):
            if (itemName == self.items[i].type):
                del self.items[i]
                break
    def upDateItem(self,itemName,newItemName):
        for i in range(0,len(self.items)):
            if (self.items[i].type == itemName):
               self.items[i].type = newItemName
                
        
    def giveAllItems(self):
        for i in range(0,len(self.items)):
            print(self.items[i].type)

        


class Pizza:
    def __init__(self,toppings,choices,pizzaName):
        self.toppings = toppings
        self.choices = choices
        self.pizzaName = pizzaName
    
    def addTopping(self,toppingName):
        for i in range(0,len(self.choices.items)):
            #check if new topping is an option
            if (self.choices.items[i].type == toppingName):
                # check if new topping is already on pizza
                toppingUsed = False
                for j in range(0,len(self.toppings)):
                    if(self.toppings[j].type == toppingName):
                        toppingUsed = True
                        break
                        
                if (not toppingUsed):
                    self.toppings.append(Topping(self.choices.items[i].type))
    
    
    def deleteTopping(self,toppingName):
        for i in range(0,len(self.toppings)):
            if(self.toppings[i].type == toppingName):
                del self.toppings[i]
                break


   
   
    def giveAllToppings(self):
        for i in range(0,len(self.toppings)):
            print(self.toppings[i].type)


class PizzaInventory:
    def __init__(self,pizzas):
        self.pizzas = pizzas
    def addPizza(self,newPizza):
        pizzaInInventory = False
        for i in range(0,len(self.pizzas)):
            #CHECK IF PIZZA TO ADD IS ALREADY AN OPTION
            if givePizzaContents(self.pizzas[i]) == givePizzaContents(newPizza):
                pizzaInInventory = True
                break
        if not pizzaInInventory:
            self.pizzas.append(newPizza)

    def deletePizza(self,nameToDelete):
        for i in range(0,len(self.pizzas)):
            if self.pizzas[i].pizzaName == nameToDelete:
                del self.pizzas[i]
                break

    def addToppingToExistingPizza(self,newPizzaName,newToppingName):
        for i in range(0,len(self.pizzas)):
            if (self.pizzas[i].pizzaName == newPizzaName):
                self.pizzas[i].addTopping(newToppingName)

    def updateToppingsOnAnExistingPizza(self,myOptions,name):
        for i in range(0,len(self.pizzas)):
            if (self.pizzas[i].pizzaName == name):
                self.pizzas[i] = buildPizza(myOptions,name)
                break
    def updateAnExistingPizza(self,oldName,newName):
        for i in range(0,len(self.pizzas)):
            if (self.pizzas[i].pizzaName == oldName):
                self.pizzas[i].pizzaName = newName  
                break 
        
    

        









    def giveAllPizzas(self):
        pizzaContents = ""
        for i in range(0,len(self.pizzas)):
            print(self.pizzas[i].pizzaName, end="")
            print(givePizzaContents(self.pizzas[i]))






        



myOptions = toppingOptions([])
myPizza = Pizza([],myOptions,"test_pizza")
myInventory = PizzaInventory([])




notAnswered = True
while notAnswered:
    role = input("Are you an owner or a chef? \n")
    if role == "owner" or role == "chef":
        notAnswered = False

while 1:
    if (role == "owner"):
        nextAction = input("Do you want to \n 1). Add topping\n 2). Delete topping \n 3). Update existing topping \n 4). See current toppings\n 5). Switch role\n")
        if (nextAction == "1"):
            newTopping = input("What is the name of the topping you would like to add?\n")
            myOptions.addItem(Topping(newTopping))
        elif (nextAction == "2"):
            targetedTopping = input("What is the name of the topping you would like to delete?\n")
            myOptions.deleteItem(targetedTopping)
        elif (nextAction == "3"):
            oldTopping = input("What is the name of the topping you would like to update?\n")
            newTopping = input("What would you like to change it too?\n")
            myOptions.upDateItem(oldTopping,newTopping)
        elif (nextAction == "4"):
            print("\n")
            myOptions.giveAllItems()
            input("enter any character to continue...\n")
        elif (nextAction == "5"):
            role = "chef"
    elif(role == "chef"):
        nextAction = input("Do you want to \n 1). Create a new pizza \n 2). Add Topping to Pizza \n 3). delete an existing pizza \n 4). update an existing pizza \n 5). update toppings on an existing pizza \n 6). See all pizzas \n 7). change role \n") 
        if (nextAction == "1"):
            name = input("what would you like to name the pizza?\n")
            newPizza = buildPizza(myOptions,name)
            myInventory.addPizza(newPizza)
        elif (nextAction == "2"):
            nameOfPizza = input("what pizza would you like to add to?")        
            newToppingToAdd =   input("what is the name of the topping you want to add?")
            myInventory.addToppingToExistingPizza(nameOfPizza,newToppingToAdd)
        elif (nextAction == "3"):
            done = False
            while(not done):
                nametoDelete = input("Enter name of Pizza to delete. If done enter 1")
                if (nametoDelete != "1"):
                    myInventory.deletePizza(nametoDelete)
                else:
                    done = True

        elif (nextAction == "4"):
            oldName = input("what is the name of the pizza you want to update")
            newName = input("what new name would you like to give it?")
            myInventory.updateAnExistingPizza(oldName,newName)
        elif (nextAction == "5"):
            name = input("what is the name of the pizza that you want to update")
            myInventory.updateToppingsOnAnExistingPizza(myOptions,name)
        elif (nextAction == "6"):
            myInventory.giveAllPizzas()

        elif (nextAction == "7"):
            role = "owner"


            
