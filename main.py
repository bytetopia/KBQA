from qa.query_handler import QueryHandler


def main():
    if __name__ == '__main__':
        print('Welcome to KBQA. Enter "exit" to exit commmand line.')
        q = QueryHandler()
        query = input('Enter query: ')
        while query != 'exit':
            response = q.query(query)
            print(response)
            query = input('Enter query: ')


if __name__ == '__main__':
    main()


