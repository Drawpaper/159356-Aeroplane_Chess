import tkinter as tk
from  tkinter import messagebox

# log in
def login(bytes,users):
    # users= {'user1':'111111','user2':'222222','user3':'333333','user4':'444444'}

    window=tk.Tk()
    window.title('Aeroplane Chess Game - log in')
    window.geometry('500x500')
    tk.Label(window,text = 'Username:').place(x = 50,y = 100)
    tk.Label(window,text = 'Password:').place(x = 50,y = 170)
    rules_intro="This is an Aeroplane Chess Game !\n Yellow chess: press 【key0】 to get dice number\n Blue chess: press 【key1】 " \
                "to get dice number\n Red chess: press 【key2】 " \
                     "to get dice number\n Green chess: press 【key3】 to get dice number" # 显示所有可选择的棋子信息
    la= tk.Label(window, text= rules_intro).place(x=100,y=350)

    def usr_login():
        usr_name = var_usr_name.get()
        usr_pwd = var_usr_pwd.get()

        if usr_name in users and users[usr_name]==usr_pwd:
            if bytes['number']==1:
                chesscolor="【yellow】 chess"
                order="Already 1 players,continued...."
            elif bytes['number']==2:
                chesscolor="【blue】 chess"
                order="Already 2 players,continued...."
            elif bytes['number']==3:
                chesscolor="【red】 chess"
                order="Already 3 players,continued...."
            elif bytes['number']==4:
                chesscolor="【green】 chess"
                order="Already 4 players,continued...."

            tk.messagebox.showinfo(title = 'Welcome',message = ' Have a good time, ' + usr_name
                                                               + "\n You are the "+chesscolor + " !" +"\n"+ order)
            window.quit()
            window.destroy()
        else:
                tk.messagebox.showinfo(message = 'Error,your password is wrong,try again.')

    def usr_sign_up():
        def sign_to_Mofan_Python():

            np = new_pwd.get()

            np_confirm = new_pwd_confirm.get()

            nn = new_name.get()
            if nn in users:
                tk.messagebox.showerror('Error','The user has already signed up!')
            elif np!=np_confirm:
                tk.messagebox.showerror('Error','the confirm password is different! ')
            else:
                users[nn] = np
                tk.messagebox.showinfo(message ='sign up successfully ! log in now!')
                window_sign_up.destroy()
        window_sign_up = tk.Toplevel(window)
        window_sign_up.geometry('350x200')
        window_sign_up.title('Sign up window')

        new_name = tk.StringVar()
        tk.Label(window_sign_up,text = 'Username:').place(x = 10,y = 10)
        entry_new_name = tk.Entry(window_sign_up,textvariable = new_name)
        entry_new_name.place(x = 150,y = 10)

        new_pwd = tk.StringVar()
        tk.Label(window_sign_up,text = 'Password:').place(x = 10,y = 50)
        entry_new_pwd = tk.Entry(window_sign_up,textvariable = new_pwd,show = '*')
        entry_new_pwd.place(x = 150,y = 50)

        new_pwd_confirm = tk.StringVar()
        tk.Label(window_sign_up,text = 'Confirm password:').place(x = 10,y = 90)
        entry_comfirm_sign_up = tk.Entry(window_sign_up,textvariable = new_pwd_confirm,show = '*')
        entry_comfirm_sign_up.place(x = 150,y = 90)

        btn_comfirm_sign_up = tk.Button(window_sign_up,text = 'Sign up',command = sign_to_Mofan_Python)
        btn_comfirm_sign_up.place(x = 150,y = 130)

    var_usr_name = tk.StringVar()
    # input
    var_usr_pwd = tk.StringVar()
    entry_usr_name = tk.Entry(window,textvariable = var_usr_name)
    entry_usr_name.place(x = 160,y = 100)
    entry_usr_pwd = tk.Entry(window,textvariable = var_usr_pwd,show ='*')
    entry_usr_pwd.place(x = 160,y = 170)
    btn_login = tk.Button(window,text = ' Log in ',command = usr_login)
    btn_login.place(x = 170,y = 230)

    btn_sign_up = tk.Button(window,text = 'Sign up',command = usr_sign_up)
    btn_sign_up.place(x = 270,y = 230)

    window.mainloop()
    return users

