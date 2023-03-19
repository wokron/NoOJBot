from bot import NoOJBot
from utils import get_parser, set_openai_key

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    set_openai_key()

    bot = NoOJBot(args.ppath, args.mpath, args.dbg, args.mmem)

    while True:
        input_str = input("User:")

        if input_str.lower() == "quit" or input_str.lower() == "q":
            break

        print("NoOJBot:" + bot(input_str))

    print("quit success")
