# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 13:51:08 2023

@author: shubh
"""
import tkinter as tk
from tkinter import simpledialog
import openai
import cx_Oracle

proc_name=str(input("Please  procedure name: \n"))
que = str(input("\nPlease enter your query: \n"))
in_var= str(input("\nPlease enter i/p var name & where to use: \n"))
out_var= str(input("\nPlease enter o/p var name & where to use: \n"))


openai.api_key = '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'
completion = openai.Completion.create(
  model="text-davinci-003",
  prompt="create or replace with procedure name {} to {} where   \
          input variable {} & \
          output varaible {} ".format(proc_name,que,in_var,out_var),
  max_tokens=150,
  temperature=0
)
d=(completion.choices[0]['text'])
print(d)


# Establish a connection to the Oracle database
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
conn = cx_Oracle.connect(user='system', password='shubh123', dsn=dsn_tns)
# Execute a query and fetch the results
b=d.split(";") #sometime output repeats after ; hence using split and then its [0]th index at below line

query = (f'{b[0]}')
#query="select * from emp"
c=query.lower()
cursor = conn.cursor()

cursor.execute(query)

print("\n---------------------------------------")
print(f"| Procedure {proc_name} generated..    |")
print("---------------------------------------")

#------------------------------------------------------------------------------
''' ##########For Automatically create variable and print output.##########

ini=int(input("Enter input value: "))
out_var1 = ''

out_var_bind = cursor.var(cx_Oracle.STRING)
cursor.callproc(proc_name, [ini,out_var_bind])
print("ok")
out_var1 = out_var_bind.getvalue()

# Print the output
print(f"The output of {proc_name} is {out_var1}")
'''


#------------------------------------------------------------------------------

# Creating a tkinter window

root = tk.Tk()
root.title("Stored Procedures from ORACLE Database")

# Create a text widget to display the results
text = tk.Text(root)
text.pack()

# for Executing the query and display the results in the text widget
cursor = conn.cursor()
cursor.execute("SELECT object_name FROM user_objects WHERE object_type = 'PROCEDURE'")
for row in cursor:
    text.insert(tk.END, row[0] + "\n")



# Close the cursor and db connection
cursor.close()
conn.close()

# Start the Tkinter event loop
root.mainloop()
