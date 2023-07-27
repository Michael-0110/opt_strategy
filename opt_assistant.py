from stock_centre import *

class Opt_Assistant():
    def __init__(self):
        self.hq = Stock_Data_Centre()
        self.opt_info = pd.read_feather(f"{self.hq.data_path}/opt/contract_info_fix.fea")

        
    def get_opt_code(self, underlying_symbol, exercise_price, contract_type, exercise_ym=None, date=None):
        '''
        获取期权合约代码
        :param underlying_symbol:  标的代码
        :param exercise_price:  行权价格
        :param contract_type:  合约类型。CO-认购期权，PO-认沽期权
        :param exercise_ym:  到期年月（如:2023-08），与date参数二选一
        :param date:  指定日期，返回全部该日期可交易的标的
        :return:
        '''
        temp_info = self.opt_info.query(
            "underlying_symbol==@underlying_symbol and exercise_price==@exercise_price and contract_type==@contract_type")
        if date is not None:
            date = pd.to_datetime(date)
            temp_info = temp_info.query("list_date<=@date<=last_trade_date")
        elif exercise_ym is not None:
            temp_info = temp_info[temp_info['exercise_ym'] == exercise_ym]
        if len(temp_info) > 0:
            return temp_info.code.tolist()
        return []

    def get_gear_info(self, underlying_symbol, contract_type, exercise_ym, ascending=True, date=None):
        '''
        获取期权档位信息
        :param underlying_symbol: 标的代码
        :param contract_type:  合约类型。CO-认购期权，PO-认沽期权
        :param exercise_ym:  到期年月（如:2023-08）
        :param ascending:  是否升序
        :param date:  指定日期，返回全部该日期可交易的标的，不指定则返回全部。建议输入回测日期，否则可能会返回未上市或已退市的合约
        :return:
        '''
        temp_info = self.opt_info.query(
            "underlying_symbol==@underlying_symbol and contract_type==@contract_type and exercise_ym==@exercise_ym")
        if date is not None:
            date = pd.to_datetime(date)
            temp_info = temp_info.query("list_date<=@date<=last_trade_date")
        temp_info = temp_info[['code', 'exercise_price', 'contract_unit']].reset_index(drop=True).sort_values(['exercise_price'], ascending=ascending)
        return temp_info

    
    def get_daily_info(self, code, date):
        '''
        获取当天交易信息
        :param code: 期权代码
        :param date: 指定日期
        :return:
        '''
        daily_info = pd.read_feather(f"{self.hq.data_path}/quotation/opt/1d/{date}.fea")        
        temp_info = daily_info.query(
            "code==@code")
        return temp_info
    
    def get_contract_info(self, code):
        temp_info = self.opt_info.query(
            "code==@code")
        return temp_info
    
    def check_trading(self, underlying_symbol, date):
        temp_info = self.opt_info.query(
            "underlying_symbol==@underlying_symbol")
        if date is not None:
            date = pd.to_datetime(date)
            temp_info = temp_info.query("list_date<=@date<=last_trade_date")
        if len(temp_info) > 0:
            return True
        else: 
            return False