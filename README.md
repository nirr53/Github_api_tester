# Configure github.properties:
1. set a git username on 'git_username'
2. generate a git token as explained at https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token
3. set the token on 'git_token'

# Running:
For all options: Enter the ../Github_api_tester/tests

1. To run all tests of the suite: python3.7 -m pytest -v -s test_*.py

2. To run a specific class: python3.7 -m pytest -v -s test_create_gists.py

3. To run a specific test of a class (all tests are independent): python3.7 -m pytest -v -s test_edit_gists::test_edit_gist.py

4. To run only the CI tests: python3.7 -m pytest -m CI -v -s test_*.py
