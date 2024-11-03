from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import texts
from crud_functions import *


"""
Импортируем необходимые модули из aiogram:
      Bot — для создания бота.
      Dispatcher — для обработки сообщений.
      types — для работы с типами сообщений и других данных.
      MemoryStorage — для хранения состояний в памяти.
      FSMContext — для работы с контекстом машины состояний.
      State и StatesGroup — для работы с состояниями.
      executor — для запуска бота.
      ReplyKeyboardMarkup - для работы с обычной клавиатурой
      KeyboardButton - для работы с кнопками
      InlineKeyboardMarkup - для работы с Inline клавиатурой
      InlineKeyboardButton - для работы с Inline кнопками
"""

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()     # Возраст
    growth = State()  # Рост
    weight = State()  # Вес

# Создаем клавиатуру с кнопкой Регистрация
kb_reg = ReplyKeyboardMarkup(resize_keyboard=True)  # Обычная клавиатура
button_reg = KeyboardButton("Регистрация")          #  Объявление кнопки "Регистрация"
kb_reg.add(button_reg)                              # Кнопка добавляется

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True)  # Обычная клавиатура
button1 = KeyboardButton("Рассчитать")   #  Объявление кнопки "Рассчитать"
button2 = KeyboardButton("Информация")   #  Объявление кнопки "Информация"
button3 = KeyboardButton("Купить")       #  Объявление кнопки "Купить"
kb.add(button1, button2)           #  Кнопки добавляются в ряд
kb.add(button3)    # Кнопка добавляется ниже кнопок "Рассчитать" и "Информация"

# Объявляем кнопки для Inline клавиатуры

inline_button21 = InlineKeyboardButton("Product1", callback_data='product_buying')
inline_button22 = InlineKeyboardButton("Product2", callback_data='product_buying')
inline_button23 = InlineKeyboardButton("Product3", callback_data='product_buying')
inline_button24 = InlineKeyboardButton("Product4", callback_data='product_buying')

# Inline клавиатура inline_kb2, кнопки в один ряд

inline_kb2 = InlineKeyboardMarkup(inline_keyboard=[[inline_button21, inline_button22, inline_button23, inline_button24]])

inline_kb = InlineKeyboardMarkup()  # Inline клавиатура
inline_button1 = InlineKeyboardButton("Рассчитать норму калорий", callback_data='calories')
inline_button2 = InlineKeyboardButton("Формулы расчёта", callback_data='formulas')

              # callback_data= - данные, которые будут отправлены в запросе обратного вызова боту при нажатии кнопки
inline_kb.add(inline_button1, inline_button2)     #  Inline кнопки добавляются в ряд

@dp.message_handler(commands=['start'])        #  Запуск функции start при вводе команды /start
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=kb_reg)   #  Ответное сообщение и вызов
                                                                                        # клавиатуры из двух кнопок

# Создаем функции цепочки состояний RegistrationState

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()   # Ожидаем ввод имени пользователя

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) == False:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()   # Ожидаем ввод email пользователя
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()  # Функция отправляет в ожидание ввода имени пользователя

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await RegistrationState.age.set()  # Ожидаем ввод возраста пользователя
    await message.answer('Введите свой возраст:')

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    user_data = await state.get_data()       # Сохранение состояния
    add_user(user_data["username"], user_data["email"], user_data["age"])
    await message.answer('Регистрация прошла успешно', reply_markup=kb)  # Отправляется сообщение и открывается
                                                                           # клавиатура "kb"
    await state.finish()    # Завершаем прием состояний при помощи метода finish()


@dp.message_handler(text='Купить')  #  Реакция на нажатие кнопки 'Купить', запуск функции get_buying_list
async def get_buying_list(message):
    await message.answer(get_all_products(1))  # Вывод сообщения о продукте
    with open("1.jpg", "rb") as img1:                         # Открытие фотографии продукта
        await message.answer_photo(img1)                      # Вывод фотографии продукта
    await message.answer(get_all_products(2))
    with open("2.jpg", "rb") as img2:
        await message.answer_photo(img2)
    await message.answer(get_all_products(3))
    with open("3.jpg", "rb") as img3:
        await message.answer_photo(img3)
    await message.answer(get_all_products(4))
    with open("4.jpg", "rb") as img4:
        await message.answer_photo(img4)

# Прописываем хендлер реагирующий при нажатии кнопки Product
@dp.callback_query_handler(text="product_buying")
async def end_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")

@dp.message_handler(text='Рассчитать')  #  Реакция на нажатие кнопки 'Рассчитать', запуск функции main_menu
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=inline_kb)  #  Сообщение и вызов inline_kb клавиатуры

@dp.callback_query_handler(text='formulas')  #  Реакция на нажатие кнопки 'Формулы расчёта', запуск функции get_formulas
async def get_formulas(call):
    await call.message.answer("Для женщин: 10 х вес(кг) + 6.25 х рост(см) - 5 х возраст(г) - 161")
    await call.message.answer("Для мужчин: 10 х вес(кг) + 6.25 х рост(см) - 5 х возраст(г) - 5")

@dp.callback_query_handler(text='calories')  #  Запуск функции set_age на нажатие кнопки "Рассчитать норму калорий"
async def set_age(call):
    await call.answer()  #  Завершение вызова. Без этой команды кнопка останется не активной(некликабельной)
    await call.message.answer("Введите свой возраст")   #  Ответное сообщение
    await UserState.age.set()                           #  Ожидание работы следующего хэндлера

@dp.message_handler(state=UserState.age)        #  Запуск функции set_growth при вводе возраста
async def set_growth(message, state):
    await state.update_data(age=message.text)   #  Здесь в словаре age - ключ, введенное число - значение ключа
    await message.answer("Введите свой рост")   #  Ответное сообщение
    await UserState.growth.set()                #  Ожидание работы следующего хэндлера

@dp.message_handler(state=UserState.growth)     #  Запуск функции set_weight при вводе роста
async def set_weight(message, state):
    await state.update_data(growth=message.text)   #  Здесь в словаре growth - ключ, введенное число - значение ключа
    await message.answer("Введите свой вес")    #  Ответное сообщение
    await UserState.weight.set()                #  Ожидание работы следующего хэндлера

@dp.message_handler(state=UserState.weight)     #  Запуск функции send_calories при вводе веса
async def send_calories(message, state):
    await state.update_data(weight=message.text)   #  Здесь в словаре weight - ключ, введенное число - значение ключа
    data = await state.get_data()               # Это элемент, который позволит получить данные состояния (это словарь)
    age = int(data.get("age"))        #  Возраст, значение с ключем "age"
    growth = int(data.get("growth"))  #  Рост, значение с ключем  "growth"
    weight = int(data.get("weight"))  #  Вес, значение с ключем  "weight"
    calories1 = 10 * weight + 6.25 * growth - 5 * age + 5    #  Формула для мужчин
    calories2 = 10 * weight + 6.25 * growth - 5 * age - 161  #  Формула для женщин
    await message.answer(f"Ваша норма калорий (для мужчин): {calories1} ккал.")  #  Считаем норму калорий по формуле
                                                                                 #  Миффлина - Сан Жеора для мужчин
    await message.answer(f"Ваша норма калорий (для женщин): {calories2} ккал.")  #  Считаем норму калорий по формуле
                                                                                 # Миффлина - Сан Жеора для женщин
    await state.finish()  #  Когда машина отработала, ее нужно остановить, чтобы сохранить свое состояние

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)  #  Запуск из этого файла