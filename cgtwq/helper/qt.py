# -*- coding=UTF-8 -*-
"""Helper for cgtwq with qt.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from Qt.QtWidgets import (QDialog, QLabel, QLineEdit, QMessageBox, QPushButton,
                          QVBoxLayout)
from six import text_type

import cgtwq
from wlf.qttools import application


def ask_login(parent=None):
    """Ask login with a dialog.
        parent (QWidget, optional): Defaults to None. Parent widget.

    Returns:
        cgtwq.AccountInfo: Account logged in.
    """

    with application():
        dialog = QDialog(parent)
        dialog.setWindowTitle('登录CGTeamWork')
        account_input = QLineEdit()
        account_input.setPlaceholderText('CGTeamwork账号名')
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setPlaceholderText('密码')
        ok_button = QPushButton('登录')
        ok_button.setDefault(True)
        ok_button.clicked.connect(dialog.accept)

        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel('帐号'))
        layout.addWidget(account_input)
        layout.addWidget(QLabel('密码'))
        layout.addWidget(password_input)
        layout.addWidget(ok_button)
        dialog.setLayout(layout)
        dialog.exec_()

    while True:
        if dialog.result() == QDialog.Rejected:
            raise ValueError('Rejected')
        account, password = account_input.text(), password_input.text()
        try:
            return cgtwq.login(account, password)
        except (ValueError, cgtwq.AccountNotFoundError, cgtwq.PasswordError) as ex:
            msg = text_type(ex)
            QMessageBox.critical(parent, '登录失败', msg)
            dialog.exec_()