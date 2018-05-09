import challenge3

if __name__ == '__main__':
    data = []
    with open(r'challenge4_data.txt') as file:
        for line in file:
            data.append(line.strip())
    for line in data:
        try:
            results = challenge3.single_byte_xor(line)
        except UnicodeDecodeError:
            continue
        #if len(results) > 0:
            #print(results.pop(min(results)).decode())
        print(line, ': ', results)
