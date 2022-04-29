"""
Main function
"""
# %%
#Librerias
from pyomo.opt import SolverStatus, TerminationCondition
import numpy as np
import pandas as pd
import os
import time
import pickle
from pyomo.environ import *
from pyomo.environ import value

from Flowshop_sencillo import FS_sen
from Flowshop_sum_trun import FS_sum_trun
from Flowshop_position import FS_pos
from Flowshop_position_trun import FS_pos_trun
from Flowshop_sum import FS_sum

# %%

#datos experimentales-generados
dic_2x10 = {}
dic_2x20 = {}
dic_2x50 = {}
dic_2x100 = {}
dic_2x7 = {}
dic_2x8 = {}
dic_3x100 = {}

semillas = [6,51,14,30,67,12,6,17,35,22,30,2,1000,309,31,9,81,99,40,11,601,514,
             101,302,151,409,201,700,512,477] 

for i in range(1,31):
    np.random.seed(semillas[i-1])
    dic_2x10[i] = np.random.randint(1,100,(2,10))
    dic_2x20[i] = np.random.randint(1,100,(2,20))
    dic_2x50[i] = np.random.randint(1,100,(2,50))
    dic_2x100[i] = np.random.randint(1,100,(2,100))
    dic_2x7[i] = np.random.randint(1,100,(2,7))
    dic_2x8[i] = np.random.randint(1,100,(2,8))
    dic_3x100[i] = np.random.randint(1,100,(3,100))
    
c_2x10 = open('dicc_2x10.pkl', 'wb')
pickle.dump(dic_2x10, c_2x10)
c_2x10.close()
    
c_2x20 = open('dicc_2x20.pkl', 'wb')
pickle.dump(dic_2x20, c_2x20)
c_2x20.close()    

c_2x50 = open('dicc_2x50.pkl', 'wb')
pickle.dump(dic_2x50, c_2x50)
c_2x50.close()  

c_2x100 = open('dicc_2x100.pkl', 'wb')
pickle.dump(dic_2x100, c_2x100)
c_2x100.close()   

c_3x100 = open('dicc_3x100.pkl', 'wb')
pickle.dump(dic_3x100, c_3x100)
c_3x100.close()   
# %%  

#df_completo = pd.DataFrame(columns=['Workers', 'Jobs' , 'Case', 'Replicate','Param_alfa' , 'Param_beta' , 'Makespan' , 'Sequence' , 'Time'])

# %%
#ciclo princupal de corridas
results_case1 = []
results_case2 = []
results_case3 = []
results_case4 = []
results_case5 = []


#for p in range(1,31):
for p in range(9,10):
    print('p:', p)

  
    d = {}
    dic_g = dic_2x7
    
    for i in range(1,dic_g[p].shape[0]+1):
        for j in range(1,dic_g[p].shape[1]+1):
            d[(i,j)] = dic_g[p][i-1,j-1]
            
    list_alfa = [-0.152,-0.322,-0.515]
    list_beta = [0.25,0.5,0.75] 
     
    #print('En caso 1') 
    #case_1 = FS_sen(dic = d)
    # results_case1.append([dic_g[p].shape[0],
    #                           dic_g[p].shape[1],
    #                           1,
    #                           p,
    #                           np.nan,
    #                           np.nan,
    #                           case_1[0],
    #                           case_1[1],
    #                           case_1[2]])
    
    for k in range(len(list_alfa)):
        print('  k:', k)
        # print('En caso 2')
        # case_2 = FS_pos(dic = d, alfa = list_alfa[k])
        # results_case2.append([dic_g[p].shape[0],
        #                       dic_g[p].shape[1],
        #                       2,
        #                       p,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        #                       list_alfa[k],
        #                       np.nan,
        #                       case_2[0],
        #                       case_2[1],
        #                       case_2[2]])
        print('En caso 3')        
        # case_3 = FS_sum(dic = d, alfa = list_alfa[k])
        # results_case3.append([dic_g[p].shape[0],
        #                       dic_g[p].shape[1],
        #                       3,
        #                       p,
        #                       list_alfa[k],
        #                       np.nan,
        #                       case_3[0],
        #                       case_3[1],
        #                       case_3[2]])
        
                
        for l in range(len(list_beta)):
            print('   l:', l)
        #     print('En caso 4')
        #     case_4 = FS_pos_trun(dic = d, alfa = list_alfa[k], beta = list_beta[l])
        #     results_case4.append([dic_g[p].shape[0],
        #                           dic_g[p].shape[1],
        #                           4,
        #                           p,
        #                           list_alfa[k],
        #                           list_beta[l],
        #                           case_4[0],
        #                           case_4[1],
        #                           case_4[2]])
        
            print('En caso 5')
            case_5 = FS_sum_trun(dic = d, alfa = list_alfa[k], beta = list_beta[l])
            results_case5.append([dic_g[p].shape[0],
                                  dic_g[p].shape[1],
                                  5,
                                  p,
                                  list_alfa[k],
                                  list_beta[l],
                                  case_5[0],
                                  case_5[1],
                                  case_5[2]])
            df_case_5 = pd.DataFrame(results_case5,columns=['Workers', 'Jobs' , 'Case', 'Replicate','Param_alfa' , 'Param_beta' , 'Makespan' , 'Sequence' , 'Time'])  
            df_case_5.to_csv("Case25_2x7", index = False)
        
                    

#df_case_1 = pd.DataFrame(results_case1,columns=['Workers', 'Jobs' , 'Case', 'Replicate','Param_alfa' , 'Param_beta' , 'Makespan' , 'Sequence' , 'Time'])              
#df_case_2 = pd.DataFrame(results_case2,columns=['Workers', 'Jobs' , 'Case', 'Replicate','Param_alfa' , 'Param_beta' , 'Makespan' , 'Sequence' , 'Time'])  
#df_case_3 = pd.DataFrame(results_case3,columns=['Workers', 'Jobs' , 'Case', 'Replicate','Param_alfa' , 'Param_beta' , 'Makespan' , 'Sequence' , 'Time'])  
#df_case_4 = pd.DataFrame(results_case4,columns=['Workers', 'Jobs' , 'Case', 'Replicate','Param_alfa' , 'Param_beta' , 'Makespan' , 'Sequence' , 'Time'])  


#df_case_1.to_csv("Case1_2x7", index = False)
#df_case_2.to_csv("Case2_2x5", index = False)
#df_case_3.to_csv("Case3_2x7", index = False)
#df_case_4.to_csv("Case4_2x10", index = False)

