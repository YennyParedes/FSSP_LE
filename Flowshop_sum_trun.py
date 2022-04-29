"""
Flow shop sum truncated
"""

from pyomo.environ import *
from pyomo.environ import value
import os
import time

def FS_sum_trun(dic,alfa,beta):
    

    os.environ['NEOS_EMAIL'] = 'yennypaas@unisabana.edu.do'

    model = AbstractModel()
    
    num_machines = 2
    num_jobs = 7
    
    model.I = RangeSet( num_machines ) #Set() #machines
    model.J = RangeSet( num_jobs)      #Set() #trabajos
    model.R = RangeSet( num_jobs)      #Set()
     #positions
    
    model.p = dic
    model.alfa = alfa
    model.beta = beta
    model.BM =Param()
    
    model.x = Var(model.J,model.R, within=Binary)
    model.c = Var(model.I, model.R, within=NonNegativeReals)
    model.b = Var(model.I,model.R,within=NonNegativeReals)
    model.s = Var(model.I,model.R,within=NonNegativeReals)
    model.cl = Var(model.I,model.R,within=NonNegativeReals)
    model.sl = Var(model.I,model.R,within=NonNegativeReals)
    model.vl = Var(model.I,model.R,within=NonNegativeReals)
    model.Cmax = Var(within=NonNegativeReals)
    
    def Ofunction(model):
        return model.Cmax
    model.obj = Objective(rule = Ofunction,sense=minimize)
    
    def R_1(model,j):
            return sum(model.x[j,r] for r in model.R)==1
    model.Rest_1 = Constraint(model.J, rule=R_1)
    
    def R_2(model,r):
            return sum(model.x[j,r] for j in model.J)==1
    model.Rest_2 = Constraint(model.R, rule=R_2)
    
    def R_3(model,i,r):
        if i == 1:  
            return model.c[i,r]>=model.b[i,r]
        else:
            return Constraint.Skip
    model.Rest_3 = Constraint(model.I,model.R, rule=R_3)
    
    def R_4(model,i,r):
        if i > 1: 
            return model.c[i,r]-model.b[i,r]>=model.c[i-1,r]
        else:
            return Constraint.Skip
    model.Rest_4 = Constraint(model.I,model.R, rule=R_4)
    
    def R_5(model,i,j,h,r):
        if j!=h and r< len(model.R):     
            return model.c[i,r+1]-model.b[i,r+1]+((1-model.x[j,r+1])*model.BM)>=model.c[i,r]-((1-model.x[h,r])*model.BM)
        else:    
            return Constraint.Skip
    model.Rest_5 = Constraint(model.I,model.J,model.J,model.R, rule=R_5)
    
    def R_6(model,i,r):
            return model.Cmax>=model.c[i,r]
    model.Rest_6 = Constraint(model.I,model.R, rule=R_6)
    
    def R_7(model,i,r):
            return model.c[i,r]== model.b[i,r]+model.s[i,r]
    model.Rest_7 = Constraint(model.I,model.J, rule=R_7)
    
    
    def R_9(model,i,r):
        if r == 1:
             return model.b[i,r]== sum(model.x[j,r]*model.p[i,j] for j in model.J)
        else:    
             return Constraint.Skip
    model.Rest_9 = Constraint(model.I,model.J, rule=R_9)
    
    def R_8(model,i,r):
        if r >= 2:
            return model.cl[i,r]==((1+ ((1/60)*(sum (model.b[i,q] for q in model.R if q<r))))**model.alfa)*sum(model.x[j,r]*model.p[i,j] for j in model.J)
        else:    
            return Constraint.Skip
    model.Rest_8 = Constraint(model.I,model.J, rule=R_8)
    
    def R_10(model,i,r):
        if r >= 2:
            return model.sl[i,r]==model.beta*sum(model.x[j,r]*model.p[i,j] for j in model.J)
        else:    
            return Constraint.Skip
    model.Rest_10 = Constraint(model.I,model.J, rule=R_10)
    
    def R_11(model,i,r):
        if r >= 2:
            return model.vl[i,r]>=model.sl[i,r]
        else:    
            return Constraint.Skip
    model.Rest_11 = Constraint(model.I,model.J, rule=R_11)
    
    def R_13(model,i,r):
        if r >= 2:
            return model.vl[i,r]>=model.cl[i,r]
        else:    
            return Constraint.Skip
    model.Rest_13 = Constraint(model.I,model.J, rule=R_13)
    
    def R_12(model,i,r):
        if r >= 2:
             return model.b[i,r]==model.vl[i,r]
        else:    
             return Constraint.Skip
    model.Rest_12 = Constraint(model.I,model.J, rule=R_12)
        
    instance = model.create_instance('FSS_2X5v2.dat')
    
    t_inicial = time.time()
    # solver = SolverManagerFactory('neos') # ipopt
    # results=solver.solve(instance, opt = 'minlp')#tee=True , 
    solver = SolverFactory('bonmin') # ipopt
    results=solver.solve(instance, tee=True)
    t_final = time.time()
    t_total = t_final - t_inicial
    
    # instance.b.pprint()
    # instance.x.pprint()
    # instance.c.pprint()
    # instance.s.pprint()
    # instance.Cmax.pprint()
    # instance.obj.pprint()
     

    if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
        
        #Almacenamiento de resultados
        secuencia = []
        for r in range(1,num_jobs+1): #recorres las posiciones
            for j in range(1,num_jobs+1): # recorres los trabajos
        
                if  value(instance.x[j,r]) == 1:
                    secuencia.append(j)     
        
        inf_final = ( value(instance.obj),secuencia,t_total)
    
    else:
        inf_final = (np.nan,np.nan,np.nan)
        
    return inf_final 
            
