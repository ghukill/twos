"""Simple testing framework for MicroPython environment"""

from sensor import SensorValue

def test_sensor_value_creation():
    """Test SensorValue creation"""
    sv = SensorValue("Temp", 72.5, "F")
    assert sv.name == "Temp"
    assert sv.value == 72.5
    assert sv.unit == "F"
    print("✓ SensorValue creation test passed")

def test_sensor_value_str():
    """Test SensorValue __str__ method"""
    sv = SensorValue("Temp", 72.5, "F")
    expected = "Temp: 72.5 F"
    assert str(sv) == expected
    print("✓ SensorValue __str__ test passed")

def test_sensor_value_to_dict():
    """Test SensorValue to_dict method"""
    sv = SensorValue("Temp", 72.5, "F")
    expected = {"name": "Temp", "value": 72.5, "unit": "F"}
    assert sv.to_dict() == expected
    print("✓ SensorValue to_dict test passed")

def test_sensor_value_empty_unit():
    """Test SensorValue with empty unit"""
    sv = SensorValue("UVi", 5, "")
    assert str(sv) == "UVi: 5 "
    print("✓ SensorValue empty unit test passed")

# Tests will be run by pytest automatically