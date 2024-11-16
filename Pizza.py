from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)


#returns topping names of a pizza in a list

def givePizzaContents(pizza):
    contents = []
    for i in range(0,len(pizza.toppings)):
        contents.append(pizza.toppings[i].type)
    contents = sorted(contents)
    return contents


toppingsToAdd = []

nextName = ""

#defines toppings with name "type" for the name of the topping

class Topping:
    def __init__(self, type):
        self.type = type
    def __repr__(self):
        return self.type


# holds all usable toppings
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
        holder = []
        for i in range(0,len(self.items)):
            holder.append(self.items[i].type)
        return holder
            




# hold a list of unique toppings, name, and possible toppings

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
        holder = []
        for i in range(0,len(self.toppings)):
            holder.append(self.toppings[i].type)
        return holder




#contains all existing pizzas

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

    def updateToppingsOnAnExistingPizza(self,myOptions,name,toppingsToUse):
        for i in range(0,len(self.pizzas)):
            if (self.pizzas[i].pizzaName == name):
                #go to new function
                self.pizzas[i] = Pizza(toppingsToUse,myOptions,name)
                break
    def updateAnExistingPizza(self,oldName,newName):
        for i in range(0,len(self.pizzas)):
            if (self.pizzas[i].pizzaName == oldName):
                self.pizzas[i].pizzaName = newName  
                break 
        
    
    

    def giveAllPizzas(self):
        pizzaContents = ""
        for i in range(0,len(self.pizzas)):
            pizzaContents += self.pizzas[i].pizzaName +":"+"-".join(map(str, givePizzaContents(self.pizzas[i]))) + ", "
        return pizzaContents




#conatiners for possible toppings and existing pizzas

myOptions = toppingOptions([])
myInventory = PizzaInventory([])





# home page that determines role
@app.route('/')
def index():
    return '''
    <h1>Are you an owner or a chef?</h1>
    <form method="POST" action="/select_role">
        <input type="text" name="role">
        <button type="submit">Submit</button>
    </form>
'''

# role directing logic
@app.route('/select_role', methods=['GET', 'POST'])
def select_role():
    role = request.form.get('role').lower()
    if role == "owner":
        return redirect(url_for('owner_page'))
    elif role == "chef":
        return redirect(url_for('chef_page'))
    else:
        return redirect(url_for('index'))




# page to determine what action for owner to perform 
@app.route('/owner', methods=['GET', 'POST'])
def owner_page():
    return '''
    <h1>Do you want to \n 1). Add topping\n 2). Delete topping \n 3). Update existing topping \n 4). See current toppings\n 5). Switch role<br></h1>"</h1>
    <form method="POST" action="/select_owner_action">
        <input type="text" name="action">
        <button type="submit">Submit</button>
    </form>
'''



#  logic to direct to owner choice
@app.route('/select_owner_action', methods=['GET', 'POST'])
def select_owner_action():
    action = request.form.get('action')
    if action == "1":
        return redirect(url_for('add_topping_page'))
    elif action =="2":
        return redirect(url_for('delete_topping_page'))
    elif action =="3":
        return redirect(url_for('update_existing_topping_page'))
    elif action =="4":
        return redirect(url_for('see_current_toppings_page'))
    elif action =="5":
        return redirect(url_for('chef_page'))    



# gets topping to be added
@app.route('/add_topping', methods=['GET', 'POST'])
def add_topping_page():
    
    return f'''
    <h1>What is the name of the topping you would like to add?"</h1>
    <form method="POST" action="/add_topping_action">
        <input type="text" name="newTopping">
        <button type="submit">Submit</button>
    </form>
'''



# performs topping add logic
@app.route('/add_topping_action', methods=['GET', 'POST'])
def add_topping_action_page():
    newTopping = request.form.get('newTopping')
    myOptions.addItem(Topping(newTopping))
    return redirect(url_for('owner_page'))
    
    
    











