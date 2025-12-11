from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.base import Base


class Quiz(Base):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("chi_tiet_khoa_hoc.id"), nullable=False)
    tieu_de = Column(String(200), nullable=False)
    mo_ta = Column(Text)
    thoi_gian_lam_bai = Column(Integer, default=0)  # phút, 0 = không giới hạn
    diem_toi_da = Column(Numeric(5, 2), default=10.0)
    is_required = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lesson = relationship("CourseContent", backref="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")


class QuizQuestion(Base):
    __tablename__ = "quiz_question"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quiz.id"), nullable=False)
    cau_hoi = Column(Text, nullable=False)
    loai = Column(String(20), default="multiple_choice")  # multiple_choice, true_false
    diem = Column(Numeric(5, 2), default=1.0)
    thu_tu = Column(Integer, default=0)

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("QuizOption", back_populates="question", cascade="all, delete-orphan")


class QuizOption(Base):
    __tablename__ = "quiz_option"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("quiz_question.id"), nullable=False)
    noi_dung = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    thu_tu = Column(Integer, default=0)

    question = relationship("QuizQuestion", back_populates="options")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempt"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quiz.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    diem = Column(Numeric(5, 2))
    trang_thai = Column(String(20), default="completed")  # in_progress, completed
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    quiz = relationship("Quiz", backref="attempts")
    user = relationship("User", backref="quiz_attempts")
    answers = relationship("QuizAnswer", back_populates="attempt", cascade="all, delete-orphan")


class QuizAnswer(Base):
    __tablename__ = "quiz_answer"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempt.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_question.id"), nullable=False)
    option_id = Column(Integer, ForeignKey("quiz_option.id"), nullable=True)  # NULL nếu tự luận
    noi_dung_tu_luan = Column(Text)  # Nếu là tự luận
    is_correct = Column(Boolean)
    diem_dat_duoc = Column(Numeric(5, 2), default=0)

    attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("QuizQuestion")
    option = relationship("QuizOption")

