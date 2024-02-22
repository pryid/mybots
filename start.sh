#!/bin/bash
python tts_checker/main.py &
python sberprimeplus/main.py &
python sitrim/main.py &
python musarskoy/main.py &
wait

