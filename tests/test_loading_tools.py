

from ftl_automation.tools import load_tools_by_name
from ftl_automation.context import AutomationContext
from faster_than_light import localhost


def test_ftl_tools_empty():
    tools = {}
    context = AutomationContext(localhost, ['modules'], tools, localhost)
    new_tools = load_tools_by_name([], context)
    assert new_tools == {}

def test_ftl_tools_hostname():
    tools = {}
    context = AutomationContext(localhost, ['modules'], tools, localhost)
    new_tools = load_tools_by_name(['hostname'], context)
    assert new_tools != {}
    assert new_tools.get('hostname')
    print(new_tools)
