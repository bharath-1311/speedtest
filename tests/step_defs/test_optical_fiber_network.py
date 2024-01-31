from pytest_bdd import scenarios, given, when, then, parsers
from code_files.speedtest_tool_v2 import check_internet_connectivity, configure_service, speed_test


# Scenarios
scenarios('../features/test_optical_fiber_network.feature')


# Steps
@given("Internet connectivity is there")
def check_connectivity():
    return check_internet_connectivity()


@when(parsers.parse('I configure "{service}"'))
def check_configure_service(service):
    return configure_service(service)


@then(parsers.parse('I execute SpeedTest for "{service}"'))
def check_speedtest_results(service):
    return speed_test(service)
