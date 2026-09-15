import time


#PRINT A FILE
with open("./txt/input.txt", "r",encoding='utf-8') as f:
    text_in =f.read()

print(text_in)
text_out = "This is what we know about the avocado: \n" + text_in + "\nCreated on " + time.ctime() + "\n\n"

#WRITE A FILE
with open("./txt/output.txt", "w",encoding='utf-8') as f:
    f.write(text_out)

print("File written!")