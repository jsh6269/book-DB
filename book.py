from tkinter import *
from tkinter import ttk

# global bookLst
global mode
mode = "No"
root = Tk()
root.title("Book")
root.geometry("600x712+450+40")

def sort_lst(event):
    global mode
    r1 = listbox.identify("region", event.x, event.y)
    r2 = listbox.identify_column(event.x)
    if r1 == "heading":
        if r2 == "#1":
            init()
            mode = "No"
        if r2 == "#2":
            bookLst.sort()
            mode = "Title"
        if r2 == "#3":
            bookLst.sort(key=lambda x: x[1])
            mode = "Category"
        show_lst()
        root.update()


def re_sort():
    if mode == "No":
        pass
    elif mode == "Title":
        bookLst.sort()
    elif mode == "Category":
        bookLst.sort(key=lambda x: x[1])


def button_plus():
    def submit_add(e):
        title, category = e[0].get().strip(), e[1].get().strip()
        if title and category:
            with open("data.txt", "a", encoding="utf") as f:
                f.write(title + "\t" + category + "\n")
            init()
            re_sort()
            show_lst()
            top.destroy()
            top.grab_release()

    top = Toplevel(root)
    top.attributes('-topmost', True)
    top.focus()
    top.grab_set()
    top.geometry("300x145+600+180")
    top.title("Add")

    space = Label(top, font="-size 15")
    frame1 = Frame(top, pady=0)
    label1 = Label(frame1, text="Title:\t")
    entry1 = Entry(frame1)
    frame2 = Frame(top, pady=10)
    label2 = Label(frame2, text="Category:\t")
    entry2 = Entry(frame2)
    button = Button(top, text="submit", command=lambda e=[entry1, entry2]: submit_add(e), width=9)

    space.pack()
    frame1.pack()
    label1.pack(side=LEFT)
    entry1.pack()
    frame2.pack()
    label2.pack(side=LEFT)
    entry2.pack()
    button.pack(pady=6)


def button_minus():
    def delete():
        selected = listbox.item(focus)
        with open('data.txt', 'r', encoding="utf") as f:
            datas = f.readlines()

        if selected['values']:
            row = str(selected['values'][1]).strip() + "\t" + str(selected['values'][2]).strip() + '\n'
            idx = datas.index(row)

        with open('data.txt', 'w', encoding="utf") as f:
            for i in range(len(datas)):
                if i != idx:
                    f.write(datas[i])
        init()
        re_sort()
        show_lst()
        top.destroy()
        top.grab_release()

    focus = listbox.focus()
    print(root.focus_get())
    if not focus:
        return

    top = Toplevel(root)
    top.geometry("300x135+600+180")
    top.grab_set()
    top.attributes('-topmost', True)
    top.focus()
    top.title("Delete")

    space = Label(top, pady=3)
    label = Label(top, text="Are you sure you want to delete?", pady=8, font="-size 11")
    frame = Frame(top, pady=10)
    button1 = Button(frame, text="yes", command=delete, width=5)
    button2 = Button(frame, text="no", command=lambda: (top.destroy(), top.grab_release()), width=5)
    space.pack()
    label.pack()
    frame.pack()
    button1.pack(side=LEFT, padx=10)
    button2.pack(side=RIGHT, padx=10)


def button_edit():
    def submit_edit(e):
        title, category = e[0].get().strip(), e[1].get().strip()
        if title and category:
            with open('data.txt', 'r', encoding="utf") as f:
                raw = f.read()
            selected = listbox.item(focus)
            oldText = '\n' + str(selected['values'][1]).strip() + "\t" + str(selected['values'][2]).strip() + '\n'
            newText = '\n' + title + '\t' + category + '\n'
            raw = raw.replace(oldText, newText, 1)

            with open('data.txt', 'w', encoding="utf") as f:
                f.write(raw)

            init()
            re_sort()
            show_lst()
            top.destroy()
            top.grab_release()

    focus = listbox.focus()
    if not focus:
        return

    top = Toplevel(root)
    top.geometry("300x145+600+180")
    top.grab_set()
    top.attributes('-topmost', True)
    top.focus()
    top.title("Edit")

    space = Label(top, font="-size 15")
    frame1 = Frame(top, pady=0)
    label1 = Label(frame1, text="Title:\t")
    entry1 = Entry(frame1)
    entry1.insert(0, listbox.item(focus)['values'][1].strip())
    frame2 = Frame(top, pady=10)
    label2 = Label(frame2, text="Category:\t")
    entry2 = Entry(frame2)
    entry2.insert(0, listbox.item(focus)['values'][2].strip())
    button = Button(top, text="submit", command=lambda e=(entry1, entry2): submit_edit(e), width=9)

    space.pack()
    frame1.pack()
    label1.pack(side=LEFT)
    entry1.pack()
    frame2.pack()
    label2.pack(side=LEFT)
    entry2.pack()
    button.pack(pady=6)


def init():
    global bookLst
    with open("data.txt", "r", encoding="utf") as f:
        data = f.readlines()
        bookLst = [[item.split("\t")[0].strip(), item.split("\t")[1].strip().split(', ')] for item in data]


def bind():
    listbox.bind("<Button-1>", sort_lst)
    combobox.bind("<<ComboboxSelected>>", show_lst)


def show_lst(event=None):
    cnt = 1
    listbox.delete(*listbox.get_children())
    for i in range(len(bookLst)):
        if combobox.get() == "전체" or combobox.get() in bookLst[i][1]:
            listbox.insert("", "end", values=(cnt, bookLst[i][0], ', '.join(bookLst[i][1])))
            cnt += 1
    label.focus_force()


def get_category():
    with open('list.txt', 'r', encoding="utf") as f:
        return ['전체'] + [category.strip() for category in f.readlines()]


frame = Frame(root)
space1 = Label(root, font="-size 1", height=1, pady=0)
label = Label(frame, text="Book", width=30, pady=4, anchor=W, font=('Segoe UI', 16))
space2 = Label(root, font="-size 1", height=1, pady=0)
button1 = Button(frame, text="✎", width=2, height=1, padx=0, pady=0, command=button_edit, relief="ridge", bd=1)
button2 = Button(frame, text="-", width=2, height=1, padx=0, pady=0, command=button_minus, relief="ridge", bd=1)
button3 = Button(frame, text="+", width=2, height=1, padx=0, pady=0, command=button_plus, relief="ridge", bd=1)
combobox = ttk.Combobox(frame, values=get_category(), state="readonly", width=9)
combobox.current(0)
listbox = ttk.Treeview(root, column=("No", "Title", "Category"), height=30, show="headings")

s = ttk.Style()
s.theme_use("vista")
s.configure('Treeview.Heading', foreground='#000000', font=('Segoe UI', 8, "bold"))
# print(s.theme_names())

listbox.column("#1", width=50, anchor=CENTER)
listbox.heading("#1", text="No")
listbox.column("#2", width=350, anchor=W)
listbox.heading("#2", text="Title")
listbox.column("#3", width=120, anchor=CENTER)
listbox.heading("#3", text="Category")

init()
bind()
show_lst()

space1.pack(side=TOP, fill="x")
frame.pack()
label.pack(side=LEFT)
space2.pack()
button1.pack(side=RIGHT, anchor=S)
button2.pack(side=RIGHT, anchor=S)
button3.pack(side=RIGHT, anchor=S)
combobox.pack(side=RIGHT, anchor=S, padx=4)
listbox.pack()
root.mainloop()
