# py-imouse

python -m build


测试发布 twine upload --repository testpypi dist/*

正式发布 twine upload dist/*

测试token pypi-AgENdGVzdC5weXBpLm9yZwIkOTBlZWM1ZmMtYTU5YS00M2FiLWE1ZmItNTBlYjRjMjU0NjRmAAIRWzEsWyJpbW91c2UteHAiXV0AAixbMixbIjlmMDdhZjk1LWFiNTQtNGM0Ni04NjBhLWEzNmRlNmE5MzI0MiJdXQAABiDNCLMijyimblvH00QL5hEBT_a5ojRRy7XcjG3UG2DZkA
正式token pypi-AgEIcHlwaS5vcmcCJGM2Njg1MjhjLWFjMTUtNDgxYi1iMjJhLTI4ZGI4ZGRjZGQwYgACKlszLCIxYjUxZDAyMC0wZDJkLTRjMTEtYjUwOS01MTVmZDNmNWVjNjIiXQAABiAgW9XSyj822WATc81dagbiGyOn4jSjsrv4J58mBCkrig
pypi-AgEIcHlwaS5vcmcCJDMyYmRmMjc4LTgxNGQtNGIyOC1iYzQxLTQ3YjNkOTZiNjE3YgACEVsxLFsiaW1vdXNlLXhwIl1dAAIsWzIsWyJlMWFmNmVhOC01Yjk0LTQ5MWItYmFmNC04ZDFiMzQ4NGE2NDAiXV0AAAYgD5gi67VfTyanlehoKGK1k4ZAa98Y57x7OfPbEk0U-3A
pip uninstall imouse_xp -y

pip install --index-url https://test.pypi.org/simple/ imouse_xp

pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple imouse_xp==0.0.3

pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple 



