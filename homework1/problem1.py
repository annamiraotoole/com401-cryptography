import string


Q1a_m = "To anyone who knew the country well, the mere style and title of Don Quixote of La Mancha gave the key to the authors meaning at once. La Mancha as the knights country and scene of his chivalries is of a piece with the pasteboard helmet, the farm-labourer on ass-back for a squire, knighthood conferred by a rascally ventero, convicts taken for victims of oppression, and the rest of the incongruities between Don Quixotes world and the world he lived in, between things as he saw them and things as they were."

s = "aaaaaaAAA bb cc dd i"

def preproccess(message):

    # remove spaces
    message = message.replace(" ", "")
    # make lowercase
    message = message.lower()

    # find positions of repeated characters
    indices = []
    for i in range(len(message)-1):
        if message[i] == message[i+1]:
            indices += [i]

    # add "x" between all repeated characters
    c = 0
    for i in indices:
        message = message[:i+c+1] + "x" + message[i+c+1:]
        c += 1

    # add "x" to message if it has odd length
    if len(message) % 2 == 1:
        message += "x"

    # split into digrams
    digrams = []
    while message:
        digrams += [message[:2]]
        message = message[2:]

    return digrams


def main():
    print(preproccess(s))

if __name__ == "__main__":
    main()
