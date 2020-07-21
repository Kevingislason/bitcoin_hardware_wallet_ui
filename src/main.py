import configparser
import sys
from os import path
from models.watch_only_wallet import WatchOnlyWallet
from persistence.wallet_file import WalletFile

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from controllers.main_controller import MainController
from models.serial_connection_state import SerialConnectionState
from models.watch_only_wallet import WatchOnlyWallet
from networking.blockchain.block_explorer_client import BlockExplorerClient
from networking.serial.serial_client import SerialClient
from persistence.config import (
    Config, NetworkClient, BalanceUnits, ChainParameters
)
from persistence.wallet_file import WalletFile
from views.initialize_wallet_view import InitializeWalletView
from views.wallet_view import WalletView


class BitcoinHardwareWalletBridge(QMainWindow):
    main_controller: MainController

    serial_connection_state: SerialConnectionState
    watch_only_wallet: WatchOnlyWallet

    initialize_wallet_view: InitializeWalletView
    wallet_view: WalletView

    def __init__(self):
        super().__init__()
        if not path.exists("config.ini"):
            Config.set_defaults()

        self.init_ui()

        # Init models
        self.watch_only_wallet = WatchOnlyWallet()
        self.serial_connection_state = SerialConnectionState()

        self.controller = MainController(
            self.watch_only_wallet, self.serial_connection_state)

        # Init views
        self.initialize_wallet_view = InitializeWalletView(
            self.serial_connection_state, self.controller)
        self.central_widget.addWidget(self.initialize_wallet_view)

        self.wallet_view = WalletView(
            self.watch_only_wallet, self.serial_connection_state, self.controller)
        self.central_widget.addWidget(self.wallet_view)

        if WalletFile.exists():
            self.change_view(WalletView.VIEW_INDEX)

    def init_ui(self):
        # Set window title
        WINDOW_TITLE = "Bitcoin Wallet"
        self.setWindowTitle(WINDOW_TITLE)
        # Set window size
        DEFAULT_LEFT = 10
        DEFAULT_TOP = 10
        DEFAULT_WIDTH = 750
        DEFAULT_HEIGHT = 500
        self.setGeometry(DEFAULT_LEFT, DEFAULT_TOP,
                         DEFAULT_WIDTH, DEFAULT_HEIGHT)
        # Create app "pages"
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.show()

    def change_view(self, new_view_index: int):
        self.central_widget.setCurrentIndex(new_view_index)

    def init_config_file(self):
        Config.set_network_client(NetworkClient.BLOCK_EXPLORER)
        Config.set_chain_parameters(ChainParameters.MAINNET)
        Config.set_balance_display_units(BalanceDisplayUnits.BTC)


def main():
    app = QApplication(sys.argv)
    ex = BitcoinHardwareWalletBridge()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
