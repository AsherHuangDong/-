from 银行自动提款机系统.admin import Admin
from 银行自动提款机系统.提款机 import ATM
import os # 数据持久性模块
import pickle
'''
分析：
类：
用户：  类名：User
       属性：姓名  身份证号  电话号码  卡
       行为：


卡:    类名：Card
       属性：卡号  密码  余额
       行为：



提款机：类名：ATM
       属性：用户字典uy
       行为：开户   查询   取款   存款   转账   改密  锁定  解锁   补卡   销户   退出


管理员: 类名：Admin
       属性：
       行为：管理员界面  系统功能界面  管理员登录

'''


def main():
    #存储所有用户的信息
    allUsers = {}
    # 界面对象
    admin = Admin()
    admin.printAdminView()

    # 管理员开机
    if(admin.adminOption()):
        return -1
    absPath = os.getcwd()
    filePath = os.path.join(absPath, "银行自动提款机系统/allUsers.txt")
    fo = open(filePath,"rb")
    allUsers = pickle.load(fo)
    # 提款机对象
    atm = ATM(allUsers)

    while (True):
        admin.printSysFunctionView()

        # 等待用户操作
        option = input("请输入您的操作：")
        if (option == '1'):
            atm.createUser()

        elif(option == '2'):
            atm.searchUserInfo()

        elif (option == '3'):
            atm.withdrawals()

        elif (option == '4'):
            atm.saveMoney()

        elif (option == '5'):
            atm.transferMoney()

        elif (option == '6'):
            atm.changePasswd()

        elif (option == '7'):
            atm.lockUser()

        elif (option == '8'):
            atm.unlockUser()

        elif (option == '9'):
            atm.newCard()

        elif (option == '0'):
            atm.cancelUser()

        elif(option == 't'):
            if(not admin.adminOption()):
                # 将当前系统中的用户信息保存在文件中
                fo = open(filePath,"wb")
                pickle.dump(atm.allUsers, fo)
                fo.close()
                return -1


if(__name__ == "__main__"):
    main()























