# IMPORTED MODULES
from sqlite3.dbapi2 import Row, connect
from tkinter import *
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt

# SQL CONNECTION TO THE DATABASE 
connection = sqlite3.connect('NY_INSPECTION_DATA.db')
cursor = connection.cursor()

class Application:
    """ A CLASS FOR THE DATA ANALYSIS / VISUALISATION TOOL"""

    def __init__(self, root, dset, names):
        self.dataset = dset
        self.header_names = names

        # TITLE FOR THE WINDOW 
        root.title("Data Analysis/Visualisation Tool")

        # STYLES FOR THE FRAMES 
        navBarStyle = ttk.Style()
        navBarStyle.configure('RFrame.TFrame', background='#ACDAF4')
        spreadsheetStyle = ttk.Style()
        spreadsheetStyle.configure('BFrame.TFrame', background='#90ADDE')
        treestyle = ttk.Style()
        treestyle.configure('Treeview', rowheight=20)

        # CREATING THE FRAMES AND SETTING DEFAULTS 
        navigationFrame = ttk.Frame(root)
        navigationFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        spreadSheetFrame = ttk.Frame(root, style="BFrame.TFrame")
        spreadSheetFrame.grid(column=0, row=1, sticky=N)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=6)
        treeframe = ttk.Frame(spreadSheetFrame)
        treeframe.pack(fill='both')

        # SEARCH BAR
        ttk.Label(navigationFrame, text="Search:").grid(column=0, row=0, sticky=E, padx=(50,10), pady=(30, 0))
        self.searchbar = StringVar()
        self.bar = ttk.Entry(navigationFrame, textvariable=self.searchbar)
        self.bar.grid(column=1, row=0, sticky=(W), padx=(15, 15),pady=(30, 0))
        self.bar.insert(0, 'Search')

        # START DATE 
        ttk.Label(navigationFrame, text="Start Date:").grid(column=2, row=0, sticky=E, pady=(30, 0))
        self.startdate = StringVar()
        self.startD = ttk.Entry(navigationFrame, textvariable=self.startdate)
        self.startD.grid(column=3, row=0, sticky=(W),padx=(15, 15),pady=(30, 0))
        self.startD.insert(0, 'YYYY-MM-DD')

        # END DATE
        ttk.Label(navigationFrame, text="End Date:").grid(column=4, row=0, sticky=E, pady=(30, 0))
        self.enddate = StringVar()
        self.endD = ttk.Entry(navigationFrame, textvariable=self.enddate)
        self.endD.grid(column=5, row=0, sticky=(W),padx=(15, 15),pady=(30, 0))
        self.endD.insert(0, 'YYYY-MM-DD')

        #FILTER BY SUBURB
        ttk.Label(navigationFrame, text="Filter by Suburb:").grid(column=6, row=0, sticky=E, pady=(30, 0))
        self.dropdown1 = StringVar()
        self.dd1 = ttk.Combobox(navigationFrame, textvariable=self.dropdown1, values=["Select Suburb","BRONX", "BROOKLYN","MANHATTAN","QUEENS", "STATEN ISLAND"])
        self.dd1.grid(column=7, row=0, sticky=(W),padx=(15, 15),pady=(30, 0))
        self.dd1.current(0)
        self.dd1.state(["readonly"])
        self.dd1.bind("<<ComboboxSelected>>",lambda e: navigationFrame.focus())

        # BUTTONS
        # the command refers to the function below 
        ttk.Button(navigationFrame, text="Search", command=self.searchButton, width=20).grid(column=8, row=0, sticky=(N),padx=(10, 10) ,pady=(50, 20))
        ttk.Button(navigationFrame, text="Visualise", command=self.visualisations, width=20).grid(column=9, row=0, sticky=(N),padx=10,pady=(50, 20))
        ttk.Button(navigationFrame, text="Clear", command=self.Clear, width=20).grid(column=10, row=0, sticky=(N),padx=10, pady=(50, 20))

        # SQL TO SELECT TABLE HEADINGS ############ MOVE THIS TO OUTSIDE THE CLASS THEN PASS IT IN #############
        cursor.execute('SELECT * FROM NYC_RESTAURANT_INSPECTION_DATA')
        names = list(map(lambda x: x[0], cursor.description))

        # TREEVIEW SCROLLBAR SETTINGS 
        tree_scrolly = Scrollbar(treeframe)
        tree_scrolly.pack(side=RIGHT, fill=Y)
        tree_scrollx = Scrollbar(treeframe, orient='horizontal')
        tree_scrollx.pack(side=BOTTOM, fill=X)

        # TREEVIEW FOR DATABASE 
        tree = ttk.Treeview(treeframe, yscrollcommand=tree_scrolly.set, xscrollcommand=tree_scrollx.set, height=40)
        tree['columns'] = names
        tree.column("#0", width=50)
        tree.heading("#0", text='ID')
        for i in range(len(names)):
            tree.heading(i, text=names[i])
        # FOR LOOP FOR ID NUMBER VALUES. DO NOT USE 
        tree.pack(fill='both')
        tree_scrolly.configure(command=tree.yview)
        tree_scrollx.configure(command=tree.xview)
        
    def update_dataset(self, dset):
        self.dataset = dset
      
    #BUTTON FUNCTIONS
    def searchButton(self, *args):
        pass

    def visualisations(self, *args):
        # CREATES A TOP LEVEL WINDOW CONTAINING RADIOBUTTONS TO CALL DIFFERENT PLOTS IN MATPLOTLIB
        # CREATING THE TOPLEVEL, GIVING DIMENSIONS AND A TITLE, RESTRICTING RESIZING OF WINDOW
        visualiser = Toplevel(root)
        visualiser.geometry("350x500")
        visualiser.title('Select Plot Type')
        visualiser.resizable(FALSE,FALSE)
        # CREATING A NEW FRAME FOR THE TOP LEVEL WINDOW AND SETTING DEFAULTS 
        visFrame = ttk.Frame(visualiser)
        visFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        visualiser.columnconfigure(0, weight=1)
        visualiser.rowconfigure(0, weight=1)
        #CREATING A RADIO BUTTON FOR THE TOP LEVEL WINDOW
        radioButton = StringVar()
        SubLine = ttk.Radiobutton(visFrame, text='Violations Over Suburb - Line Graph', variable=radioButton, value='Subline').grid(column=0, row=0, sticky=(W), padx=20, pady=(20, 20))
        SubBar = ttk.Radiobutton(visFrame, text='Violations Over Suburb - Bar Graph', variable=radioButton, value='SubBar').grid(column=0, row=1, sticky=(W), padx=20, pady=(20, 20))
        AniLine = ttk.Radiobutton(visFrame, text='Animals Over Time and Suburb - Line Graph', variable=radioButton, value='AniLine').grid(column=0, row=3, sticky=(W), padx=20, pady=(20, 20))
        AniBar = ttk.Radiobutton(visFrame, text='Animals Over Time and Suburb - Bar Graph', variable=radioButton, value='AniBar').grid(column=0, row=4, sticky=(W), padx=20, pady=(20, 20))
        VioCode = ttk.Radiobutton(visFrame, text='Violation Over Time and Violation Code - Line Graph', variable=radioButton, value='VioCode').grid(column=0, row=5, sticky=(W), padx=20, pady=(20, 20))
        VioBar = ttk.Radiobutton(visFrame, text='Violation Over Time and Violation Code - Bar Graph', variable=radioButton, value='VioBar').grid(column=0, row=6, sticky=(W), padx=20, pady=(20, 20))
        # CREATING A BUTTON TO DIPLAY THE PLOT, POITNS TO PLOT FUNCTION 
        ttk.Button(visFrame, text="Plot", command=self.Plot, width=20).grid(column=0, row=7, sticky=(W),padx=20 ,pady=(50, 0))
        
    def Clear(self, *args):   #CLEAR RESULTS FUNCTION 
        pass
    def Plot(self, *args):    #VISUALISE PLOT FUNCTION 
        pass
        