# gets name of topping to delete
@app.route('/delete_topping', methods=['GET', 'POST'])
def delete_topping_page():

    


    
    return '''
    <h1>What is the name of the topping you would like to delete?</h1>
    <form method="POST" action="/delete_topping_action">
        <input type="text" name="targetedTopping">
        <button type="submit">Submit</button>
    </form>
'''



# performs topping delete logic
@app.route('/delete_topping_action', methods=['GET', 'POST'])
def delete_topping_action_page():

    targetedTopping = request.form.get('targetedTopping')
    myOptions.deleteItem(targetedTopping)



    return redirect(url_for('owner_page'))











# gets name of topping to be changed
@app.route('/update_existing_topping', methods=['GET', 'POST'])
def update_existing_topping_page():




    
    return '''
    <h1>"What is the name of the topping you would like to update?</h1>
    <form method="POST" action="/update_existing_topping_two">
        <input type="text" name="oldTopping">
        <button type="submit">Submit</button>
    </form>
'''




# gets new topping name
@app.route('/update_existing_topping_two', methods=['GET', 'POST'])
def update_existing_topping_two_page():

    
    oldTopping = request.form.get('oldTopping')

    return f'''
    <h1>What would you like to change "{oldTopping}" to?</h1>
    <form method="POST" action="/update_existing_topping_three">
        <input type="hidden" name="oldTopping" value="{oldTopping}">
        <input type="text" name="newTopping">
        <button type="submit">Submit</button>
    </form>
    '''




# performs topping change logic
@app.route('/update_existing_topping_three', methods=['GET', 'POST'])
def update_existing_topping_three_page():

    oldTopping = request.form.get('oldTopping')
    newTopping = request.form.get('newTopping')
    
    myOptions.upDateItem(oldTopping,newTopping)
    return redirect(url_for('owner_page')) 





























# displays all current topping options
@app.route('/see_current_toppings', methods=['GET', 'POST'])
def see_current_toppings_page():
    
    holder = myOptions.giveAllItems()  
    holder = ", ".join(holder) 
    
    return f'''
    <h1>{holder}</h1>
    <form method="POST" action="/owner">
        <input type="text" name="action">
        <button type="submit">Submit</button>
    </form>
'''





    















































# asks chef what option they want to perform
@app.route('/chef',methods=['GET', 'POST'])
def chef_page():
    return '''
    <h1>Do you want to \n 1). Create a new pizza \n 2). Add Topping to Pizza \n 3). delete an existing pizza \n 4). update an existing pizza \n 5). update toppings on an existing pizza \n 6). See all pizzas \n 7). change role \n<br></h1>"</h1>
    <form method="POST" action="/chef_choice">
        <input type="text" name="action">
        <button type="submit">Submit</button>
    </form>
'''




# logic to direct chef choice to next option 
@app.route('/chef_choice', methods=['GET', 'POST'])
def chef_choice_page():
    action = request.form.get('action')
    if action == "1":
        return redirect(url_for('create_a_new_pizza_page'))
    elif action =="2":
        return redirect(url_for('add_topping_to_Pizza_page'))
    elif action =="3":
        return redirect(url_for('delete_an_existing_pizza_page'))
    elif action =="4":
        return redirect(url_for('update_existing_pizza_page'))
    elif action =="5":
        return redirect(url_for('update_toppings_on_an_existing_pizza_page'))
    elif action =="6":
        return redirect(url_for('see_all_pizzas_page'))
    elif action =="7":
        return redirect(url_for('owner_page')) 






# gets name of pizza to be created
@app.route('/create_a_new_pizza', methods=['GET', 'POST'])
def create_a_new_pizza_page():

    
    
    
    return '''
    <h1>what would you like to name the pizza?</h1>
    <form method="POST" action="/create_a_new_name">
        <input type="text" name="newName">

        <button type="submit">Submit</button>
    </form>
'''


# assigns pizza name to global variable
@app.route('/create_a_new_name', methods=['GET', 'POST'])
def create_a_new_pizza_name_page():
    
    global nextName
    newName = request.form.get('newName')

    nextName = newName
    
    return redirect(url_for('create_a_new_pizza_two_page'))







