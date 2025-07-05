from machine import ADC, Pin


class Battery:
    def __init__(self):
        self.attached = False
        try:
            self.vbat_adc = ADC(Pin(35))
            self.vbat_adc.atten(ADC.ATTN_11DB)
            self.attached = True
        except Exception as exc:
            print(f"Could not load battery: {exc}")

    def get_voltage(self) -> float:
        raw = self.vbat_adc.read()
        return raw / 4095 * 3.6 * 2

    def get_voltage_str(self) -> str:
        return "{:.2f} v".format(self.get_voltage())
