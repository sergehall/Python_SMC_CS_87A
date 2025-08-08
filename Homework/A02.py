# Name : Siarhei Hancharou
# Assignment #: 2
# Submission Date : 09/24/2020
#
# Description of program :
# This is Math Trivia Quiz.

from random import randint

print("********************************************************")
print("Welcome to math Trivia Quiz .")
print("Math Quiz of 6 questions, the program will\n"
      "automatically select three questions for you.")
print("Win by answering all three questions correctly.")
print("********************************************************")
print()

#  The question is assigned to a variable.
one = 'What is the first step in the Order of Operations?\n' \
      + '1. Exponents\n' + '2. Addition\n' + '3. Brackets\n' \
      + '4. Subtraction\n' + '5. Multiplication'
two = 'What is notification of superfactorial?\n' + '1. #\n' + '2. !\n' \
      + '3. L\n' + '4. &\n' + '5. $'
three = 'What does pi equal?\n' + '1. 4.3532\n' + '2. 3.14159\n' \
        + '3. 2.7182\n' + '4. 6.28318\n' + '5. 3.017'
four = 'What is the degree of a triangle?\n' + '1. 90º\n' + '2. 540º\n' \
       + '3. 180º\n' + '4. 270º\n' + '5. 360º'
five = 'What are the numbers 2, 3, 5, 7, 11 ... ?.\n' + '1. Primer\n' \
       + '2. Odd\n' + '3. composite\n' + '4. float\n' + '5. None of these'
six = '1, 1, 2, 3, 5, 8, 13 ... are called ______ numbers.\n' \
      + "1. Euler's number\n" + '2. Lucky Numbers Slevin\n' + '3. Rāmānujan\n' \
      + '4. Fibonacci\n' + '5. Feigenbaum constants'

# Choose randomly three numbers but that would all be different numbers.
count = 0
while True:
    q_one = randint(1, 6)
    q_two = randint(1, 6)
    q_three = randint(1, 6)
    if q_one != q_two and q_two != q_three and q_one != q_three:
        break
    else:
        count += 1

#  A list of random numbers. We will pass it to the for loop.
question = [q_one, q_two, q_three]

#  Index, so that you can add zero to the place of the deleted
#  index(question. insert(index, 0)). The length of the list has not changed,
#  but the next iterations fall on the zero loop continue. In order to
#  repeatedly pass through the list, do not ask questions that have already
#  been answered , but only answer those whose value is not answered
#  correctly and their value in the list is not equal to 0.

index = 0

# The number of the question. In question.remove(n)- remove the answered
# question. For print out the question number.
n = 0

# count counts correctly answered questions.
count = 0
# Infinite while loop until there is a break command.
while True:
    #  The for loop goes through the list of questions where
    #  item = question numbers.
    for i in question:
        #  When we go through the list and meet the value zero.
        if i == 0:
            continue
        if i == 1:
            # Remember the index number. If the question is answered correctly,
            # we insert 0 at this index.
            index = question.index(i)
            # Since we change the value of i below to preserve the value of i,
            # we assign them to var n.
            n = i
            # The variable i is assigned a new value (this value is a question
            # for the player).
            i = one
        if i == 2:
            index = question.index(i)
            n = i
            i = two
        if i == 3:
            index = question.index(i)
            n = i
            i = three
        if i == 4:
            index = question.index(i)
            n = i
            i = four
        if i == 5:
            index = question.index(i)
            n = i
            i = five
        if i == 6:
            index = question.index(i)
            n = i
            i = six

        print('************* The',
              str(n) + 'th question out of six. *************')
        #  A question is asked to the player.
        print(i)  # Question(one, two, three, four, five or six)
        answer = int(input('Enter your answer (1,2,3,4 or 5): '))

        if i == one:
            if answer == 1:
                print('Perfectly. Congratulations on the correct answer.')
                print()
                question.remove(n)  # Removing the answered question
                question.insert(index,
                                0)  # Inserts 0 to the list at the index
                # of the answered question.
                count += 1
                continue
            else:
                print("Better luck next time.")
                print()

        if i == two:
            if answer == 5:
                print("Excellent. You're an advanced mathematician.")
                print()
                question.remove(n)
                question.insert(index, 0)
                count += 1
                continue
            else:
                print("Better luck next time.")
                print()

        if i == three:
            if answer == 2:
                print(
                    'Congratulations, you remember the basics of mathematics.')
                print()
                question.remove(n)
                question.insert(index, 0)
                count += 1
                continue
            elif answer == 3:
                print(
                    "The number 2.71828, known as Euler's number e, is "
                    "a mathematical constant\n "
                    "approximately equal to 2.71828.\n")
                continue
            else:
                print("Better luck next time.")
                print()

        if i == four:
            if answer == 3:
                print(
                    'Good! In a Euclidean space, the sum of angles of a '
                    'triangle equals 180 degrees.')
                print()
                question.remove(n)
                question.insert(index, 0)
                count += 1
                continue
            else:
                print("Better luck next time.")
                print()

        if i == five:
            if answer == 1:
                print(
                    'Right. A prime number is a natural number greater '
                    'than 1 that is not a product of\n'
                    'two smaller natural numbers.\n')
                print()
                question.remove(n)
                question.insert(index, 0)
                count += 1
                continue
            else:
                print("Better luck next time.")
                print()

        if i == six:
            if answer == 4:
                print(
                    'Terrific!. In mathematics, the Fibonacci numbers, '
                    'commonly denoted Fn,form\n'
                    'a sequence, called the Fibonacci sequence, '
                    'such that each number is the sum of\n'
                    'the two preceding ones, starting from 0 and 1...\n')
                print()
                question.remove(n)
                question.insert(index, 0)
                count += 1
                continue
            else:
                print("Better luck next time.")
                print()
    #  while loop control.
    if count == 3:
        print('Great! You answered all the questions correctly.')
        print('Thank you for playing. Goodbye')
        break
    if count < 3:
        print('You answered', count, 'out of 3 questions correctly')
        repeat = input(
            'Do you want to try your incorrect answers again? (y)es or (n)o?: ')
        print()
        if repeat == 'y':
            continue
        else:
            print("Don't worry, you'll be lucky next time!")
            break
