import tkinter as tk
from tkinter import PhotoImage, filedialog, ttk
from tkinter.messagebox import showinfo
from readWrite import f2dmtxEncode
from readWrite import f2dmtxDecode
from PIL import Image
from filenameFromPath import path_leaf
from printready import MakePrintReady
import webbrowser

def PromptOutput():
    return filedialog.askdirectory()

def EncodeFile():
    # Prompt user for file paths
    filePaths = filedialog.askopenfilenames()

    # Prompt user for output location
    outputPath = PromptOutput()

    # Convert file(s) to data matrix
    for path in filePaths:
        # Read file data
        fileToEncode = open(path, 'rb')
        rawData = fileToEncode.read()
        fileToEncode.close()

        matrices = f2dmtxEncode(rawData, path_leaf(path))

        # Write matrices to disk
        for matrix in matrices:
            filename = matrix[0]
            partitionIndex = matrix[2]
            totalPartitions = matrix[3]

            printReady =  MakePrintReady(matrix[1], filename, str(partitionIndex + 1) + '/' + str(totalPartitions))

            filename = filename + '_' + str(partitionIndex) + '-' + str(totalPartitions - 1)
            printReady.save(outputPath + "/" + filename + '.png')
    
    # Success message
    showinfo('Success!', 'Encoded files successfully!')

def DecodeFile():
    # Prompt user for file paths
    filePaths = filedialog.askopenfilenames()

    # Prompt user for output location
    outputPath = PromptOutput()

    # Decode file data
    images = []
    for path in filePaths:
        images.append(Image.open(path))
    print('Beginning decode...')
    file = f2dmtxDecode(images)
    print('Decode complete!\n\nWriting file to disk')

    # Write file to disk
    print(file[0])
    writeFile = open(outputPath + '/' + file[0], "wb")
    writeFile.write(file[1])
    writeFile.close()
    print('File written to disk!')

    # Success message
    showinfo('Success!', 'Decoded file successfully!')

def gotoGithub():
    webbrowser.open('https://github.com/Suscept/file2dmtx')

def create_main_window():
    root = tk.Tk()
    root.title('file2dmtx')
    root.geometry('400x500+50+50')
    root.resizable(False, False)
    root.iconbitmap("./barcode.ico")

    encodeButton = ttk.Button(
        root,
        text='Encode file',
        command=EncodeFile
    )

    encodeButton.pack(
        ipadx=0,
        ipady=5,
        side='left',
        expand=True,
    )

    decodeButton = ttk.Button(
        root,
        text='Decode matrix',
        command=DecodeFile
    )

    decodeButton.pack(
        ipadx=0,
        ipady=5,
        side='left',
        expand=True,
    )

    # Github logo
    githubLogo = PhotoImage(file=r"C:\Users\garfi\Pictures\Code\file2dmtx\GitHub-Mark-64px.png")

    githubButton = ttk.Button(
        root,
        text='My Github',
        image=githubLogo,
        command=gotoGithub
    )

    githubButton.pack(
        ipadx=0,
        ipady=5,
        side='bottom',
        expand=True,
    )

    root.mainloop()

if __name__ == "__main__":
    create_main_window()