from tkinter import * 

root = Tk()

labelText = StringVar()
labelText.set("")

entryField = Entry(root, width= 70)
entryField.grid(row=0, column=0)
entryField.insert(0, "Name here")

myLabel = Label(root, textvariable=labelText)
myLabel.grid(row=2, column = 0)


def myClick():
	labelText.set("Hello " + entryField.get())	
	


clickButton = Button(root, text="Enter your name", command=myClick)

clickButton.grid(row=1, column=0)

root.mainloop()


