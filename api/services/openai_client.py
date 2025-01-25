from typing import Optional
from fastapi import HTTPException
from loguru import logger
from openai import AsyncOpenAI
from loguru import logger

from config import settings

class OpenAIClient:
    
    @staticmethod
    async def ask(
        question: str,
        from_lang: str = "ru",
        to_lang: str = "ru",
        context: Optional[str] = None,
        model: str = settings.default_model
    ) -> Optional[str]:
        """
        Метод для получения ответа от модели ИИ
        """

        client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_link
        )

        PROMPT = f"""Answer the question:
            #### Question: {question}
            #### Context: {context or "No context"}
        """

        try:
            answer = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": PROMPT}],
                stream=False,
            )
            answer = answer.choices[0].message.content
            # TODO: туть переводить ответ
            return answer
        except Exception as e:
            logger.error(f"Can not make request to LLM: {e}")
            raise HTTPException(
                status_code=500,
                detail="Can not make request to LLM: connect with support"
            ) 
