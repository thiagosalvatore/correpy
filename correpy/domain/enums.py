from enum import Enum


class TransactionType(Enum):
    BUY = "buy"
    SELL = "sell"


class SecurityType(Enum):
    STOCK = "AÇÃO"
    REAL_STATE_FUND = "FII"
    ETF = "ETF"
    BDR = "BDR"
    OPTION = "OPÇÃO"
    INDEX = "ÍNDICE"


class BrokerageNoteFeeType(Enum):
    SETTLEMENT_FEE = "SETTLEMENT_FEE"
    REGISTRATION_FE = "REGISTRATION_FEE"
    TERM_FEE = "TERM_FEE"
    ANA_FEE = "ANA_FEE"
    EMOLUMENTS = "EMOLUMENTS"
    OPERATIONAL_FEE = "OPERATIONAL_FEE"
    EXECUTION = "EXECUTION"
    CUSTODY_FEE = "CUSTODY_FEE"
    IRRF = "IRRF"
    TAXES = "TAXES"
    OTHERS = "OTHERS"
