# Вывести последнюю букву в слове
word = 'Архангельск'
print(word[-1])
# ???


# Вывести количество букв "а" в слове
word = 'Архангельск'
print(word.lower().count('а'))
# ???


# Вывести количество гласных букв в слове
word = 'Архангельск'
vowel_letters = 'аеёиоуыэюя'
vowel_letters_counter = 0
for letter in word.lower():
    if letter in vowel_letters:
        vowel_letters_counter += 1
print(vowel_letters_counter)
# ???


# Вывести количество слов в предложении
sentence = 'Мы приехали в гости'
print(len(sentence.split()))
# ???


# Вывести первую букву каждого слова на отдельной строке
sentence = 'Мы приехали в гости'
for word in sentence.split():
    print(word[0])
# ???


# Вывести усреднённую длину слова в предложении
sentence = 'Мы приехали в гости'
numbers_of_letters = 0
for word in sentence.split():
    numbers_of_letters += len(word)
print(numbers_of_letters / len(sentence.split()))
# ???