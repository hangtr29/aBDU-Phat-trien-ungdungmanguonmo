from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import subprocess
import tempfile
import os
import time
from typing import Optional

from ...db.session import get_db
from ...schemas.code_execution import CodeExecutionRequest, CodeExecutionResponse
from ...api.deps import get_current_active_user
from ...models.user import User

router = APIRouter()

# Mapping language to command
LANGUAGE_COMMANDS = {
    "python": {
        "command": "python",
        "extension": ".py",
        "timeout": 10
    },
    "javascript": {
        "command": "node",
        "extension": ".js",
        "timeout": 10
    },
    "cpp": {
        "command": "g++",
        "extension": ".cpp",
        "compile_timeout": 5,
        "run_timeout": 10
    },
    "java": {
        "command": "javac",
        "extension": ".java",
        "compile_timeout": 5,
        "run_timeout": 10
    }
}


def execute_python(code: str, stdin: Optional[str] = None, timeout: int = 10) -> CodeExecutionResponse:
    """Chạy code Python"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            start_time = time.time()
            result = subprocess.run(
                ["python", temp_file],
                input=stdin.encode() if stdin else None,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            execution_time = time.time() - start_time

            return CodeExecutionResponse(
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                execution_time=execution_time,
                exit_code=result.returncode
            )
        finally:
            os.unlink(temp_file)
    except subprocess.TimeoutExpired:
        return CodeExecutionResponse(
            output="",
            error=f"Code execution timeout after {timeout} seconds",
            execution_time=timeout,
            exit_code=-1
        )
    except Exception as e:
        return CodeExecutionResponse(
            output="",
            error=str(e),
            execution_time=0,
            exit_code=-1
        )


def execute_javascript(code: str, stdin: Optional[str] = None, timeout: int = 10) -> CodeExecutionResponse:
    """Chạy code JavaScript với Node.js"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            start_time = time.time()
            result = subprocess.run(
                ["node", temp_file],
                input=stdin.encode() if stdin else None,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            execution_time = time.time() - start_time

            return CodeExecutionResponse(
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                execution_time=execution_time,
                exit_code=result.returncode
            )
        finally:
            os.unlink(temp_file)
    except subprocess.TimeoutExpired:
        return CodeExecutionResponse(
            output="",
            error=f"Code execution timeout after {timeout} seconds",
            execution_time=timeout,
            exit_code=-1
        )
    except Exception as e:
        return CodeExecutionResponse(
            output="",
            error=str(e),
            execution_time=0,
            exit_code=-1
        )


def execute_cpp(code: str, stdin: Optional[str] = None, compile_timeout: int = 5, run_timeout: int = 10) -> CodeExecutionResponse:
    """Chạy code C++"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
            f.write(code)
            temp_file = f.name

        executable = temp_file.replace('.cpp', '.exe')

        try:
            # Compile
            compile_result = subprocess.run(
                ["g++", temp_file, "-o", executable],
                capture_output=True,
                text=True,
                timeout=compile_timeout
            )

            if compile_result.returncode != 0:
                return CodeExecutionResponse(
                    output="",
                    error=compile_result.stderr,
                    execution_time=0,
                    exit_code=compile_result.returncode
                )

            # Run
            start_time = time.time()
            run_result = subprocess.run(
                [executable],
                input=stdin.encode() if stdin else None,
                capture_output=True,
                text=True,
                timeout=run_timeout
            )
            execution_time = time.time() - start_time

            return CodeExecutionResponse(
                output=run_result.stdout,
                error=run_result.stderr if run_result.returncode != 0 else None,
                execution_time=execution_time,
                exit_code=run_result.returncode
            )
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            if os.path.exists(executable):
                os.unlink(executable)
    except subprocess.TimeoutExpired:
        return CodeExecutionResponse(
            output="",
            error="Code execution timeout",
            execution_time=run_timeout,
            exit_code=-1
        )
    except Exception as e:
        return CodeExecutionResponse(
            output="",
            error=str(e),
            execution_time=0,
            exit_code=-1
        )


@router.post("/execute", response_model=CodeExecutionResponse)
def execute_code(
    payload: CodeExecutionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Chạy code và trả về kết quả"""
    language = payload.language.lower()

    if language not in LANGUAGE_COMMANDS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Language '{language}' không được hỗ trợ. Các ngôn ngữ hỗ trợ: python, javascript, cpp, java"
        )

    # Giới hạn độ dài code để tránh abuse
    if len(payload.code) > 10000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code quá dài (tối đa 10000 ký tự)"
        )

    try:
        if language == "python":
            return execute_python(payload.code, payload.stdin)
        elif language == "javascript":
            return execute_javascript(payload.code, payload.stdin)
        elif language == "cpp":
            return execute_cpp(payload.code, payload.stdin)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Language '{language}' chưa được implement"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi chạy code: {str(e)}"
        )

