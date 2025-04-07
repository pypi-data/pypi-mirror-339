#錯誤訊息

class ErrorType:
    #無結果
    def no_result():
        return 'No result.'
    
    #爬取失敗
    def status_error(error_code):
        return 'Requests failed: {}'.format(str(error_code))
    
    #超過限制
    def over_limit():
        return 'You can only use 5 tags.'
    
    #無此ID
    def no_limit():
        return 'No such code found.'
    
    #帳號密碼錯誤
    def wronge_data():
        return 'Your username or password are incorract.'