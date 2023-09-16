import streamlit as st
import re
import numpy as np
from tkinter import VERTICAL
from streamlit_option_menu import option_menu
import time as tm

st.set_page_config(layout="wide")

with open("styles.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

heading = "<div class='title'>Page Replacement Algorithms</heading1>"
st.markdown(heading, unsafe_allow_html=True)
A = []
# 1 2 3 4 1 2 5 1 2 3 4 5 "A good string to compare the three algos"
try:
   bold_text="<style> h3{ color:black } </style><h3>Enter page Reference String below..</h3>"
   st.markdown(bold_text,unsafe_allow_html=True)
   numbers=st.text_input("")
   
#    numbers = st.text_input("Enter Page Reference String below..")
   def collect_numbers(x): return [int(round(float(i)))  for i in re.split("[^0-9.]", x) if i != ""]
   A = collect_numbers(numbers)

except ValueError:
   st.error("You have Entered Invalid Page reference string")



if(len(A) > 0):
   c1, c2, x3 = st.columns([4, 5, 7])
   with c1:
       st.markdown("Total number of frames : ")
   with c2:
       st.markdown("Select the total number of frames you want in RAM from drop down below")
       total_pages = st.selectbox('', [k for k in range(1, len(set(A))+1)])

line = "<hr class='line'>"
st.markdown(line, unsafe_allow_html=True)



def FIFO(A, n):
   beg_time = tm.time()
   Final_list_of_list_for_fifo = []
   Current_list = ["&emsp;"]*n
   current_pointer = 0
   no_of_pagehits = 0
   for k in A:
       if(k not in Current_list):
           Y = Current_list.copy()
           Y[current_pointer] = k
           Final_list_of_list_for_fifo.append(Y)
           current_pointer = (current_pointer+1) % n
           Current_list = Y.copy()
       else:
           Final_list_of_list_for_fifo.append(["&emsp;"]*n)
           no_of_pagehits += 1
   Final_list_of_list_for_fifo = np.transpose(Final_list_of_list_for_fifo)
   end = tm.time()
   page_faults=len(A)-no_of_pagehits
   return Final_list_of_list_for_fifo.tolist(), page_faults,end-beg_time
	

def LRU(A, n):
   beg_time = tm.time()
   final_list_of_list = []
   page_hits=0
   current_list = ["&emsp;"]*n
   current_pointer=0
   s=set()
   faults=0
   for element in A:
        if element not in current_list:
            faults=faults+1
            s.add(element)
            Y=current_list.copy()
            if len(s)<=n:  
               Y[len(s)-1]=element
               final_list_of_list.append(Y.copy()) 
               current_list=Y.copy()
            else:
               s1=set()
               for i in range(current_pointer-1,-1,-1):
                    s1.add(A[i])
                    if len(s1)==n:
                        Y[Y.index(A[i])]=element
                        break
            
               final_list_of_list.append(Y.copy())
               current_list=Y.copy()
        else:
           final_list_of_list.append(["&emsp;"]*n)
        
        current_pointer=current_pointer+1
       
   final_list_of_list = np.transpose(final_list_of_list)
   end = tm.time()
   return final_list_of_list.tolist(), faults,end-beg_time

def Optimal(A,n):
    beg=tm.time()
    final_list_of_list=[]
    current_pointer=0
    page_hits=0
    current_list=["&emsp;"]*n
    #1 2 3 4 1 2 5 1 2 3 4 5
    for element in A:
        Y=current_list.copy()
        if element not in Y:
            if current_pointer<n:
                Y[current_pointer]=element
            else:
                index_list=[]
                for k in Y:
                    if k not in A[current_pointer+1:]:
                        Y[Y.index(k)]=element
                        break
                    else:
                        index_list.append( (A[current_pointer+1:].index(k)))
                else:   
                    Y[Y.index(A[current_pointer+1:][max(index_list)])]=element
        
            final_list_of_list.append(Y)
        else:
            final_list_of_list.append(["&emsp;"]*n)
            page_hits=page_hits+1
        
        current_pointer=current_pointer+1
        current_list=Y.copy()

    end=tm.time()
    final_list_of_list=np.transpose(final_list_of_list)
    final_list_of_list=final_list_of_list.tolist()
    
    return final_list_of_list,len(A)-page_hits,end-beg

def Ans(A, final_list_of_list, n, page_faults):
   if(len(A) > 0):
       m = "<div class='Ans'>"
       for x in final_list_of_list:
           m += "<p>"
           m += "".join(["<code>"+str(y)+"</code>&emsp;" for y in x])
           m += "</p>"
       st.markdown(m+"</div>", unsafe_allow_html=True)
       
          
# -----------Main code starts here-----------

col1, col2 = st.columns([3, 9])
with col1:
   choice = option_menu("", ["FIFO", "LRU(Least Recently Used)",
                        "Optimal", "Compare all"], orientation=VERTICAL)
   if(len(A)>0):
       if choice == "FIFO":
           with col2:
               B, page_faults,Etime = FIFO(A, total_pages)
               UBtime = 0.000010004 * len(A)
               if(len(B)>0 and len(B[0])<=15):
                   Ans(A, B, total_pages, page_faults)
               else:
                   st.write("(To long to Show)")
               Etime,UBtime = "{:.8f} Seconds".format(Etime),"{:.8f} Seconds".format(UBtime)
               
               st.markdown("<h2>Page Faults : "+str(page_faults) + "</h2><br><h2>Elapsed Time : "+str(Etime) + "</h2>", unsafe_allow_html=True)
               st.markdown("<h2>Uppper Bound : "+str(UBtime)+"</h2>", unsafe_allow_html=True)

       elif choice == "LRU(Least Recently Used)":
           with col2:
               B, page_faults,Etime = LRU(A, total_pages)
               UBtime = 0.00000045786 * len(A) * len(A)
               if(len(B)>0 and len(B[0])<=15):
                   Ans(A, B, total_pages, page_faults)
               else:
                   st.write("(To long to Show)")
               Etime,UBtime = "{:.8f} Seconds".format(Etime),"{:.8f} Seconds".format(UBtime)
               
               st.markdown("<h2>Page Faults : "+str(page_faults) + "</h2><br><h2>Elapsed Time : "+str(Etime) + "</h2>", unsafe_allow_html=True)
               st.markdown("<h2>Uppper Bound : "+str(UBtime)+"</h2>", unsafe_allow_html=True)
       elif choice == "Optimal":
           with col2:
               B, page_faults,Etime = Optimal(A, total_pages)
               UBtime = 0.000000404119 * len(A) * len(A)
               if(len(B)>0 and len(B[0])<=15):
                   Ans(A, B, total_pages, page_faults)
               else:
                   st.write("(To long to Show)")
               Etime,UBtime = "{:.8f} Seconds".format(Etime),"{:.8f} Seconds".format(UBtime)
               
               st.markdown("<h2>Page Faults : "+str(page_faults) + "</h2><br><h2>Elapsed Time : "+str(Etime) + "</h2>", unsafe_allow_html=True)
               st.markdown("<h2>Uppper Bound : "+str(UBtime)+"</h2>", unsafe_allow_html=True)
       else:
           with col2:
               D = {"a": "LRU", }
               B, a,Etime1 = LRU(A, total_pages)
               B, b,Etime2 = FIFO(A, total_pages)
               B, c,Etime3 = Optimal(A, total_pages)
               Etime1,Etime2,Etime3 = ["{:.6f}".format(Etime1),"{:.6f}".format(Etime2),"{:.6f}".format(Etime3)]
               X = [[a,Etime1, "LRU"], [b,Etime2, "FIFO"], [c,Etime3, "Optimal"]]
               X.sort(key=lambda y: y[1])
               final = """<table align="center">
               <th>Algorithm</th>
               <th>Execution time(s)</th>
               <th>Total Page Fault</th>"""
               for k in X:
                   final += "<tr><td>" + str(k[2])+"</td><td>" + str(k[1])+"</td><td>"+str(k[0])+"</td></tr>"
               final += "</table>"
               st.markdown(final, unsafe_allow_html=True)
