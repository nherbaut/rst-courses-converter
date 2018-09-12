import pytest
import rst_courses_converter


def test_project_defines_author_and_version():
    assert hasattr(rst_courses_converter, '__author__')
    assert hasattr(rst_courses_converter, '__version__')
