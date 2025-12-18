import asyncio

from aiogram import Router, types
from llm.llm import parse_query
from analytics.executor import execute_query
from db import SessionLocal

router = Router()

@router.message()
async def handle_message(message: types.Message):
    if not message.text:
        await message.answer("Нужен текстовый запрос")
        return
    
    print("Message received:", message.text)
    
    # парсим текст через llm в отдельном потоке
    user_txt = message.text
    parsed = await asyncio.to_thread(parse_query, user_txt)
    
    if not parsed or parsed.get("error"):
        await message.answer("Не понял запрос")
        return
    
    # выполняем запрос к базе
    with SessionLocal() as session:
        try:
            result = execute_query(parsed, session)
        except Exception as e:
            print("Executor error:", e)
            await message.answer("Ошибка обработки запроса")
            return
    
    await message.answer(str(result))