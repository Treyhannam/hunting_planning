import pytest
from tests.helpers.st import import_page

def test_no_feedback():
    at = import_page('overview.py').run()

    at.button[0].click().run()

    assert at.warning[0].value == "Please provide feedback before submitting."

    
def test_feedback_no_email():
    at = import_page('overview.py').run()

    at.text_input[0].set_value(None)

    at.text_input[1].set_value('Sample feedback')

    at.button[0].click().run()

    assert at.success[0].value == 'Feedback submitted, thank you!'


def test_feedback_with_email():
    at = import_page('overview.py').run()

    at.text_input[0].set_value('fakeuser@gmail.com')

    at.text_input[1].set_value('Sample feedback')

    at.button[0].click().run()

    assert at.success[0].value == 'Feedback submitted, thank you!'