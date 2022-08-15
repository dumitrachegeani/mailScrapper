import main
import utils

EMAILS = 'BFWEFB 2NJNJ listafirme@GMAIL.COM U21B12 KDKDK@DND.RO ceva@trading.listafirme'
PHONES = 'BFWEFB 2NJNJ 0720061016 COM U21B12 +40720061016 ceva@trading.listafirme'

page_source = 'BFWEFB 2NJNJ 0720061016 COM  ceva@trading.com U21B12 +40720061016 ceva@trading.com'
if __name__ == '__main__':
    list = [
        utils.Phone('07233048', 'link1'),
        utils.Phone('07233048', 'link2'),
        utils.Phone('07233048', 'link3'),
        utils.Phone('07233048', 'link4'),
        utils.Phone('072330482', 'link5')
    ]

    list_emails = [
        utils.Email('GEANY@GMAIL.COM', 'link1'),
        utils.Email('GEANY@GMAIL.COM', 'link2'),
        utils.Email('GEANY@GMAIL.COM', 'link3'),
        utils.Email('GEANY@GMAIL.COM', 'link4'),
        utils.Email('GEANY@GMAIL.COM2', 'link5')
    ]
    print(utils.compress_phones(list))
    print(utils.compress_emails(list_emails))
