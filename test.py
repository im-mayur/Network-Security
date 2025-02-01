# Open the file in read mode
with open('requirements.txt', 'r') as file:
    lines=file.readlines()
    requirement_lst=[]
    for line in lines:
        # Print each line
        requirement=line.strip()
        requirement_lst.append(requirement)
       

    print(requirement_lst)