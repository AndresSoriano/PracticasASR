from numpy.f2py.auxfuncs import throw_error

import handlerSNMP as hs
from six.moves import tkinter as tk
from tkinter import ttk
from threading import *
class GUI(tk.Frame):
    def __init__(self, parent = None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

        self.commmnity_lbl = tk.Label(self.parent, text = "ComunidadASR")

        self.commmnity_lbl.pack()
        self.commmnity_lbl.place(relx=.1, rely=.1, anchor="c")

        self.com_text = tk.Entry(self.parent)
        self.com_text.insert(0, "gr_4cm1")
        self.com_text.pack()
        self.com_text.place(relx=.3, rely = 0.1, anchor = "c")


        self.ip_lbl = tk.Label(self.parent, text = "IP:")
        self.ip_lbl.pack()
        self.ip_lbl.place(relx =.1, rely = 0.15, anchor = "c")

        self.ip_text = tk.Entry(self.parent)
        self.ip_text.insert(0, "localhost")
        self.ip_text.pack()
        self.ip_text.place(relx = .3, rely = .15, anchor = "c")

        self.thresh_lbl = tk.Label(self.parent, text="Umbral: (bp,go,set)")
        self.thresh_lbl.pack()
        self.thresh_lbl.place(relx=.1, rely=0.2, anchor="c")

        self.thresh_text = tk.Entry(self.parent)
        self.thresh_text.insert(0, "25, 80, 20")
        self.thresh_text.pack()
        self.thresh_text.place(relx=.3, rely=.2, anchor="c")

        self.options_oid = ttk.Combobox(self.parent)
        self.options_oid.place(relx = 0.3, rely = 0.3, anchor="c")
        self.options_oid["values"] = ["RAM", "CPUload", "DISCO"]
        self.oids = {"CPUload":"iso.3.6.1.2.1.25.3.3.1.2.196608","RAM":"1.3.6.1.4.1.2021.4.6.0","DISCO": "1.3.6.1.2.1.1.3.0"}

        self.btn_start = tk.Button(self.parent, text = "Start", command = self.run)
        self.btn_start.pack()
        self.btn_start.place(relx=0.1, rely=.35, anchor="c")


        #self. = tk.
    def run(self):
        thread = Thread(target = self.start, args=(self.oids[self.options_oid.get()], self.options_oid.get()))
        thread.start()
    def init_ui(self):
        self.parent.title("Revision")

    def start(self, oid, type):
        path_rrd = "/home/mintsoriano2/Escritorio/"
        name_rrd = "trend.rrd"

        h1 = hs.HandlerSNMP(path_rrd, name_rrd)

        h1.create(type)

        commmnity = self.com_text.get()
        ip = self.ip_text.get()
        thresholds = self.thresh_text.get()
        thresholds.replace(" ", "")
        thre = thresholds.split(", ")

        print(thre)
        self.umbrales = {"breakpoint": thre[0], "set": thre[2], "go": thre[1]}
        h1.update(commmnity, ip, OID = oid, type = type)
        print(self.options_oid.get())
        #h1.create_image(path_rrd,
         #               self.umbrales["breakpoint"],
          #              self.umbrales["set"],
           #             self.umbrales["go"], self.options_oid.get())

        h1.deteccion(self.umbrales, type = type)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("600x400")
    app = GUI(parent = root)
    app.mainloop()
    root.destroy()