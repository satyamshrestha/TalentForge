import pytest
from types import SimpleNamespace
from unittest.mock import Mock

from exceptions.interview_exception import (
    InterviewAccessDeniedException,
    InterviewNotFoundException,
    ResumeTextNotFoundException,
)
from exceptions.resume_exception import (
    ResumeAccessDeniedException,
    ResumeNotFoundException,
    ResumeNotReadyException,
)
from models.interview import Interview
from services.interview_service import InterviewService


def create_service():
    return InterviewService(
        interview_repository=Mock(),
        question_repository=Mock(),
        resume_repository=Mock(),
        question_generator=Mock(),
        audit_log_service=Mock(),
    )


def create_user(user_id="user-1"):
    return SimpleNamespace(id=user_id)


def create_resume(
    resume_id="resume-1",
    user_id="user-1",
    status="COMPLETED",
    raw_text="Python developer with FastAPI experience.",
):
    return SimpleNamespace(
        id=resume_id,
        user_id=user_id,
        status=status,
        parsed_text=(
            {"raw_text": raw_text}
            if raw_text is not None
            else {}
        ),
    )


# ---------------------------------------------------------
# create_interview_from_resume
# ---------------------------------------------------------

def test_create_interview_from_resume_success():
    db = Mock()
    service = create_service()
    user = create_user()
    resume = create_resume()

    service.resume_repository.get_resume_by_id.return_value = resume

    generated_questions = [
        "Explain FastAPI.",
        "Explain dependency injection.",
    ]

    service.question_generator.generate.return_value = (
        generated_questions
    )

    interview = Interview(
        id="interview-1",
        role_target="Backend Engineer",
        status="CREATED",
        user_id=user.id,
    )

    service.interview_repository.create_interview.return_value = (
        interview
    )

    service.interview_repository.get_interview_by_id.return_value = (
        interview
    )

    result = service.create_interview_from_resume(
        db,
        resume.id,
        user,
    )

    assert result is interview

    service.question_generator.generate.assert_called_once_with(
        "Python developer with FastAPI experience."
    )

    assert (
        service.question_repository.create_question.call_count
        == len(generated_questions)
    )

    created_questions = [
        call.args[1]
        for call in (
            service.question_repository
            .create_question
            .call_args_list
        )
    ]

    assert [
        question.question_text
        for question in created_questions
    ] == generated_questions

    assert all(
        question.interview_id == interview.id
        for question in created_questions
    )

    service.audit_log_service.log_action.assert_called_once_with(
        db,
        user.id,
        "CREATE_INTERVIEW",
        "INTERVIEW",
        interview.id,
    )


def test_create_interview_from_resume_with_no_generated_questions():
    db = Mock()
    service = create_service()
    user = create_user()
    resume = create_resume()

    service.resume_repository.get_resume_by_id.return_value = resume
    service.question_generator.generate.return_value = []

    interview = Interview(
        id="interview-1",
        role_target="Backend Engineer",
        status="CREATED",
        user_id=user.id,
    )

    service.interview_repository.create_interview.return_value = (
        interview
    )

    service.interview_repository.get_interview_by_id.return_value = (
        interview
    )

    result = service.create_interview_from_resume(
        db,
        resume.id,
        user,
    )

    assert result is interview

    service.question_generator.generate.assert_called_once_with(
        resume.parsed_text["raw_text"]
    )

    service.question_repository.create_question.assert_not_called()

    service.audit_log_service.log_action.assert_called_once_with(
        db,
        user.id,
        "CREATE_INTERVIEW",
        "INTERVIEW",
        interview.id,
    )


def test_create_interview_resume_not_found():
    db = Mock()
    service = create_service()
    user = create_user()

    service.resume_repository.get_resume_by_id.return_value = None

    with pytest.raises(ResumeNotFoundException):
        service.create_interview_from_resume(
            db,
            "missing-resume",
            user,
        )

    service.question_generator.generate.assert_not_called()


def test_create_interview_resume_access_denied():
    db = Mock()
    service = create_service()

    resume = create_resume(
        user_id="different-user",
    )

    service.resume_repository.get_resume_by_id.return_value = resume

    with pytest.raises(ResumeAccessDeniedException):
        service.create_interview_from_resume(
            db,
            resume.id,
            create_user("user-1"),
        )

    service.question_generator.generate.assert_not_called()


