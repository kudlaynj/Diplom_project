from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import re
import crud_func

api = "7295601810:AAE0F2VLYt-bKByUkKBw4Gqkc2pPFIHgoS0"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Главное меню
start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Информация')],
        [KeyboardButton(text='Купить')],
        [KeyboardButton(text='Регистрация')],
    ], resize_keyboard=True)

# Меню продуктов
produkt_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Кольца', callback_data='rings')],
        [InlineKeyboardButton(text='Серьги', callback_data='earrings')],
        [InlineKeyboardButton(text='Браслеты', callback_data='bracelet')],
        [InlineKeyboardButton(text='Подвески', callback_data='pendant')],
    ])


# Состояния для регистрации
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer("Добро пожаловать в ювелирный магазин!", reply_markup=start_menu)


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    await message.answer(text='Выберите лот для покупки:', reply_markup=produkt_menu)


@dp.callback_query_handler(lambda call: call.data in ['rings', 'earrings', 'bracelet', 'pendant'])
async def show_product_info(call: types.CallbackQuery):
    product_info = {
        'rings': {
            'name': 'Кольца',
            'description': 'Оригинальное кольцо из золота добавит элегантности вашему стилю и будут '
                           'отлично гармонировать с любыми украшениями и аксессуарами.',
            'price': 'от 12 300',
            'image': 'c:\\Users\\Admin\\PycharmProjects\\JewerlyStore\\image_jewerly\\k_1.png'
        },
        'earrings': {
            'name': 'Серьги',
            'description': 'Модные серьги – это удивительное украшение, '
                           'способное привлечь внимание окружающих благодаря своему оригинальному дизайну.',
            'price': 'от 18 700',
            'image': 'c:\\Users\\Admin\\PycharmProjects\\JewerlyStore\\image_jewerly\\s_1.png'
        },
        'bracelet': {
            'name': 'Браслеты',
            'description': 'Золотой браслет – это не просто украшение, '
                           'это изящное золотистое дополнение к вашему образу, '
                           'которое подчеркивает стиль и вкус его владельца.',
            'price': 'от 9 780',
            'image': 'c:\\Users\\Admin\\PycharmProjects\\JewerlyStore\\image_jewerly\\b_1.png'
        },
        'pendant': {
            'name': 'Подвески',
            'description': 'Золотая подвеска - это прекрасный выбор в качестве подарка своей любимой девушке, '
                           'маме, сестре или коллеге. Подвеска в классическом дизайне будет идеальным дополнением'
                           'к повседневному образу и станет отличным подарком.',
            'price': 'от 11 320',
            'image': 'c:\\Users\\Admin\\PycharmProjects\\JewerlyStore\\image_jewerly\\p_1.png'
        }
    }

    product = product_info.get(call.data)

    # Кнопка "Купить" для каждого продукта
    buy_button = InlineKeyboardButton(text='Купить', callback_data=f'buy_{call.data}')
    buy_menu = InlineKeyboardMarkup().add(buy_button)

    # Отправка изображения продукта с его описанием и кнопкой "Купить"
    with open(product['image'], 'rb') as img:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=img,
            caption=(f"Название: {product['name']}\nОписание: {product['description']}\nЦена: {product['price']} руб."),
            reply_markup=buy_menu
        )


@dp.callback_query_handler(lambda call: call.data.startswith('buy_'))
async def handle_purchase(call: types.CallbackQuery):
    product_code = call.data.split('_')[1]

    product_names = {
        'rings': 'Кольца',
        'earrings': 'Серьги',
        'bracelet': 'Браслеты',
        'pendant': 'Подвески'
    }

    product_name = product_names.get(product_code, 'Продукт')

    await call.message.answer(f"Вы успешно отправили заявку на приобретение {product_name}!"
                              f"В ближайшее время с вами свяжется наш менеджер.")
    await call.answer()


@dp.message_handler(text='Информация')
async def inform(message: types.Message):
    await message.answer('Добро пожаловать в ювелирный магазин! '
                         'В нашем телеграмм-канале вы можете ознакомиться с доступными лотами ювелирных изделий',
                         reply_markup=start_menu)


@dp.message_handler(text='Регистрация')
async def sing_up(message: types.Message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    if not re.match("^[A-Za-z]+$", message.text):
        await message.answer('Имя пользователя должно содержать только латинские буквы. Попробуйте снова.')
        return

    if crud_func.is_included(message.text) != True:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

    if crud_func.is_included(message.text) == True:
        await message.answer("Пользователь существует, введите другое имя")
        await message.answer("Введите имя пользователя (только латинский алфавит):")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Регистрация завершена! Ваш баланс будет пополнен на 1000 призовых баллов.')

    # Начальный баланс пользователя
    await state.update_data(balance=1000)

    # Получаем данные пользователя из состояния
    data = await state.get_data()
    username = data['username']
    email = data['email']
    age = data['age']
    balance = data['balance']

    # Добавляем пользователя в базу данных
    crud_func.add_user(username=username, email=email, age=age, balance=balance)

    await message.answer(f"Пользователь {username} успешно зарегистрирован!")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
