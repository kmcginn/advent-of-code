import hashlib

def main():
    door = 'ffykfhsq'
    password = ['', '', '', '', '', '', '', '']
    print(password)
    i = 0
    while '' in password:
        h = hashlib.md5(door + str(i)).hexdigest()
        if h[:5] == '00000':
            position = int(h[5], 16)
            if position < 8:
                if password[position] == '':
                    password[position] = h[6]
                    print(password)
        i = i + 1
    print(password)

main()
