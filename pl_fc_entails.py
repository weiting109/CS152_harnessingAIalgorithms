'''
Includes classes for propositional logic: Symbol, DefiniteClause
Implements front chaining entailment algorithm described in Section 7.5 of Russell, S. J., & Norvig, P. (2016). Artificial intelligence: a modern approach (3rd ed.). Boston: Pearson.
'''

from collections import deque

class Symbol:
    #data structure for logical symbol

    def __init__(self,symbol,proposition=None):
        self.symbol = symbol #char symbol is the symbol chosen
        self.proposition = proposition #string descriptor for symbol (optional)
        self.inferred = False #boolean val, used for front chaining, False by default

    def inferTrue(self):
        self.inferred = True

class DefiniteClause:
    #data structure for a definite clause
    #symbols assigned True in premise are removed from premise

    def __init__(self,body,head):
        self.body = body #list body contains Symbol objects of literals in premise/body
        self.head = head #Symbol head is the Symbol object of literal in conclusion/head
        self.cnt = len(self.body) #number of literals in premise yet to be assigned True

    def updatecnt(self):
        '''update cnt variable after passing facts through premises'''
        self.cnt = len(self.body)
        return self.cnt

    def print(self):
        '''prints definite clause in English'''
        for l in self.body: print(l.symbol,"AND ",end = '')
        print("implies",self.head.symbol)

def pl_fc_entails(KB,q):
    '''pl_fc_entails uses forward chaining on definite clauses (propositional logic) in
    list KB to determine if they entail Symbol object q, the query

    returns True if clauses in KB entail q, False otherwise'''

    #queue agenda contains literals that are given or inferred to be True
    #yet to be matched with literals in bodies of sentences in KB
    agenda = deque([])

    #adding given facts to agenda
    for s in KB:
        if type(s) == Symbol: agenda.append(s)
    #print(f"agenda: {[s.symbol for s in agenda]}")

    while agenda:
        p = agenda.pop()
        #print("Now at symbol: ",p.symbol)

        #if a fact matches a query, KB entails q
        if p.symbol == q.symbol: return True

        if p.inferred == False:
            #assign symbols in agenda to True
            p.inferTrue()
            #print("just set",p.symbol,"to",p.inferred)

            #look for premises that contain symbol p
            for s in KB:

                #skip facts/single literals
                if type(s) == Symbol: break

                '''
                print("looking at") #premise being examined
                s.print()
                '''

                present = 1 #used in case of repeated symbols in a single premise
                while present:
                    try:
                        id = s.body.index(p) #obtain index of symbol p in premise
                        s.body.pop(id) #remove symbol in premise
                    except ValueError: #if symbol p is not found
                        present = 0 #set present to 0 to terminate searching for p

                '''
                print("UPDATE:") #updated premise after removing symbol p in premise
                s.print()
                '''

                #if no. of literals in premise left unmatched with facts in KB is 0, premise is true
                #by Modus Ponens, conclusion is true
                if s.updatecnt() == 0:
                    agenda.append(s.head) #add conclusion to agenda
                    KB.append(s.head) #add conclusion to KB as a fact

    return False #query could not be proved with KB

#EXAMPLE in Section 7.5.3 of Russell, S. J., & Norvig, P. (2016). Artificial intelligence: a modern approach (3rd ed.). Boston: Pearson.

L = Symbol('L',"loc in 1,1")
B = Symbol('B',"breeze")
V = Symbol('V',"breeze in 1,1")
s1 = DefiniteClause ([L,B],V)

print(pl_fc_entails([s1,L,B],V))