# gets name of a topping to added in the creation of a new pizza
@app.route('/create_a_new_pizza_two', methods=['GET', 'POST'])
def create_a_new_pizza_two_page():
    
     

    
    
    return f'''
    <h1>Enter topping name to add to pizza, otherwise enter 1 to create</h1>
    
    <form method="POST" action="/create_a_new_pizza_three">
        <input type="text" name="toppingToAdd">
        <button type="submit">Submit</button>
    </form>
'''




# performs recusive logic to create pizza; loops back to "create_a_new_pizza_two_page()" until all toppings added
@app.route('/create_a_new_pizza_three', methods=['GET', 'POST'])
def create_a_new_pizza_three_page():
    global toppingsToAdd
    global nextName

    
    toppingToAdd = request.form.get('toppingToAdd')

    if(toppingToAdd == "1"):
        newPizza = Pizza(toppingsToAdd,myOptions,nextName)
        myInventory.addPizza(newPizza)
        toppingsToAdd = []
        nextName = ""
        return redirect(url_for('chef_page'))
    
    else:
        toppingsToAdd.append(Topping(toppingToAdd))
        return redirect(url_for('create_a_new_pizza_two_page'))
    
        
    
    
    










# PGet name of pizza that topping will be added to 
@app.route('/add_topping_to_Pizza', methods=['GET', 'POST'])
def add_topping_to_Pizza_page():

   

    return '''
    <h1>what pizza would you like to add to?</h1>
    <form method="POST" action="/add_topping_to_Pizza_two">
        <input type="text" name="nameOfPizza">
        <button type="submit">Submit</button>
    </form>
'''




# Gets name of topping to be added to pizza
@app.route('/add_topping_to_Pizza_two', methods=['GET', 'POST'])
def add_topping_to_Pizza_two_page():

    nameOfPizza = request.form.get('nameOfPizza')

    return f'''
    <h1>what is the name of the topping you want to add to {nameOfPizza}</h1>
    <form method="POST" action="/add_topping_to_Pizza_three">
        <input type="hidden" name="nameOfPizza" value="{nameOfPizza}">
        <input type="text" name="newToppingToAdd">
        <button type="submit">Submit</button>
    </form>
'''


# Performs logic to add topping to existing pizza
@app.route('/add_topping_to_Pizza_three', methods=['GET', 'POST'])
def add_topping_to_Pizza_three_page():

    newToppingToAdd = request.form.get('newToppingToAdd')
    nameOfPizza = request.form.get('nameOfPizza')
    
    myInventory.addToppingToExistingPizza(nameOfPizza,newToppingToAdd)


    return f'''
    <h1>{newToppingToAdd} added to {nameOfPizza}</h1>
    <form method="POST" action="/chef">
        <input type="text" name="nameOfPizza">
        <button type="submit">Submit</button>
    </form>
'''







# Gets name of pizza that will be deleted
@app.route('/delete_an_existing_pizza', methods=['GET', 'POST'])
def delete_an_existing_pizza_page():
    return '''
    <h1>Enter name of Pizza to delete.</h1>
    <form method="POST" action="/delete_an_existing_pizza_two">
        <input type="text" name="nametoDelete">
        <button type="submit">Submit</button>
    </form>
'''


# perfomrs logic to delete given pizza
@app.route('/delete_an_existing_pizza_two', methods=['GET', 'POST'])
def delete_an_existing_pizza_two_page():


    nametoDelete = request.form.get('nametoDelete')
    myInventory.deletePizza(nametoDelete)


    
    return redirect(url_for('chef_page'))













      
# Gets name of pizza that will be updated
@app.route('/update_existing_pizza', methods=['GET', 'POST'])
def update_existing_pizza_page():


    return '''
    <h1>what is the name of the pizza you want to update</h1>
    <form method="POST" action="/update_existing_pizza_two">
        <input type="text" name="oldName">
        <button type="submit">Submit</button>
    </form>
'''


