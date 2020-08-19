from threading import Thread

def f():
    import server
def f_2():
    import com

th_1, th_2 = Thread(target=f), Thread(target = f_2)

if __name__ == '__main__':
    th_1.start(), th_2.start()
    th_1.join(), th_2.join()
