# coding: utf-8
import subprocess
start_runner = "python runner.py"
start_redis = "redis/src/redis-server redis/redis.conf"
del_redis_data = "redis/src/redis-cli flushall"
check_redis = "redis/src/redis-cli scan 0"
works_1 = "python works_redis.py"
works_2 = "python works_redis.py"
works_3 = "python works_redis.py"
works_4 = "python works_redis.py"
works_5 = "python works_redis.py"


if __name__ == '__main__':
    print("start redis")
    subprocess.Popen(start_redis, shell=True)
    # print("del redis data")
    # subprocess.run(del_redis_data, shell=True)
    # print("check redis data")
    # subprocess.run(check_redis, shell=True)
    # print("start_runner")
    # subprocess.Popen(start_runner, shell=True)
    # print("run works 1")
    # subprocess.Popen(works_1, shell=True)
    # print("run works 2")
    # subprocess.Popen(works_2, shell=True)
    # print("run works 3")
    # subprocess.Popen(works_3, shell=True)
    # print("run works 4")
    # subprocess.Popen(works_4, shell=True)
    # print("run works 5")
    # subprocess.Popen(works_5, shell=True)
    # print("done")
