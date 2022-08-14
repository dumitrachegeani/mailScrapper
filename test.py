import main
import utils

EMAILS = 'BFWEFB 2NJNJ listafirme@GMAIL.COM U21B12 KDKDK@DND.RO ceva@trading.listafirme'
PHONES = 'BFWEFB 2NJNJ 0720061016 COM U21B12 +40720061016 ceva@trading.listafirme'


page_source = 'BFWEFB 2NJNJ 0720061016 COM  ceva@trading.com U21B12 +40720061016 ceva@trading.com'
if __name__ == '__main__':
    # print(list(utils.extract_mails_from(EMAILS)))
    #
    # print(utils.extract_phones_from(PHONES))

    emails, phones = main.mine_from(page_source, 'ceva')
    for email in emails:
        print(email.email)
        print(email.count)

    for phone in phones:
        print(phone.phone)
        print(phone.count)