import aiohttp
from memorycode.config import MEMORYCODE_EMAIL, MEMORYCODE_PASSWORD, MEMORYCODE_BASE_URL
import json
import logging

logger = logging.getLogger(__name__)

async def get_access_token(email, password, device='bot-v0.0.1'):
    """
    Asynchronously retrieves an access token using the provided email, password, and device parameters.
    
    Parameters:
        email (str): The email of the user.
        password (str): The password of the user.
        device (str): The device identifier (default is 'bot-v0.0.1').
    
    Returns:
        str: The access token if available in the response data, otherwise returns the data itself.
    """
    url = f"{MEMORYCODE_BASE_URL}/api/v1/get-access-token"
    params = {"email": email, "password": password, "device": device}
    return (await aiohttp.request("POST", url, params=params)).json()["access_token"]


async def update_memory_page(initial_page_file, updated_fields_file, access_token):
    """
    This code defines an asynchronous function update_memory_page that updates a memory page by loading data from two JSON files, 
    merging the data, and sending a PUT request to a specified URL with the updated data using aiohttp.
    If the request is successful (status code 200), it logs a success message; otherwise,
      it logs an error message with the error code and text.
    """
    # Загрузка данных из файлов JSON
    with open(initial_page_file, 'r') as file:
        initial_page_data = json.load(file)
    with open(updated_fields_file, 'r') as file:
        updated_fields_data = json.load(file)

    # Обновление изначальных данных согласно второму файлу
    initial_page_data.update(updated_fields_data)

    url = f"{MEMORYCODE_BASE_URL}/page/{initial_page_data['id']}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {access_token}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=initial_page_data, headers=headers) as response:
            if response.status == 200:
                logger.info("Страница памяти успешно обновлена!")
            else:
                logger.error("Произошла ошибка при обновлении страницы памяти.")
                logger.error(f"Код ошибки: {response.status}")
                logger.error(f"Текст ошибки: {await response.text()}")


async def search_pages(access_token, query_params):
    """
    Этот код представляет собой асинхронную функцию search_pages, 
    которая выполняет поиск страниц с использованием указанных параметров запроса.
    Функция отправляет GET-запрос по указанному URL с параметрами запроса и возвращает результат в формате JSON.
    """
    url = f"{MEMORYCODE_BASE_URL}/page/search"
    params = {"access_token": access_token, **query_params}
    async with aiohttp.ClientSession() as session:
        response = await session.get(url, params=params)
        return await response.json()


async def link_pages(access_token, link_data):
    """
    Этот код представляет собой асинхронную функцию link_pages,
      которая отправляет POST-запрос на указанный URL с заголовком авторизации и данными в формате JSON. 
      Затем функция возвращает результат запроса в формате JSON.
    """
    url = f"{MEMORYCODE_BASE_URL}/page/relative"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with aiohttp.ClientSession() as session:
        response = await session.post(url, headers=headers, json=link_data)
        return await response.json()


async def get_individual_page_by_name(access_token, name):
    """
    Этот код определяет асинхронную функцию get_individual_page_by_name, которая извлекает определенную страницу по имени.
    Он выполняет запрос GET к заданному URL-адресу с указанными заголовками, используя aiohttp ClientSession.
    Если статус ответа не 200 или тип контента не JSON, он регистрирует ошибки.
    Затем он обрабатывает данные ответа JSON, выполняя поиск страницы с совпадающим именем в данных.
    Если он найден, он возвращает данные страницы в формате JSON; в противном случае он регистрирует предупреждение и возвращает None.
    Если во время запроса произойдет какая-либо ошибка,
    он регистрирует ошибку и возвращает None.

    """
    url = f"{MEMORYCODE_BASE_URL}/api/cabinet/individual-pages"
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json", "Content-Type": "application/json;charset=UTF-8"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error("Ошибка при получении страницы")
                    logger.error(f"Код ошибки: {response.status}")
                    logger.error(f"Текст ошибки: {await response.text()}")
                    return None
                content_type = response.headers.get("Content-Type", "")
                if "application/json" not in content_type:
                    logger.error("Ошибка при получении страницы: Не JSON, получен HTML.")
                    logger.error(f"Тип контента: {content_type}")
                    return None
                data = await response.json()
                for page in data:
                    if isinstance(page, dict) and page.get('name') == name:
                        return json.dumps(page)
                logger.warning("Страница памяти не найдена.")
                return None
        except aiohttp.ClientError as e:
            logger.error("Ошибка при выполнении запроса:")
            logger.error(e)
            return None


async def get_all_memory_pages(access_token):
    """
    Этот код определяет асинхронную функцию get_all_memory_pages, которая извлекает все страницы памяти, используя конечную точку API.
    Он отправляет запрос GET с указанными заголовками и токеном доступа. Если статус ответа не 200, он регистрирует ошибку с подробностями.
    Если содержимое ответа не является JSON, регистрируется ошибка. Наконец, он возвращает данные JSON всех полученных страниц памяти.
    Если во время запроса возникает какая-либо ошибка, она регистрируется и возвращает None.
    """
    url = f"{MEMORYCODE_BASE_URL}/api/cabinet/individual-pages"
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json", "Content-Type": "application/json;charset=UTF-8"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error("Ошибка при получении всех страниц памяти.")
                    logger.error(f"Код ошибки: {response.status}")
                    logger.error(f"Текст ошибки: {await response.text()}")
                    return None

                content_type = response.headers.get("Content-Type", "")
                if "application/json" not in content_type:
                    logger.error("Ошибка при получении всех страниц памяти: ожидался JSON, получен HTML.")
                    logger.error(f"Тип контента: {content_type}")
                    return None

                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            logger.error("Ошибка при выполнении запроса:")
            logger.error(e)
            return None


async def main():
    """
    Описание всей функции, ее параметров и типов возвращаемых значений.
    """
    access_token = await get_access_token(MEMORYCODE_EMAIL, MEMORYCODE_PASSWORD)
    if access_token:
        pages_info = await get_all_memory_pages(access_token)
        logger.info("Все карточки:", pages_info)
        person_name = "Иванов Иван Иванович"
        page_info = await get_individual_page_by_name(access_token, person_name)
        page_info = json.loads(page_info)
        if page_info:
            logger.info("Информация о человеке:")
            logger.info("Имя:", page_info.get('name'))
            logger.info("Дата рождения:", page_info.get('birthday_at'))
            logger.info("Дата смерти:", page_info.get('died_at'))
            logger.info("Эпитафия:", page_info.get('epitaph'))
        else:
            logger.info(f"Страница с именем '{person_name}' не найдена.")
    else:
        logger.error("Не удалось получить токен доступа.")

