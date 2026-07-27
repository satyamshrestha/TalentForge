import pytest
from unittest.mock import Mock, patch

from ai.services.answer_evaluator import AnswerEvaluator
from ai.services.question_generator import QuestionGenerator
from ai.services.resume_analyzer import ResumeAnalyzer


# ---------------------------------------------------------
# Resume Analyzer
# ---------------------------------------------------------

@patch("ai.services.resume_analyzer.parse_ai_response")
@patch("ai.services.resume_analyzer.get_provider")
def test_resume_analyzer_success(mock_get_provider, mock_parse):
    provider = Mock()
    provider.generate.return_value = '{"skills": ["Python"]}'

    expected_result = Mock()

    mock_get_provider.return_value = provider
    mock_parse.return_value = expected_result

    analyzer = ResumeAnalyzer()

    result = analyzer.analyze(
        "Python developer with FastAPI experience."
    )

    assert result is expected_result

    provider.generate.assert_called_once()
    mock_parse.assert_called_once()

    prompt = provider.generate.call_args.args[0]

    assert "Python developer with FastAPI experience." in prompt


@patch("ai.services.resume_analyzer.get_provider")
def test_resume_analyzer_provider_failure(mock_get_provider):
    provider = Mock()
    provider.generate.side_effect = RuntimeError(
        "Provider unavailable"
    )

    mock_get_provider.return_value = provider

    analyzer = ResumeAnalyzer()

    with pytest.raises(
        RuntimeError,
        match="Provider unavailable"
    ):
        analyzer.analyze("Python developer")


# ---------------------------------------------------------
# Question Generator
# ---------------------------------------------------------

@patch("ai.services.question_generator.parse_ai_response")
@patch("ai.services.question_generator.get_provider")
def test_question_generator_success(mock_get_provider, mock_parse):
    provider = Mock()
    provider.generate.return_value = (
        '{"questions": ["Explain FastAPI."]}'
    )

    parsed_response = Mock()
    parsed_response.questions = [
        "Explain FastAPI.",
        "Explain dependency injection."
    ]

    mock_get_provider.return_value = provider
    mock_parse.return_value = parsed_response

    generator = QuestionGenerator()

    result = generator.generate(
        "Backend developer with FastAPI experience."
    )

    assert result == [
        "Explain FastAPI.",
        "Explain dependency injection."
    ]

    provider.generate.assert_called_once()
    mock_parse.assert_called_once()

    prompt = provider.generate.call_args.args[0]

    assert "Backend developer with FastAPI experience." in prompt


@patch("ai.services.question_generator.get_provider")
def test_question_generator_provider_failure(mock_get_provider):
    provider = Mock()
    provider.generate.side_effect = RuntimeError(
        "Provider unavailable"
    )

    mock_get_provider.return_value = provider

    generator = QuestionGenerator()

    with pytest.raises(
        RuntimeError,
        match="Provider unavailable"
    ):
        generator.generate("Backend developer")


# ---------------------------------------------------------
# Answer Evaluator
# ---------------------------------------------------------

@patch("ai.services.answer_evaluator.parse_ai_response")
@patch("ai.services.answer_evaluator.get_provider")
def test_answer_evaluator_success(mock_get_provider, mock_parse):
    provider = Mock()
    provider.generate.return_value = (
        '{"feedback": "Good answer", "score": 8}'
    )

    expected_result = Mock()

    mock_get_provider.return_value = provider
    mock_parse.return_value = expected_result

    evaluator = AnswerEvaluator()

    result = evaluator.evaluate(
        "What is dependency injection?",
        "Dependency injection provides dependencies from outside."
    )

    assert result is expected_result

    provider.generate.assert_called_once()
    mock_parse.assert_called_once()

    prompt = provider.generate.call_args.args[0]

    assert "What is dependency injection?" in prompt
    assert (
        "Dependency injection provides dependencies from outside."
        in prompt
    )


@patch("ai.services.answer_evaluator.get_provider")
def test_answer_evaluator_provider_failure(mock_get_provider):
    provider = Mock()
    provider.generate.side_effect = RuntimeError(
        "Provider unavailable"
    )

    mock_get_provider.return_value = provider

    evaluator = AnswerEvaluator()

    with pytest.raises(
        RuntimeError,
        match="Provider unavailable"
    ):
        evaluator.evaluate(
            "What is FastAPI?",
            "FastAPI is a Python web framework."
        )