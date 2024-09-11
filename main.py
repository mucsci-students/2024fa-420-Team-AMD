if __name__ == '__main__':
    quit = False
    while not quit:
        command = input('Enter UML Command: ')
        match command:
            case 'temp':
                print('Temporary test!')
            case _:
                print('error! print some help here')