root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.state('zoomed')
Application(root)
root.mainloop()


"""THESE ARE EXTRA FILTERS IN CASE WE WISH TO ADD ANY MORE!!!"""
   # # FILTER 2 
        # ttk.Label(mainframe, text="Filter by Cruisne:").grid(column=8, row=0, sticky=E, pady=(30, 0))
        # self.filter2 = StringVar()
        # self.fil2 = ttk.Entry(mainframe, textvariable=self.filter2)
        # self.fil2.grid(column=9, row=0, sticky=(W),padx=(15, 15),pady=(30, 0))
        # self.fil2.insert(0, 'Filter 2')
        # # FILTER 3
        # ttk.Label(mainframe, text="Filter by Animal:").grid(column=10, row=0, sticky=E, pady=(30, 0))
        # self.filter3 = StringVar()
        # self.fil3 = ttk.Entry(mainframe, textvariable=self.filter3)
        # self.fil3.grid(column=11, row=0, sticky=(W),padx=(15, 15),pady=(30, 0))
        # self.fil3.insert(0, 'Filter 3')
        # # FILTER 4
        # ttk.Label(mainframe, text="Filter By Violation Code:").grid(column=12, row=0, sticky=E, pady=(30, 0))
        # self.filter4 = StringVar()
        # self.fil4 = ttk.Entry(mainframe, textvariable=self.filter4)
        # self.fil4.grid(column=13, row=0, sticky=(W),padx=(10, 10),pady=(30, 0))
        # self.fil4.insert(0, 'Filter 4')
