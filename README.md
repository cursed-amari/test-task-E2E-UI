python -m venv .
. .\Scripts\activate
git clone https://github.com/cursed-amari/test-task-E2E-UI.git
cd .\test-task-E2E-UI\
pip install -r .\requirements.txt
pytest main.py::test_purchase_of_good
