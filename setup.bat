@echo off

echo Start building project...

IF "%VIRTUAL_ENV%"=="" (
  echo Create new virtual environment
  python -m venv venv
  call venv\Scripts\activate
) ELSE (
  echo Virtual environment already active
)

FOR /F "tokens=* USEBACKQ" %%F IN (`python -c "import sys; print(sys.prefix)"`) DO (
  SET python_prefix=%%F
)

echo Installing dependencies...

pip install -r requirements.txt

echo Build completed.