# import libraries
from googlesearch import search
from urllib import request
from bs4 import BeautifulSoup as bs
import re
import tkinter as tk
import nltk

window = tk.Tk()
csvtext = ""
nltk.download('punkt')


def searchQuery():
    global csvtext
    result_output.delete(0.0, 'end')
    query = query_input.get()
    queries = re.split('\s', query)
    scripts = ""
    urls = "URL:\n"
    csv = "kalimat_relevan\n"  # save all sentences related to query

    for url in search(query, lang='id', num=10, stop=10, pause=2.0):
        urls += ("- %s\n" % url)
        scripts += ("--- KALIMAT YANG RELEVAN UNTUK ALAMAT: %s ---\n" % url)

        # get response from the webr
        req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = request.urlopen(req, timeout=20)
        html = response.read().decode(encoding='utf-8', errors='ignore')

        # get HTML text using BeautifulSoup
        soup = bs(html, "html.parser")
        pars = []
        for par in soup.stripped_strings:
            pars.append(str(par))

        # segment and clean the raw text then search the query inside lines
        i = 1

        for par in pars:
            lines = nltk.sent_tokenize(par)
            for line in lines:
                # clean the wild characters
                line = re.sub(r"[^\w\s]", "", line)

                # search query inside line
                pattern = re.compile(r'\b(?:%s)\b' % "|".join(queries))
                result = re.search(pattern, line)
                if result:
                    scripts += ("%d. %s\n" % (i, line.strip()))
                    i += 1
                    csv += ("%s\n" % line.strip())
        scripts += "\n"
    scripts = urls+("Kueri yang dimasukkan\n\"%s\"\n" % query)+scripts
    result_output.insert(0.0, scripts)
    csvtext = csv


def exportToCSV(csvtext):
    file = open('related_word.csv', 'w')
    file.write(csvtext)
    file.close()


height = int(window.winfo_screenwidth()*0.5)
width = int(window.winfo_screenheight()*0.5)
dimension = str(height)+"x"+str(width)

# set the title
window.title("Kuis 1 PBA - Aplikasi IR Sederhana (09021281823071)")
frame = tk.Frame(master=window, width=100)

# set label kueri
query_label = tk.Label(master=frame, text="Kueri")
query_label.grid(column=0, row=0, sticky='w')

# set entry field (a line only)
query_input = tk.Entry(master=frame, width=100)
query_input.grid(column=0, row=1, sticky='w', columnspan=4)

# set label output
result_label = tk.Label(master=frame, text="Hasil Kueri yang Relevan")
result_label.grid(sticky='w')

# set text field output (not editable)
result_output = tk.Text(master=frame, wrap='word')
result_output.grid(columnspan=4)

# button search left
proceed_btn = tk.Button(master=frame, text="Cari Dokumen",
                        width=15, command=searchQuery)
proceed_btn.grid(column=0, row=4, sticky='w')

# button export to csv middle command=lambda: exportToCSV(C)
export_btn = tk.Button(master=frame, text="Ekspor ke CSV",
                       width=15, command=lambda: exportToCSV(csvtext))
export_btn.grid(column=1, row=4, sticky='w')

# button exit right
exit_btn = tk.Button(master=frame, text="Keluar",
                     command=window.destroy, width=15)
exit_btn.grid(column=3, row=4, sticky='e')

frame.place(relx=0.5, rely=0.5, anchor='center')
window.geometry(dimension)
window.resizable()
# display window
window.mainloop()
