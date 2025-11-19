import re
import os

def split_at_top_level(s, sep):
    if s.startswith("<") and s.endswith(">"):
        s_inner = s[1:-1].strip()
    else:
        s_inner = s.strip()
    depth = 0
    for i, c in enumerate(s_inner):
        if c == "<":
            depth += 1
        elif c == ">":
            depth -= 1
        elif c == sep and depth == 0:
            return s_inner[:i].strip(), s_inner[i+1:].strip()
    return None, None

class PropositionalCalculusProof:
    def __init__(self):
        self.theorems = []

    def addThm(self, thm): #FOR TESTING
        self.theorems.append(thm)

    def joining(self, x, y):
        if x in self.theorems and y in self.theorems:
            self.theorems.append(f"<{x}^{y}>")
        else:
            print("One or more strings are not theorems.")

    def separation(self, conjugate):
        if conjugate in self.theorems:

            left, right = split_at_top_level(conjugate, "^")
            if left and right:
                self.theorems.extend([left, right])
            else:
                print(f"{conjugate} is not of the form <P^Q>")

        else:
            print(f"{conjugate} is not a theorem.")

    def removeDoubleTilde(self,string):
        if "~~" not in string:
            print(f"No ~~ in {string}")
            return
        if string not in self.theorems:
            print(f"{string} is not a theorem.")
            return
        newstring = re.sub(r'~~', '', string)
        self.theorems.append(newstring)

    def addDoubleTilde(self,string,idx):
        if string not in self.theorems:
            return f"{string} is not a theorem."
        if abs(idx) > len(string)-1:
            return f"Index {idx} out of range."
        newstring = string[:idx] + '~~' + string[idx:]
        self.theorems.append(newstring)

    def detachment(self, x, implication):
        if x not in self.theorems:
            print(f"{x} is not a theorem.")
            return
        if implication not in self.theorems:
            print(f"{implication} is not a theorem.")
            return
        
        antecedent, consequent = split_at_top_level(implication, ")")
        if antecedent is None or consequent is None:
            print("Not of the form P and <P)Q>")
            return
        
        if x.startswith("<") and x.endswith(">"):
            x_inner = x[1:-1].strip()
        else:
            x_inner = x.strip()

        if antecedent.startswith("<") and antecedent.endswith(">"):
            a_inner = antecedent[1:-1].strip()
        else:
            a_inner = antecedent.strip()

        if x_inner == a_inner:
            self.theorems.append(consequent.strip())

        else:
            print("Not of the form P and <P)Q>")

        
    
    def contrapositive(self, string):
        if string not in self.theorems:
            print(f"{string} is not a theorem.")
            return

        if string.startswith("<~") and string.endswith(">"):
            inner = string[2:-1]
            antecedent, consequent = split_at_top_level(inner, ")")
            if antecedent and consequent and consequent.startswith("~"):
                q = consequent[1:].strip()
                newstring = f"<{q}){antecedent}>"
                self.theorems.append(newstring)
                return

        antecedent, consequent = split_at_top_level(string, ")")
        if antecedent and consequent:
            newstring = f"<~{consequent})~{antecedent}>"
            self.theorems.append(newstring)
        else:
            print(f"{string} is not of the form <P)Q>")
            
    def deMorgans(self, string):
        if string not in self.theorems:
            print(f"{string} is not a theorem.")
            return
        
        if string.startswith("~<") and string.endswith(">"):
            inner = string[2:-1]
            left, right = split_at_top_level(inner, "v")
            if left and right:
                newstring = f"<~{left}^~{right}>"
                self.theorems.append(newstring)
                return
        
        left, right = split_at_top_level(string, "^")
        if left and right:
            if left.startswith("~") and right.startswith("~"):
                p = left[1:].strip()
                q = right[1:].strip()
                newstring = f"~<{p}v{q}>"
                self.theorems.append(newstring)
            else:
                print(f"{string} is not of the form <~P^~Q> or ~<PvQ>")
        else:
            print(f"{string} is not a valid form. ")

    def switcheroo(self, string):
        if string not in self.theorems:
            print(f"{string} is not a theorem.")
            return
        if string.startswith("<") and string.endswith(">"):
            body = string[1:-1].strip()
            left, right = split_at_top_level(body, "v")
            if left is not None and right is not None:
                newstring = f"<~{left}){right}>"
                self.theorems.append(newstring)

        if string.startswith("<") and string.endswith(">"):
            body = string[1:-1].strip()
            left, right = split_at_top_level(body, ")")
            if left is not None and right is not None and left.startswith("~"):
                p = left[1:].strip()
                q = right
                newstring = f"<{p}v{q}>"
                self.theorems.append(newstring)
            
            
