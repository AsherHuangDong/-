from 银行自动提款机系统.card import Card
from 银行自动提款机系统.user import User
import random


class ATM(object):
    def __init__(self, allUsers):
        self.allUsers = allUsers

    def createUser(self):
        # 向用户字典中添加一对键值对(键：卡号  值：用户)
        name = input("请输入您的姓名：")
        idCard = input("请输入您的身份证号：")
        phone = input("请输入您的手机号码：")
        prestoreMoney = int(input("请输入预存款金额："))
        if(prestoreMoney < 0):
            print("预存款输入有误！！！开户失败....")
            return -1
        onePasswd = input("请设置密码：")
        # 验证密码
        if(not self.checkPasswd(onePasswd)):
            print("密码输入错误！！开户失败.....")
            return -1
        # 所有信息齐了
        cardStr = self.randomCardId()
        card = Card(cardStr, onePasswd, prestoreMoney)
        user = User(name, idCard, phone, card)
        # 存到字典
        self.allUsers[cardStr] = user
        print("开户成功！！请牢记卡号（%s）密码........"%(cardStr))

    def searchUserInfo(self):
        cardNum = input("请输入您的卡号：")
        user = self.allUsers.get(cardNum)
        # 验证是否存在该卡号
        if(not user):
            print("该卡号不存在！！查询失败......")
            return -1
        if(user.card.cardLock == True):
            print("改卡已经被锁定！！请解锁后使用")
            return -1
        # 验证密码
        if(not self.checkPasswd(user.card.cardPasswd)):
            print("密码输入错误次数达到三次！！该卡已经被锁定！！请解锁后使用.......")
            user.card.cardLock = True
            return -1
        print("账号：%s  余额%d"%(user.card.cardId, user.card.cardMoney))


    def withdrawals(self):
        cardNum = input("请输入卡号：")
        user = self.allUsers.get(cardNum)
        if(not user):
            print("账号不存在！！请尝试其他账号...")
            return -1
        if(user.card.cardLock == True):
            print("该卡号一经被锁定！！请解锁后使用..")
            return -1
        if(not self.checkPasswd(user.card.cardPasswd)):
            print("密码输入错误次数达到三次！！该卡已经被锁定！！请解锁后使用.......")
            user.card.cardLock = True
            return -1

        Money = int(input("请输入取款金额："))
        if(Money > user.card.cardMoney):
            print("余额不足！！！")
            return -1
        user.card.cardMoney = user.card.cardMoney - Money
        print("您已取款：%d   余额： %d"%(Money,user.card.cardMoney))


    def saveMoney(self):
        cardNum = input("请输入卡号：")
        user = self.allUsers.get(cardNum)
        if (not user):
            print("账号不存在！！请尝试其他账号...")
            return -1
        if (user.card.cardLock == True):
            print("该卡号一经被锁定！！请解锁后使用..")
            return -1
        if (not self.checkPasswd(user.card.cardPasswd)):
            print("密码输入错误次数达到三次！！该卡已经被锁定！！请解锁后使用.......")
            user.card.cardLock = True
            return -1
        Money = int(input("请输入您要存入的金额："))
        if(Money <= 0):
            print("存入金额输入不正确！！存款失败.....")
            return -1
        user.card.cardMoney = user.card.cardMoney + Money
        print("您已成功存入 %d    余额为：%d"% (Money,user.card.cardMoney))


    def transferMoney(self):
        cardNum = input("请输入卡号：")
        user = self.allUsers.get(cardNum)
        if (not user):
            print("账号不存在！！请尝试其他账号...")
            return -1
        if (user.card.cardLock == True):
            print("该卡号一经被锁定！！请解锁后使用..")
            return -1
        if (not self.checkPasswd(user.card.cardPasswd)):
            print("密码输入错误次数达到三次！！该卡已经被锁定！！请解锁后使用.......")
            user.card.cardLock = True
            return -1

        otherCardNum = input("请输入您要转入的账号：")
        user1 = self.allUsers.get(otherCardNum)
        if (not user1):
            print("该账户不存在！！转账失败")
            return -1
        if (user1.card.cardLock == True):
            print("该账户已经被锁定！！转账失败")
            return -1
        Money = int(input("请输入转账金额："))
        if(Money > user.card.cardMoney):
            print("账户余额不足！！转账失败.....")
            return -1
        user.card.cardMoney = user.card.cardMoney - Money
        user1.card.cardMoney = user1.card.cardMoney + Money
        print("转账成功！！")

    def changePasswd(self):
        cardNum = input("请输入卡号：")
        user = self.allUsers.get(cardNum)
        if (not user):
            print("账号不存在！！请尝试其他账号...")
            return -1
        if (user.card.cardLock == True):
            print("该卡号一经被锁定！！请解锁后使用..")
            return -1
        if (not self.checkPasswd(user.card.cardPasswd)):
            print("密码输入错误次数达到三次！！该卡已经被锁定！！请解锁后使用.......")
            user.card.cardLock = True
            return -1
        IdCard = input("请输入身份证号：")
        if(IdCard != user.idCard):
            print("身份证号输入错误！！改密失败......")
            return -1
        newPasswd = input("请输入新密码：")
        if(newPasswd.isalnum() == False or len(newPasswd) != 3):
            print("密码输入格式有误！！改密失败....")
            return -1
        if(not self.checkPasswd(newPasswd)):
            print("密码输入错误次数达到三次！！改密失败.....")
            return -1
        user.card.cardPasswd = newPasswd
        print("改密成功!!! 请牢记新密码.........")


    def lockUser(self):
        cardNum = input("请输入您的卡号：")
        user = self.allUsers.get(cardNum)
        # 验证是否存在该卡号
        if (not user):
            print("该卡号不存在！！锁定失败......")
            return -1
        if(user.card.cardLock):
            print("该卡已经被锁定!!!请解锁后再尝试.....")
            return -1
            # 验证密码
        if (not self.checkPasswd(user.card.cardPasswd)):
            print("密码输入错误！！锁定失败.......")
            return -1
        tempCard = input("请输入您的身份证号码：")
        if(tempCard != user.idCard):
            print("身份证输入错误！！！锁定失败....")
            return -1
        user.card.cardLock = True
        print("锁定成功!!")


    def unlockUser(self):
        cardNum = input("请输入您的卡号：")
        user = self.allUsers.get(cardNum)
        # 验证是否存在该卡号
        if (not user):
            print("该卡号不存在！！解锁失败......")
            return -1
        if(user.card.cardLock == False):
            print("该卡号没有被锁定！！无需解锁....")
            return -1
        if (not self.checkPasswd(user.card.cardPasswd)):
            print("密码输入错误！！解锁失败.......")
            return -1

        tempCard = input("请输入您的身份证号码：")
        if (tempCard != user.idCard):
            print("身份证输入错误！！！锁定失败....")
            return -1
        user.card.cardLock = False
        print("解锁成功！！")

    def newCard(self):
        cardNum = input("请输入原来的卡号：")
        user = self.allUsers.get(cardNum)
        if (not user):
            print("账号不存在！！请尝试其他账号...")
            return -1
        if (user.card.cardLock == True):
            print("该卡号一经被锁定！！请解锁后使用..")
            return -1
        if (not self.checkPasswd(user.card.cardPasswd)):
            print("密码输入错误次数达到三次！！该卡已经被锁定！！请解锁后使用.......")
            user.card.cardLock = True
            return -1
        IdCard = input("请输入身份证号：")
        if (IdCard != user.idCard):
            print("身份证号输入错误！！改密失败......")
            return -1
        del self.allUsers[user.card.cardId]
        cardStr = self.randomCardId()
        card = Card(cardStr, user.card.cardPasswd, user.card.cardMoney)
        user = User(user.name, user.idCard, user.phone, card)
        # 存到字典
        self.allUsers[cardStr] = user

        print("补卡成功！！请牢记卡号（%s）密码........" % (cardStr))


    def cancelUser(self):
        cardNum = input("请输入卡号：")
        user = self.allUsers.get(cardNum)
        if (not user):
            print("账号不存在！！请尝试其他账号...")
            return -1
        if (user.card.cardLock == True):
            print("该卡号一经被锁定！！请解锁后使用..")
            return -1
        if (not self.checkPasswd(user.card.cardPasswd)):
            print("密码输入错误次数达到三次！！该卡已经被锁定！！请解锁后使用.......")
            user.card.cardLock = True
            return -1
        IdCard = input("请输入身份证号：")
        if (IdCard != user.idCard):
            print("身份证号输入错误！！改密失败......")
            return -1
        del self.allUsers[user.card.cardId]
        print("注销成功！！")

    # 验证密码
    def checkPasswd(self, realPasswd):
        for i in range(3):
            tempPasswd = input("请输入密码：")
            if(tempPasswd == realPasswd):
                return True
        return False
    # 生成卡号
    def randomCardId(self):

        while (True):
            str = ""
            for i in range(6):
                ch = chr(random.randrange(ord('0'), ord('9')))
                str += ch
                # 判断是否重复
            if(not self.allUsers.get(str)):
                return str