def test_create_interview_resume_not_ready():
    db = Mock()
    service = create_service()

    resume = create_resume(
        status="PROCESSING",
    )

    service.resume_repository.get_resume_by_id.return_value = resume

    with pytest.raises(ResumeNotReadyException):
        service.create_interview_from_resume(
            db,
            resume.id,
            create_user(),
        )

    service.question_generator.generate.assert_not_called()


def test_create_interview_resume_text_not_found():
    db = Mock()
    service = create_service()

    resume = create_resume(
        raw_text=None,
    )

    service.resume_repository.get_resume_by_id.return_value = resume

    with pytest.raises(ResumeTextNotFoundException):
        service.create_interview_from_resume(
            db,
            resume.id,
            create_user(),
        )

    service.question_generator.generate.assert_not_called()


# ---------------------------------------------------------
# retake_interview
# ---------------------------------------------------------

def test_retake_interview_success():
    db = Mock()
    service = create_service()
    user = create_user()

    original_questions = [
        SimpleNamespace(
            id="question-1",
            question_text="Explain dependency injection.",
        ),
        SimpleNamespace(
            id="question-2",
            question_text="Explain FastAPI middleware.",
        ),
    ]

    original_interview = SimpleNamespace(
        id="interview-1",
        role_target="Backend Engineer",
        status="COMPLETED",
        user_id=user.id,
        questions=original_questions,
    )

    new_interview = Interview(
        id="interview-2",
        role_target="Backend Engineer",
        status="CREATED",
        user_id=user.id,
    )

    service.interview_repository.get_interview_by_id.side_effect = [
        original_interview,
        new_interview,
    ]

    service.interview_repository.create_interview.return_value = (
        new_interview
    )

    result = service.retake_interview(
        db,
        original_interview.id,
        user,
    )

    assert result is new_interview
    assert result.id != original_interview.id
    assert result.role_target == "Backend Engineer"
    assert result.status == "CREATED"

    service.interview_repository.create_interview.assert_called_once()

    assert (
        service.question_repository.create_question.call_count
        == len(original_questions)
    )

    created_questions = [
        call.args[1]
        for call in (
            service.question_repository
            .create_question
            .call_args_list
        )
    ]

    assert [
        question.question_text
        for question in created_questions
    ] == [
        question.question_text
        for question in original_questions
    ]

    assert all(
        question.interview_id == new_interview.id
        for question in created_questions
    )

    service.audit_log_service.log_action.assert_called_once_with(
        db,
        user.id,
        "RETAKE_INTERVIEW",
        "INTERVIEW",
        new_interview.id,
    )


def test_retake_interview_with_no_questions():
    db = Mock()
    service = create_service()
    user = create_user()

    original_interview = SimpleNamespace(
        id="interview-1",
        role_target="Backend Engineer",
        status="COMPLETED",
        user_id=user.id,
        questions=[],
    )

    new_interview = Interview(
        id="interview-2",
        role_target="Backend Engineer",
        status="CREATED",
        user_id=user.id,
    )

    service.interview_repository.get_interview_by_id.side_effect = [
        original_interview,
        new_interview,
    ]

    service.interview_repository.create_interview.return_value = (
        new_interview
    )

    result = service.retake_interview(
        db,
        original_interview.id,
        user,
    )

    assert result is new_interview

    service.interview_repository.create_interview.assert_called_once()

    service.question_repository.create_question.assert_not_called()

    service.audit_log_service.log_action.assert_called_once_with(
        db,
        user.id,
        "RETAKE_INTERVIEW",
        "INTERVIEW",
        new_interview.id,
    )


def test_retake_interview_not_found():
    db = Mock()
    service = create_service()
    user = create_user()

    service.interview_repository.get_interview_by_id.return_value = None

    with pytest.raises(InterviewNotFoundException):
        service.retake_interview(
            db,
            "missing-interview",
            user,
        )

    service.interview_repository.create_interview.assert_not_called()


def test_retake_interview_access_denied():
    db = Mock()
    service = create_service()

    interview = SimpleNamespace(
        id="interview-1",
        role_target="Backend Engineer",
        status="COMPLETED",
        user_id="different-user",
        questions=[],
    )

    service.interview_repository.get_interview_by_id.return_value = (
        interview
    )

    with pytest.raises(InterviewAccessDeniedException):
        service.retake_interview(
            db,
            interview.id,
            create_user("user-1"),
        )

    service.interview_repository.create_interview.assert_not_called()