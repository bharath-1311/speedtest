Feature: Test Optical Fiber Network
  As a network engineer,
  I want to identify the speed and latency of the optical fiber connection,
  So that I can validate the results.

  Scenario: Basic DHCP Test
    Given Internet connectivity is there
    When I configure "IPoE"
    Then I execute SpeedTest for "IPoE"

  Scenario: Basic PPPoE Test
    Given Internet connectivity is there
    When I configure "VIPoE"
    Then I execute SpeedTest for "VIPoE"
