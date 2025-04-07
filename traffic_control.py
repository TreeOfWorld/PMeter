# 验证流量控制的可行性
class Operation:
    """
    用于执行的任务（这部分代码似乎该写在Task中）
    """

    """
    定义Operation的类型？或许也可以不用定义，毕竟我会在后面定义执行动作
    """
    operation_type: str

    def __init__(self, **kwargs):
        self.operation_type = kwargs['operation_type']

    def create_operation(self):
        """
        定义生产任务的方式
        :return:
        """

    pass


class Producer:
    """
    生产任务（这部分代码似乎该写在Task中）
    """
    pass

    def __init__(self, *args, **kwargs):
        pass


class Consumer:
    """
    消费任务（这部分代码似乎该写在Task中）
    """
    pass

    def __init__(self, *args, **kwargs):
        pass


class Task:
    operation_list: list[Operation] = []
    producer: Producer
    consumer: Consumer

    def __init__(self, *args, **kwargs):
        self.define_operation()
        self.define_producer(kwargs['producer_conf'])
        self.define_consumer(kwargs['consumer_conf'])
        pass

    def define_operation(self):
        pass

    def define_producer(self, conf):
        self.producer = Producer(conf)
        pass

    def define_consumer(self, conf):
        self.consumer = Consumer(conf)
        pass


def main():
    pass


if __name__ == '__main__':
    pass
