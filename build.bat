call venv\Scripts\activate
cmake -S . -B build -G Ninja
cmake --build build
pause
