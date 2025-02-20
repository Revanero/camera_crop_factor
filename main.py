import sys
from PyQt5 import QtWidgets
import camera_crop_factor
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, QTimer


class MyWindow(QtWidgets.QMainWindow, camera_crop_factor.Ui_Menu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 1 list item disabled (for preview)
        self.model = self.cb_sensors.model()
        self.model.item(0).setEnabled(False)

        # Input boundaries
        validator = QRegExpValidator(QRegExp(r"^\d*(\.\d{1,2})?$"))
        self.le_min_foc_leng_user.setValidator(validator)
        self.le_max_foc_leng_user.setValidator(validator)
        self.le_min_aper_f_val_user.setValidator(validator)
        self.le_max_aper_f_val_user.setValidator(validator)
        self.le_min_foc_leng_result.setValidator(validator)
        self.le_max_foc_leng_result.setValidator(validator)
        self.le_min_aper_f_val_result.setValidator(validator)
        self.le_max_aper_f_val_result.setValidator(validator)

        # Button function
        self.btClear.clicked.connect(self.clear_all)
        self.cb_sensors.currentIndexChanged.connect(self.update_crop_factor)

        self.crop_factor = 1  # Initialize crop factor to 1

        # Connect text changed signals to update calculations
        self.le_min_foc_leng_user.textChanged.connect(self.calculate_min_foc_len_from_user)
        self.le_max_foc_leng_user.textChanged.connect(self.calculate_max_foc_len_from_user)
        self.le_min_aper_f_val_user.textChanged.connect(self.calculate_min_aper_from_user)
        self.le_max_aper_f_val_user.textChanged.connect(self.calculate_max_aper_from_user)
        self.le_min_foc_leng_result.textChanged.connect(self.calculate_min_foc_len_from_result)
        self.le_max_foc_leng_result.textChanged.connect(self.calculate_max_foc_len_from_result)
        self.le_min_aper_f_val_result.textChanged.connect(self.calculate_min_aper_from_result)
        self.le_max_aper_f_val_result.textChanged.connect(self.calculate_max_aper_from_result)

        self.update_crop_factor()  # Initial update of crop factor and calculations


    # Clear button func
    def clear_all(self):
        self.cb_sensors.setCurrentIndex(0)
        self.le_min_foc_leng_user.clear()
        self.le_max_foc_leng_user.clear()
        self.le_min_aper_f_val_user.clear()
        self.le_max_aper_f_val_user.clear()
        self.le_min_foc_leng_result.clear()
        self.le_max_foc_leng_result.clear()
        self.le_min_aper_f_val_result.clear()
        self.le_max_aper_f_val_result.clear()
        self.crop_factor = 1
        self.update_crop_factor()

    def try_float(self, text):
        try:
            return round(float(text), 2)  # Round to 2 decimal places
        except ValueError:
            return None

    def update_crop_factor(self):
        index = self.cb_sensors.currentIndex()
        if index == 1:
            self.crop_factor = 1
        elif index == 2:
            self.crop_factor = 1.5
        elif index == 3:
            self.crop_factor = 1.6
        elif index == 4:
            self.crop_factor = 2
        else:
            self.crop_factor = 1  # Default to 1
        self.calculate_all()

    def calculate_all(self):
        self.calculate_min_foc_len_from_user()
        self.calculate_max_foc_len_from_user()
        self.calculate_min_aper_from_user()
        self.calculate_max_aper_from_user()
        self.calculate_min_foc_len_from_result()
        self.calculate_max_foc_len_from_result()
        self.calculate_min_aper_from_result()
        self.calculate_max_aper_from_result()

    def calculate_min_foc_len_from_user(self):
        min_foc_length_user = self.try_float(self.le_min_foc_leng_user.text())
        if min_foc_length_user is not None:
            result = round(min_foc_length_user * self.crop_factor, 2)
            self.le_min_foc_leng_result.setText(str(result))
        else:
            self.le_min_foc_leng_result.clear()

    def calculate_max_foc_len_from_user(self):
        max_foc_length_user = self.try_float(self.le_max_foc_leng_user.text())
        if max_foc_length_user is not None:
            result = round(max_foc_length_user * self.crop_factor, 2)
            self.le_max_foc_leng_result.setText(str(result))
        else:
            self.le_max_foc_leng_result.clear()

    def calculate_min_aper_from_user(self):
        min_aper_f_val_user = self.try_float(self.le_min_aper_f_val_user.text())
        if min_aper_f_val_user is not None:
            result = round(min_aper_f_val_user * self.crop_factor, 2)
            self.le_min_aper_f_val_result.setText(str(result))
        else:
            self.le_min_aper_f_val_result.clear()

    def calculate_max_aper_from_user(self):
        max_aper_f_val_user = self.try_float(self.le_max_aper_f_val_user.text())
        if max_aper_f_val_user is not None:
            result = round(max_aper_f_val_user * self.crop_factor, 2)
            self.le_max_aper_f_val_result.setText(str(result))
        else:
            self.le_max_aper_f_val_result.clear()

    def calculate_min_foc_len_from_result(self):
        min_foc_length_result = self.try_float(self.le_min_foc_leng_result.text())
        if min_foc_length_result is not None and self.crop_factor != 0:
            result = round(min_foc_length_result / self.crop_factor, 2)
            self.le_min_foc_leng_user.setText(str(result))
        else:
            self.le_min_foc_leng_user.clear()

    def calculate_max_foc_len_from_result(self):
        max_foc_length_result = self.try_float(self.le_max_foc_leng_result.text())
        if max_foc_length_result is not None and self.crop_factor != 0:
            result = round(max_foc_length_result / self.crop_factor, 2)
            self.le_max_foc_leng_user.setText(str(result))
        else:
            self.le_max_foc_leng_user.clear()

    def calculate_min_aper_from_result(self):
        min_aper_f_val_result = self.try_float(self.le_min_aper_f_val_result.text())
        if min_aper_f_val_result is not None and self.crop_factor != 0:
            result = round(min_aper_f_val_result / self.crop_factor, 2)
            self.le_min_aper_f_val_user.setText(str(result))
        else:
            self.le_min_aper_f_val_user.clear()

    def calculate_max_aper_from_result(self):
        max_aper_f_val_result = self.try_float(self.le_max_aper_f_val_result.text())
        if max_aper_f_val_result is not None and self.crop_factor != 0:
            result = round(max_aper_f_val_result / self.crop_factor, 2)
            self.le_max_aper_f_val_user.setText(str(result))
        else:
            self.le_max_aper_f_val_user.clear()



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()