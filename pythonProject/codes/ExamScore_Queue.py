from queue import Queue

def read_scores(scores_queue, student):
    while True:
        if scores_queue.full():
            print("The given queue score is now full!")
            break
        else:
            score = float(input("Enter exam score of student " + str(student) + ": "))
            scores_queue.put(score)
            list_score.append(score)
            student += 1

    return scores_queue

def print_scores(scores_queue, student):
    print("Exam scores in the queue excluding of 100:\n")
    while not scores_queue.empty():
        score = scores_queue.get()
        if score != 100:
            print("student: ", student,"- score: "+ str(score))
            student += 1

max_queue_size = int(input("\nEnter the maximum size of the queue: "))
scores_queue = Queue(maxsize=max_queue_size)
list_score =[]
student = 1

print("\n~~~~~~~~~~Enter Exam scores~~~~~~~~~~")
read_scores(scores_queue, student)
print("\n~~~~~~~~~~All Exam scores~~~~~~~~~~")
print_scores(scores_queue, student)
print("\n~~~~~~~~~~Exam scores in list~~~~~~~~~~")
print(list_score)