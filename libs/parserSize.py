def getSize(size):
    counter = 0
    while size > 1024:
        counter += 1
        size /= 1024
    size = round(size, 2)
    if counter == 0:
        size = str(size)+"bytes"
    elif counter == 1:
        size = str(size)+"KB"
    elif counter == 2:
        size = str(size)+"MB"
    elif counter == 3:
        size = str(size)+"GB"
    elif counter == 4:
        size = str(size)+"TB"
    elif counter == 5:
        size = str(size)+"PB"
    elif counter == 6:
        size = str(size)+"ZB"
    else:
        size = "您太离谱了"

    return size
