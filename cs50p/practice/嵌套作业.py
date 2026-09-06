def  main ():
    number =get_number()
    print_flag(number )


def get_number():
    size = int ( input ("what size do you want ? "))
    return size 


def print_flag(a):
    for e in range (a ):
        for b in range ( a):
            if  b == e or b+e== a-1:
                print ("@",end = "" ) 
            else :
                print ("#",end ="")
        print ()
main () 