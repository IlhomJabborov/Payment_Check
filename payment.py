import re
from datetime import datetime
from PIL import Image
import pytesseract

class Payment:
    
    def __init__(self):
        pass

    def pay(self, image: str, price: float) -> bool:
        try:
            text = pytesseract.image_to_string(Image.open(image))
            text = text.lower()

            def find_currency_amount(text: str) -> float:
                pattern = r"(\d[\d\s]*[\.,]?\d*)\s*(so'm|sum|aqcha|cym|uzs)"
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    amount = matches[0][0].replace(' ', '').replace(',', '')
                    amount = amount.split('\n')[-1]
                    return float(amount)
                else:
                    return float(0.0)

            def check_sum(total_sum: float, price: float) -> float:
                ratio = (total_sum * 100) / price
                if ratio <= 1 and total_sum * 100 >= price:
                    return price
                elif 1 < ratio <= 2 and total_sum * 50 >= price:
                    return price
                else:
                    return 0.0

            sum_us = find_currency_amount(text)
            full_pay = check_sum(sum_us, price)
        except Exception as e:
            print(f"Error processing the image: {e}")
            return False

        today_date = datetime.today().strftime('%d.%m.%Y')
        last_word = "1155"
        name_list = ['ilhom', 'ilkhom', 'jabborov']

        if today_date in text:
            date_matches = re.findall(r'\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}', text)
            for match in date_matches:
                date_from_text = datetime.strptime(match, '%d.%m.%Y %H:%M')
                current_time = datetime.now()
                time_diff = current_time - date_from_text

                if abs(time_diff.total_seconds()) <= 180:  # 180 seconds = 3 minutes
                    if last_word in text:
                        if any(name in text for name in name_list):
                            if float(sum_us) >= price or float(full_pay) == price:
                                return True

        return False
