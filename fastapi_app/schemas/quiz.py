from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class QuizOptionBase(BaseModel):
    noi_dung: str
    is_correct: bool = False
    thu_tu: int = 0


class QuizOptionCreate(QuizOptionBase):
    pass


class QuizOptionOut(QuizOptionBase):
    id: int

    class Config:
        from_attributes = True


class QuizQuestionBase(BaseModel):
    cau_hoi: str
    loai: str = "multiple_choice"
    diem: Decimal = 1.0
    thu_tu: int = 0


class QuizQuestionCreate(QuizQuestionBase):
    options: List[QuizOptionCreate] = []


class QuizQuestionOut(QuizQuestionBase):
    id: int
    options: List[QuizOptionOut] = []

    class Config:
        from_attributes = True


class QuizBase(BaseModel):
    tieu_de: str
    mo_ta: Optional[str] = None
    thoi_gian_lam_bai: int = 0
    diem_toi_da: Decimal = 10.0
    is_required: bool = False


class QuizCreate(QuizBase):
    lesson_id: int
    questions: List[QuizQuestionCreate] = []


class QuizOut(QuizBase):
    id: int
    lesson_id: int
    created_at: Optional[datetime] = None
    questions: List[QuizQuestionOut] = []

    class Config:
        from_attributes = True


class QuizAnswerSubmit(BaseModel):
    question_id: int
    option_id: Optional[int] = None
    noi_dung_tu_luan: Optional[str] = None


class QuizAttemptCreate(BaseModel):
    quiz_id: int
    answers: List[QuizAnswerSubmit]


class QuizAttemptOut(BaseModel):
    id: int
    quiz_id: int
    user_id: int
    diem: Optional[Decimal] = None
    trang_thai: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

