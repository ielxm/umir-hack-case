from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from constants import *
from validation import *

# выбранный дизайн-проект
class QuizForm(BaseModel):
    apartment_type: ApartmentTypes = Field(
        description="Вопрос: Какое помещение вы планируете оформить"
    )
    rooms_to_include: List[RoomTypes] = Field(
        description="Вопрос: Какие зоны нужно включить в дизайн-проект"
    )
    size: float = Field(
        description="Вопрос: Площадь апартаментов (в м²)"
    )
    budget: float = Field(
        description="Вопрос: Бюджет на реализацию проекта (в млн. рублей)"
    )
    apartment_style: ApartmentStyles = Field(
        description="Вопрос: Предпочитаемый стиль апартаментов"
    )
    comment: Optional[str] = Field(
        description="Комментарий", default=None
    )
    contacts: ContactForm = Field(
        description="Контактные данные клиента (объект класса ContactForm)"
    )

# контактная информация
class ContactForm(BaseModel):
    phone_number: str = Field(description="Номер мобильного телефона пользователя")                         # обязательно
    name: str = Field(description="Имя пользователя")                                                       # обязательно
    email: str = Field(description="Электронная почта пользователя")                                        # обязательно
    #available_at_weekdays: Optional[str] = Field(description="Доступность (дни недели)", default=None)     # необязательно
    #available_at_hours: Optional[str] = Field(description="Доступность (часы дня)", default=None)          # необязательно

    # Валидация номера телефона
    @field_validator("phone_number")
    def phone_number_validation(cls, value: str) -> str:
        # Если введён некорректный номер телефона
        if not phone_number_is_valid(value):
            raise ValueError("Ошибка: Пользователь ввёл некорректный номер телефона.")

        # Если введён корректный номер телефона
        else:
            return value
    
    # Валидация электронной почты
    @field_validator("email")
    def email_validation(cls, value: str) -> str:
        # Если введена некорректная электронная почта
        if not email_is_valid(value):
            raise ValueError("Ошибка: Пользователь ввёл некорректную электронную почту")
        
        # Если введена корректная электронная почта
        else:
            return value