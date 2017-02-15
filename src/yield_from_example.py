class Node:

    def __init__(self, value):
        self.left = []
        self.value = value
        self.right = []

    def iterate(self):
        # for node in self.left:
        #     for value in node.iterate():
        #         yield value
        # yield self.value
        # for node in self.right:
        #     for value in node.iterate():
        #         yield value
        # <- This is cumbersome - use `yield from` instead

        for node in self.left:
            yield from node.iterate()
        yield self.value
        for node in self.right:
            yield from node.iterate()

    def node_iterate(self):
        for node in self.left:
            input_value = yield node.value
            self.compute_something(input_value)
        input_value = yield self.value
        self.compute_something(input_value)
        for node in self.right:
            input_value = yield node.value
            self.compute_something(input_value)

    def compute_something(self, input_value):
        print(input_value)


def main():
    root = Node(0)
    root.left = [Node(i) for i in [10, 20, 30]]
    root.left[0].right = [Node(i) for i in [11, 12, 13, 14]]
    root.right = [Node(i) for i in [40, 50, 60]]

    # for value in root.iterate():
    #     print(value)

    iter_obj = root.iterate()
    #iter_obj = root.node_iterate()
    send_value = None
    while True:
        try:
            received_value = iter_obj.send(send_value) # send a value into the generator, yield expression receives that value
            print("Received value {0} from generator".format(received_value))
            send_value = "Send back {0}".format(received_value)
            print('#' * 15)
        except StopIteration:
            print('Iteration stopped')
            break


if __name__ == "__main__":
    main()
