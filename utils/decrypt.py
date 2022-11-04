#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/10 23:20
@Project:WeiboSpider
@File:decrypt.py
@Desc:
"""
import base64

from Crypto.Cipher import AES


class AESDecrypt:
    """AES解密"""
    iv = '0123456789ABCDEF'
    key = 'jo8j9wGw%6HbxfFn'

    @classmethod
    def _pkcs7unpadding(cls, text):
        """
        处理使用PKCS7填充过的数据
        :param text: 解密后的字符串
        :return:
        """
        length = len(text)
        unpadding = ord(text[length - 1])
        return text[0:length - unpadding]

    @classmethod
    def decrypt(cls, content):
        """
        AES解密，模式cbc，去填充pkcs7
        :param content: 16进制编码的加密字符串
        :return: 返回解密后的字符串
        """
        key = bytes(cls.key, encoding='utf-8')
        iv = bytes(cls.iv, encoding='utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypt_bytes = cipher.decrypt(bytes.fromhex(content))
        result = str(decrypt_bytes, encoding='utf-8')
        result = cls._pkcs7unpadding(result)
        return result


class AESStrDecrypt(AESDecrypt):
    """字符串AES加密/解密"""
    key = '0IqEusWFpwQoJvhwviSBNx7Dq4thVUcC'  # 自定义 秘钥 256bit
    encoding = 'utf-8'

    @classmethod
    def add_16(cls, par):
        """
        这里的密钥长度必须是16、24或32，目前16位的就够用了
        :param par:
        :return:
        """
        par = par.encode(cls.encoding)
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    @classmethod
    def encrypt(cls, content):
        """
        AES加密，模式cbc
        :param content:
        :return:
        """
        key = bytes(cls.key, encoding=cls.encoding)
        iv = bytes(cls.iv, encoding=cls.encoding)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = cipher.encrypt(cls.add_16(content))
        result = base64.encodebytes(encrypt_text).decode().strip()
        return result

    @classmethod
    def decrypt(cls, content):
        """
        AES解密，模式cbc
        :param content:
        :return:
        """
        key = bytes(cls.key, encoding=cls.encoding)
        iv = bytes(cls.iv, encoding=cls.encoding)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypt_text = cipher.decrypt(base64.decodebytes(content.encode(cls.encoding)))
        result = decrypt_text.decode(cls.encoding).strip('\0')
        return result