class Fantasy(PropositionalCalculusProof): # Fix double tilde logic, add rest of rules, add check for well-formedness

    def __init__(self, theorems=None):
        PropositionalCalculusProof.__init__(self)
        if theorems is not None:
            self.theorems = theorems[:]
        else:
            self.theorems = []
        self.result = None
        
        
        supposal = input("Enter 'q' to end fantasy.\n[\n")
        if supposal != "q":
            self.theorems.append(supposal)
            
            rule = ""
            while rule != "q":

                rule = input("Enter rule: ")

                if rule.lower() == "fantasy": #Recursively call openFantasy
                    fantasy_result = self.openFantasy(self.theorems)
                    if fantasy_result:
                        self.theorems.append(fantasy_result)
                        self.printproof()
                    
                
                elif rule.lower() == "addthm": #TESTING PURPOSES
                    thm = input("Type thm to make thm (TESTING)")
                    self.addThm(thm)
                    self.printproof()

                elif rule.lower() == "joining":
                    thms = input("Join which 2 theorems? (Separate w/ space)").split()
                    print("")
                    self.joining(thms[0], thms[1])
                    self.printproof()

                elif rule.lower() == "separation":
                    conjugate = input("Separate which theorem?")
                    print("")
                    self.separation(conjugate)
                    self.printproof()

                elif rule.lower() == "doubletilde":
                    add_or_remove = input("Add or remove? ")
                    if add_or_remove.lower() == "remove":
                        string = input("String to remove double tilde: ")
                        print("")
                        self.removeDoubleTilde(string)
                        self.printproof()
                    elif add_or_remove.lower() == "add":
                        string = input("String to add double tilde: ")
                        idx = int(input("Index to insert double tilde: "))
                        print("")
                        self.addDoubleTilde(string, idx)
                        self.printproof()

                elif rule.lower() == "detachment":
                    x = input("Enter the antecedent (P in '<P)Q>'): ")
                    implication = input("Enter the implication ('<P)Q>'): ")
                    print("")
                    self.detachment(x, implication)
                    self.printproof()

                elif rule.lower() == "contrapositive":
                    string = input("Which string to operate on? ")
                    print("")
                    self.contrapositive(string)
                    self.printproof()

                elif rule.lower() == "demorgans":
                    string = input("Which string to operate on? ")
                    print("")
                    self.deMorgans(string)
                    self.printproof()
                
                elif rule.lower() == "switcheroo":
                    string = input("Which string to operate on? ")
                    print("")
                    self.switcheroo(string)
                    self.printproof()
                    


            self.printproof()
            print("]")
            self.result = f"<{supposal}){self.theorems[-1]}>"
            print(self.result)


    @classmethod
    def openFantasy(cls, theorems=None):
        fantasy = cls(theorems)
        return getattr(fantasy, 'result', None)
    

    def printproof(self):
            
            print("\n[")
            for thm in self.theorems:
                print("   ",thm)
            

def isAxiom1(string):
    if string == "Aa:~(Sa=0)":
        return True
    else:
        return False
    
def isAxiom2(string):
    if string == "Aa:a+0=a":
        return True
    else:
        return False

def isAxiom3(string):
    if string == "Aa:Ab:a+Sb=S(a+b)":
        return True
    else:
        return False
    
def isAxiom4(string):
    if string == "Aa:a*0=0":
        return True
    else:
        return False
    
def isAxiom5(string):
    if string == "Aa:Ab:a*Sb=(a*b)+a":
        return True
    else:
        return False
    
def isAxiom(string):
    if isAxiom1(string) or isAxiom2(string) or isAxiom3(string) or isAxiom4(string) or isAxiom5(string):
        return True
    else:
        return False

def isValidProof(proof):
    pass

if __name__ == "__main__":
    i = Fantasy()