# gets new name to give to pizza that will be updated
@app.route('/update_existing_pizza_two', methods=['GET', 'POST'])
def update_existing_pizza_two_page():

    oldName = request.form.get('oldName')
    return f'''
    <h1>what new name would you like to give it? {oldName}</h1>
    <form method="POST" action="/update_existing_pizza_three">
    <input type="hidden" name="oldName" value="{oldName}">
        <input type="text" name="newName">
        <button type="submit">Submit</button>
    </form>
'''


# performs logic to update pizza name
@app.route('/update_existing_pizza_three', methods=['GET', 'POST'])
def update_existing_pizza_three_page():

    oldName = request.form.get('oldName')
    newName = request.form.get('newName')
    myInventory.updateAnExistingPizza(oldName,newName)
     
    return redirect(url_for('chef_page'))

    return f'''
    <h1>{oldName} is now {newName}</h1>
    <form method="POST" action="/update_existing_pizza_two">
        <input type="text" name="oldName">
        <button type="submit">Submit</button>
    </form>
'''







newNameToGive = ""
toppingsToAddBeAdded = []
# Gets name of pizza to be updated
@app.route('/update_toppings_on_an_existing_pizza', methods=['GET', 'POST'])
def update_toppings_on_an_existing_pizza_page():
    return '''
    <h1>what is the name of the pizza that you want to update</h1>
    <form method="POST" action="/update_toppings_on_an_existing_pizza_name">
        <input type="text" name="name">
        <button type="submit">Submit</button>
    </form>
'''




# stores name of pizza to be updated in a global variable
@app.route('/update_toppings_on_an_existing_pizza_name', methods=['GET', 'POST'])
def update_toppings_on_an_existing_pizza_name_page():
    global newNameToGive
    name = request.form.get('name')
    
    newNameToGive = name
    
  
    return redirect(url_for('update_toppings_on_an_existing_pizza_two_page'))
    




# Gets name of topping to be included in updated pizza
@app.route('/update_toppings_on_an_existing_pizza_two', methods=['GET', 'POST'])
def update_toppings_on_an_existing_pizza_two_page():
    
    
  
    

    return f'''
    <h1>Enter topping name to include in updated pizza, otherwise enter 1 to create </h1>
 
    <form method="POST" action="/update_toppings_on_an_existing_pizza_three">
        <input type="text" name="toppingToBeAdded">
        <button type="submit">Submit</button>
    </form>
'''

# performs recusive logic to updated pizza. contiues looping back to "update_toppings_on_an_existing_pizza_two()" until all toppings recived, then updates pizza 
@app.route('/update_toppings_on_an_existing_pizza_three', methods=['GET', 'POST'])
def update_toppings_on_an_existing_pizza_three_page():
    
    global toppingsToAddBeAdded
    global newNameToGive

    toppingToBeAdded = request.form.get('toppingToBeAdded')


    if(toppingToBeAdded == "1"):
              
        myInventory.updateToppingsOnAnExistingPizza(myOptions,newNameToGive,toppingsToAddBeAdded)
        toppingsToAddBeAdded = []
        newNameToGive = ""
        return redirect(url_for('chef_page'))
    
    else:
        toppingsToAddBeAdded.append(Topping(toppingToBeAdded))
        return redirect(url_for('update_toppings_on_an_existing_pizza_two_page'))
    
        
    
    
    





# displays all exisiting pizzas


@app.route('/see_all_pizzas', methods=['GET', 'POST'])
def see_all_pizzas_page():
    holderx = ""
    for pizza in myInventory.pizzas:
        holderx += pizza.pizzaName + ": "
        toppings_list = [topping.type for topping in pizza.toppings]
        holderx += ", ".join(toppings_list) + " | "
    
    return f'''
    <h1>{holderx}</h1>
    <form method="POST" action="/chef">
        <input type="text">
        <button type="submit">Submit</button>
    </form>
'''






"""

if __name__ == '__main__':
    app.run(debug=True)
"""
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)
