from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...db.session import get_db
from ...models.quiz import Quiz, QuizQuestion, QuizOption, QuizAttempt, QuizAnswer
from ...models.course_content import CourseContent
from ...schemas.quiz import (
    QuizCreate, QuizOut, QuizQuestionCreate, QuizOptionCreate,
    QuizAttemptCreate, QuizAttemptOut
)
from ...api.deps import get_current_active_user
from ...models.user import User

router = APIRouter()


@router.post("/lessons/{lesson_id}/quizzes", response_model=QuizOut, status_code=status.HTTP_201_CREATED)
def create_quiz(
    lesson_id: int,
    payload: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Tạo quiz cho bài học - chỉ giáo viên hoặc admin"""
    if current_user.role not in ['teacher', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên mới có thể tạo quiz"
        )

    # Kiểm tra lesson tồn tại
    lesson = db.query(CourseContent).filter(CourseContent.id == lesson_id).first()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bài học không tồn tại"
        )

    # Tạo quiz
    quiz = Quiz(
        lesson_id=lesson_id,
        tieu_de=payload.tieu_de,
        mo_ta=payload.mo_ta,
        thoi_gian_lam_bai=payload.thoi_gian_lam_bai,
        diem_toi_da=payload.diem_toi_da,
        is_required=payload.is_required
    )
    db.add(quiz)
    db.flush()

    # Tạo câu hỏi và đáp án
    for q_idx, q_data in enumerate(payload.questions):
        question = QuizQuestion(
            quiz_id=quiz.id,
            cau_hoi=q_data.cau_hoi,
            loai=q_data.loai,
            diem=q_data.diem,
            thu_tu=q_data.thu_tu or (q_idx + 1)
        )
        db.add(question)
        db.flush()

        # Tạo các đáp án
        for o_idx, o_data in enumerate(q_data.options):
            option = QuizOption(
                question_id=question.id,
                noi_dung=o_data.noi_dung,
                is_correct=o_data.is_correct,
                thu_tu=o_data.thu_tu or (o_idx + 1)
            )
            db.add(option)

    db.commit()
    db.refresh(quiz)
    return quiz


@router.get("/lessons/{lesson_id}/quizzes", response_model=List[QuizOut])
def list_quizzes(lesson_id: int, db: Session = Depends(get_db)):
    """Lấy danh sách quiz của bài học"""
    lesson = db.query(CourseContent).filter(CourseContent.id == lesson_id).first()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bài học không tồn tại"
        )

    quizzes = db.query(Quiz).filter(Quiz.lesson_id == lesson_id).all()
    return quizzes


@router.get("/quizzes/{quiz_id}", response_model=QuizOut)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết quiz"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz không tồn tại"
        )
    return quiz


@router.post("/quizzes/{quiz_id}/attempt", response_model=QuizAttemptOut, status_code=status.HTTP_201_CREATED)
def submit_quiz_attempt(
    quiz_id: int,
    payload: QuizAttemptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Nộp bài quiz và tự động chấm điểm"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz không tồn tại"
        )

    # Tạo attempt
    attempt = QuizAttempt(
        quiz_id=quiz_id,
        user_id=current_user.id,
        trang_thai="completed"
    )
    db.add(attempt)
    db.flush()

    total_score = 0.0
    total_max_score = 0.0

    # Chấm từng câu trả lời
    for answer_data in payload.answers:
        question = db.query(QuizQuestion).filter(QuizQuestion.id == answer_data.question_id).first()
        if not question or question.quiz_id != quiz_id:
            continue

        total_max_score += float(question.diem)
        is_correct = False
        score = 0.0

        if answer_data.option_id:
            # Trắc nghiệm
            option = db.query(QuizOption).filter(
                QuizOption.id == answer_data.option_id,
                QuizOption.question_id == question.id
            ).first()
            if option and option.is_correct:
                is_correct = True
                score = float(question.diem)

        # Lưu câu trả lời
        answer = QuizAnswer(
            attempt_id=attempt.id,
            question_id=question.id,
            option_id=answer_data.option_id,
            noi_dung_tu_luan=answer_data.noi_dung_tu_luan,
            is_correct=is_correct,
            diem_dat_duoc=score
        )
        db.add(answer)
        total_score += score

    # Tính điểm tổng (theo tỷ lệ diem_toi_da)
    if total_max_score > 0:
        percentage = total_score / total_max_score
        attempt.diem = float(quiz.diem_toi_da) * percentage
    else:
        attempt.diem = 0

    from datetime import datetime
    attempt.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(attempt)
    return attempt


@router.get("/quizzes/{quiz_id}/attempts", response_model=List[QuizAttemptOut])
def list_quiz_attempts(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy danh sách attempts của quiz"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz không tồn tại"
        )

    # Học viên chỉ xem được attempts của mình
    if current_user.role == 'student':
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.quiz_id == quiz_id,
            QuizAttempt.user_id == current_user.id
        ).all()
    else:
        # Giáo viên/admin xem được tất cả
        attempts = db.query(QuizAttempt).filter(QuizAttempt.quiz_id == quiz_id).all()

    return attempts

