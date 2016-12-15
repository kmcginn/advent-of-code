import hashlib

def main():
    door = 'ffykfhsq'
    password = ''
    i = 0
    while len(password) < 8:
        h = hashlib.md5(door + str(i)).hexdigest()
        if h[:5] == '00000':
            password += h[5]
        i = i + 1
    print(password)

if __name__ == "__main__":
    main()
