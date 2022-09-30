import threading
from tkinter import *
from tkinter import ttk
from helper import Jobs,Export
from tkinter import messagebox
from tkinter import filedialog
import time

def msgbox_retry():
    messagebox.showerror("Done","Error fetching results! Retrying..")

RESUME_PATH = ""
def get_all_jobs(title,location,filtered_labels,filtered_companies):
    jobs = Jobs()
    jobs.direct()
    jobs.filter(title, location, filtered_labels, filtered_companies)
    all_jobs = jobs.get_jobs()
    jobs.close()
    f = open("data.log","r")
    log = f.read().split(" ")   
    print(log) 
    f.close()
    
    if log[-2].strip() != 'SUCCESS':
        threading.Thread(target=msgbox_retry,args=()).start()
        return get_all_jobs(title,location,filtered_labels,filtered_companies)
    return all_jobs

def export_jobs(resume_path,all_jobs):
    export = Export(resume_path)
    ats = export.get_ats_score(all_jobs)
    export.export(all_jobs, ats)

def search_jobs(title,location,filtered_labels,filtered_companies):
    top = Toplevel()
    progress = ttk.Progressbar(top, orient=HORIZONTAL, mode='determinate', length=300)
    Label(top, text="Fetching the jobs....").pack(padx=10, pady=5)
    progress.pack(padx=10, pady=5)
    progress.start()
    all_jobs = get_all_jobs(title, location, filtered_labels, filtered_companies)
    export_jobs(RESUME_PATH,all_jobs)
    messagebox.showinfo("Done","Processed "+str(len(all_jobs))+" Jobs")
    top.destroy()


def find_resume():
    global RESUME_PATH
    RESUME_PATH = filedialog.askopenfilename(filetypes=(("pdf files","*.pdf"),("all files","*.*")))
    resume_label.config(text = RESUME_PATH)
    
    
def search():
    print(title_textbox.get(),location_textbox.get(),companies_textarea.get('1.0','end'))
    title = title_textbox.get().strip()
    location = location_textbox.get()
    companies = companies_textarea.get('1.0','end').split(",")
    filtered_companies = []
    filtered_labels = []
    for company in companies:
        filtered_companies.append(company.strip())

    for i in range(6):
        if level_values[i].get() == 1:
            filtered_labels.append(levels[i])

    threading.Thread(target=search_jobs,args=(title,location,filtered_labels,filtered_companies)).start()

    print(title,location,filtered_labels,filtered_companies)

root = Tk()
root.title("Searchbox")

filter_frame = LabelFrame(root)

title_label = Label(filter_frame,text="Job Title:")
title_textbox = Entry(filter_frame)
title_label.grid(row=0,column=0)
title_textbox.grid(row=0,column=1)

location_label = Label(filter_frame,text="Location:")
location_textbox = Entry(filter_frame)
location_label.grid(row=1,column=0)
location_textbox.grid(row=1, column=1)

companies_label = Label(filter_frame,text="Companies:")
companies_textarea = Text(filter_frame,height=1,width=35)
companies_label.grid(row=2,column=0)
companies_textarea.grid(row=2, column=1)



level_frame = LabelFrame(root)
levels = ['internship','entry level','associate','mid_senior','director','executive']
Label(level_frame,text="Select your preferred roles").pack()
level_values = [IntVar() for i in range(6)]
levels_widget = []
levels_widget.append(Checkbutton(level_frame,text="Internship",variable=level_values[0]))
levels_widget.append(Checkbutton(level_frame,text="Entry Level",variable=level_values[1]))
levels_widget.append(Checkbutton(level_frame,text="Associate",variable=level_values[2]))
levels_widget.append(Checkbutton(level_frame,text="Mid Senior",variable=level_values[3]))
levels_widget.append(Checkbutton(level_frame,text="Director",variable=level_values[4]))
levels_widget.append(Checkbutton(level_frame,text="Executive",variable=level_values[5]))
for i in range(6):
    levels_widget[i].pack()

resume_frame = LabelFrame(root)
Label(resume_frame, text="Enter the filepath for your resume (pdf only)").pack(side=TOP)
resume_label = Label(resume_frame,text="")
search_resume_button = Button(resume_frame, text="search resume",command=find_resume)
search_resume_button.pack()
resume_label.pack(side=BOTTOM)

search_button = Button(root, text="Search Jobs",command = search,padx=10,pady=10)


filter_frame.pack()
level_frame.pack()
resume_frame.pack()
search_button.pack()

root.mainloop()