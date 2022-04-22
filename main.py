import math
import tkinter as tk
from tkinter import PhotoImage, filedialog, ttk
from tkinter.messagebox import showinfo, askokcancel, WARNING, INFO
from readWrite import f2dmtxEncode
from readWrite import DecodeFromImage
from PIL import Image
from filenameFromPath import path_leaf
from printready import MakePrintReady
import webbrowser

matrixSize = 1555
matricesPerPaper = 18
largeMatrixThreshold = 100
outputSizeKb = 150

def PromptOutput():
    return filedialog.askdirectory()

def PromptEncodeConfirm(dataSize: int):
    matrices = math.ceil(dataSize / matrixSize)
    pageCount = math.ceil(matrices / matricesPerPaper)
    outputSize = outputSizeKb * matrices

    answer = False
    if matrices > largeMatrixThreshold:
        answer = askokcancel(
            title='Continue encoding?',
            message='''!!WARNING!! Encoding will create {matrixCount} matrices, or {pages} double-sided pages, output will be {imageSize} KB. Encoding may take some time.
            '''.format(matrixCount=matrices, pages=pageCount, imageSize=outputSize),
            icon=WARNING)
    else:
        answer = askokcancel(
            title='Continue encoding?',
            message='''Encoding will create {matrixCount} matrices, or {pages} double-sided pages, output will be {imageSize} KB. Continue encoding?
            '''.format(matrixCount=matrices, pages=pageCount, imageSize=outputSize),
            icon=INFO)

    return answer

def EncodeFile():
    # Prompt user for file paths
    filePaths = filedialog.askopenfilenames()

    # Prompt user for output location
    outputPath = PromptOutput()

    # Convert file(s) to data matrix
    filenames = []
    matrixImages = []
    dataSize = 0
    for path in filePaths:
        # Read file data
        fileToEncode = open(path, 'rb')
        rawData = fileToEncode.read()
        fileToEncode.close()

        matrices = f2dmtxEncode(rawData, path_leaf(path))

        # Ready matrices for printing and generate filenames
        for matrix in matrices:
            filename = matrix[0]
            matrixImage = matrix[1]
            partitionIndex = matrix[2]
            totalPartitions = matrix[3]

            matrixImage = MakePrintReady(matrixImage, filename, str(partitionIndex + 1) + '/' + str(totalPartitions))

            filename = filename + '_' + str(partitionIndex) + '-' + str(totalPartitions - 1)
            filenames.append(outputPath + "/" + filename + '.png')
            matrixImages.append(matrixImage)
            dataSize += matrix[4]
    
    # Prompt user to continue encoding
    if not PromptEncodeConfirm(dataSize):
            return
    
    # Write matrices to disk
    for i, matrix in enumerate(matrixImages):
        matrix.save(filenames[i])
    
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
    file = DecodeFromImage(images)
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

def onReturn(event):

# Window generation
root = tk.Tk()
root.title('file2dmtx')
root.geometry('400x500+50+50')
root.resizable(False, False)
root.iconbitmap("./barcode.ico")

root.bind('<Return>', onReturn)

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