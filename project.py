
accounts=dict()# to make the dictionary variable global
def isclosed(account_num):
        if accounts[account_num][1]=='c':     # to check if the account is closed 
         print('The account is closed')       # by accessing the dict using the key(account_num) to check if it is c or a
         return True
     
def isfound(account_num):
    if account_num in accounts:     # check if the key(account_num) is in the system(the dictionary accounts)
        return True  
def dictionary():
  try:
    customer_file2=open('customer.txt','r')
    global accounts
    accounts={}
    for line in customer_file2:                     # we took the info from the file and wrote in dictionary
        account_num=int(line.split(',')[0])
        name=line.split(',')[1]
        status=line.split(',')[2]                         
        account_balance=float(line.rstrip('\n').split(',')[3])
        accounts[account_num]=[name,status,account_balance]
    customer_file2.close()
  except FileNotFoundError:   #in case no file we get an empty dictionary
     accounts=dict()       
def open_account():
    try:
     account_num=int(input('Enter account number:'))   
    except ValueError: # making sure its an integer
        print('Account number must be an integer')
    else:
     if not isfound(account_num):
        account_name=input('Enter customer name:')
        accounts[account_num]=[account_name,'a',0.00]
     else:
        print('Account number already exists')
        
def close_account():
    try:
     account_num=int(input('Enter account number:'))
    except ValueError:
        print('Account number must be an integer') #exception so the program does not stop if wrong value was inserted
    else:
     if isfound(account_num):
        if accounts[account_num][2]!=0:
            print('The account has a balance, cannot be closed')
        elif isclosed(account_num):
            return
        else:  
            accounts[account_num][1]='c'
     else:
        print('There is no account with this number')
        return
def withdraw():
    tran_file=open('transaction.txt','a')
    
    try:
        account_num=int(input('Enter account number:'))
    except ValueError:
        print('Account number must be an integer')
    else:
        if isfound(account_num):
            if isclosed(account_num):
                return
            else:
                try:
                    amount=float(f'{float(input("Enter amount to withdraw:")):.2f}') # I need the amount to be formatted for 2 decimals                                           
                except ValueError:                                                   # so i formatted the input then switched the string back to float
                    print('Amount must be a number')
                else:
                    
                    if amount<0:
                        print('you must enter positive number to withdraw')
                    elif amount>accounts[account_num][2]:# incase  there was no enough balance to withdraw from
                          print('insufficient fund')
                    else:
                        
                          accounts[account_num][2]-=amount
                        
                          tran_file.write(f'{account_num},w,{amount:2f}\n')
                          tran_file.close()
        else:
            print('There is no account with this number')
            return
def deposit():
    tran_file=open('transaction.txt','a')
    try:
        account_num=int(input('Enter account number:'))
    except ValueError:
        print('Account number must be an integer')
    else:
        if isfound(account_num):
            account_name=accounts[account_num][0]
            print(account_name)
            if isclosed(account_num):
                return
            else:
                try:
                    amount=float(f'{float(input("Enter amount to deposit:")):.2f}')
                except ValueError:
                    print('Amount must be a number')
                else:
                    if amount<=0:
                        print('You must enter a positive number')
                        return
                    accounts[account_num][2]+=amount
                    tran_file.write(f'{account_num},d,{amount:.2f}\n')
                    tran_file.close()                  
        else:
            print('There is no account with this number')
            return
def inquiry():
    try:
        account_num=int(input('Enter account number:'))
    except ValueError:
        print('Account number must be an integer')
    else:
        if isfound(account_num):
            account_name=accounts[account_num][0]
            status=accounts[account_num][1]
            if status=='a':
                status='Active'
            else:
                status='Closed'
            balance=accounts[account_num][2]
            print('Name: ',account_name)
            print('Status: ',status)
            print(f'Balance: {balance:.2f}')
        else:
            print('There is no account with this number')
            return
def transactions():
    account_num=int(input('Enter account number:'))
    if isfound(account_num):
        account_name=accounts[account_num][0]
        print('Name: ',account_name)
        try:
                tran_file=open('transaction.txt','r')
        except FileNotFoundError:
                print('There is no transactions file')
        else:
            lines= tran_file.readlines()# getting the lines as a list
            c=0
            for i in range(len(lines)-1,-1,-1): # I made the range goes backward so I can use the value of i to read a value from the last 5 lines
                num=int(lines[i].split(',')[0])  
                type=lines[i].split(',')[1]
                
                amount=float(lines[i].rstrip('\n').split(',')[2])
                if num==account_num:
                    print(type,amount,sep=' ')
                    c+=1
                if c==5:
                    tran_file.close()
                    break
            tran_file.close()
def top_accounts():
    balance_lst=[]# a list that has the balance values only
    for value in accounts.values():
        balance_lst.append(value[2])
    balance_lst.sort() # we sort and then reverse it so it starts from the highest balance
    balance_lst.reverse()   
    count=0# counter to know when to stop
    for i in range(len(balance_lst)-1):
            for key in accounts:
                if accounts[key][2]==balance_lst[i]:
                    name=accounts[key][0]
                    balance=accounts[key][2]
                    print(key,name,balance,sep=' ' )
                    count+=1
                    if count==5:
                        return
def save_to_file(accounts): # a function to write the dictionary (accounts) in customer.txt only when the user exit the program
    customer_file=open('customer.txt','w')
    for key,value in accounts.items():
        customer_file.write(str(key)+','+value[0]+','+value[1]+','+str(value[2])+'\n')
    customer_file.close()
def main():
    dictionary()
    while True:
        print('please select one of the following')
        list_choices=[ '1- Open Account' ,'2- Close Account' ,'3- Withdraw' ,'4- Deposit','5- Inquiry' ,'6- Transactions','7- Top Accounts','8- Exit']
        for option in list_choices:
            print(option)
        choice=(input('Enter your choice:'))
        if choice=='1':
            open_account()
        elif choice=='2':
            close_account()
        elif choice=='3':
            withdraw()
        elif choice=='4':
            deposit()
        elif choice=='5':
            inquiry()
        elif choice=='6':
            transactions()
        elif choice=='7':
            top_accounts()
        elif choice=='8':
            save_to_file(accounts)# saving the updates in customer.txt
            break
        else:
            print('Invalid choice')
main()