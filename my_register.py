
import json 
from Crypto.Cipher import AES
from base64 import b64encode
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

import requests

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256


private_key = "-----BEGIN PRIVATE KEY-----MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCS/tbfi19rs+lervP94En7EUPCNTxHvVIxaTZnMWJFr3JEnoKliJhUEfCoYczWcdU4HYPPGC7cegNLmJJIJrLOeHFGVot7/zlVlDaopNRfUHzOkQWMv4Gag4Fbk4Ij4hMpJl8vp2wf5U6yHfgZ5KMznU3WvrIyFkQv3uPlgZfuBWIm5PvdAZTokT1tc9m0ImbMFDv/W/6k+3xHOWkLcZOHTwZub4JqcodMCSH2XteQmZE4xaJVM765fUws4oKszCR0/QMzbYPgFVofEpKLmMVs6g/GdnIqOyjZh+/LF0kGkmHqklPBY/5MuLgI65FyPiOhDXeROENTIGDqOKGdC0LRAgMBAAECggEAUWsuASvlcnZ4cKVfJ+Ovloz9hviNpv7KI+wu4gGMeSSwmiliG+YI2agGMH3bQ3xRqX9Pnsm6SwyZ/qlHfQdSSuKTe248XDYFv80UaVzC9PhT6OaSuF7qnnbwk5SkpNN34XcLig2l6hTM/gNzhIQLkW8zyhpeATgsFIfUmy6oxIEDAcoQqnUhdSEfs0p3JTzous3Jdv+yKQwsnyC22BHimpUNpQTl8+rauI388rPF3KQI9OHIAu7zw8bFJlH8sqOTIMiFf19/vZGpZ6yMYs6+DLc5QV6kOFSjbc8X+LqYs7AHWTudf+nrgbAK2ZWoryzKj/kwK4PL8t0hJ1CzMdKbsQKBgQDwS3MCKdYnBKFqJ5ZUbRFNojWCVWyq3K1v+ycv4ZsgfeQwkGZTbBOUQAVEYsBITERAhCrWGhwROldklzKy3btD1bIe8rN87VlhUYokpLjzmfDL7eooYc1bmMFhI1rWd9wDqcQGvDziSnHAs1Uo+TlTpHNfmYc0aTssTM/nE7IoRwKBgQCcmlSXlYJJV+MnRwjq6wTtGkCjWDt8APYF5gdK2F0oj44m5fHclpx0lqi9GlBjM3NgC3+Y/2FtGokcRamyfrINpFD4AAkar+yyWsqqGu09wckDWud6VqeMTD0xex53BtKc0Ag5P6nARll+9BelvNLenzsOJU5xLSOMUI2/9o/gJwKBgDtqnJSDXcWmGneSNFTJ50Zn/o0srEMPb/9JfeYUBfShzGPJwNON3MWCkwrW1C7MVPAS/jiUmi4UW/mufUXHF//s/i8y2fjhA4HR1LO821K41NbIDGdRz6J/ggmP4W04k/l/5822i+N0fu4kKcGI5ojtF+4im1D1WEFa+OltcFcPAoGAcIfBo49OqM9brhywPsaUqqADtJyxWeEC6Kgrs0+YWY4WcsMnMgCT+n9MT156R15wWKLKlLFmW9UGk2dHkrjRz1W0zRCRejjSWDM/kE57DbaTcDLBRTrBeOJL0qOK97LSYtZmImUp4L1sj/psh68Qw+IduIN8Q31RHwG/aiKNrl8CgYEAzAsb/s24H3Iadr0bYAuoIF6/JHctp0oVIO3uG1wjWGt8iwogNdcC9oQ/QTuYimuuM0cABUbFTjHYmi2vfFuOKbQFBP4D4BwHqgLfxeXtP7g2YjGI0Otxz1GItAPDHya1WfQn6vxAGUleZ20sSvtxTa11HAuC4xvPIiMWIV6y0do=-----END PRIVATE KEY-----"

public_key = "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkv7W34tfa7PpXq7z/eBJ+xFDwjU8R71SMWk2ZzFiRa9yRJ6CpYiYVBHwqGHM1nHVOB2Dzxgu3HoDS5iSSCayznhxRlaLe/85VZQ2qKTUX1B8zpEFjL+BmoOBW5OCI+ITKSZfL6dsH+VOsh34GeSjM51N1r6yMhZEL97j5YGX7gViJuT73QGU6JE9bXPZtCJmzBQ7/1v+pPt8RzlpC3GTh08Gbm+CanKHTAkh9l7XkJmROMWiVTO+uX1MLOKCrMwkdP0DM22D4BVaHxKSi5jFbOoPxnZyKjso2YfvyxdJBpJh6pJTwWP+TLi4COuRcj4joQ13kThDUyBg6jihnQtC0QIDAQAB-----END PUBLIC KEY-----"
server_key = "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4gGcxidLC2AbSuW0a3BjA3MKjbcTtQEzEn6pMXU9xrc1fpvuRj9rvww1TsKYP2clKdt9HqGLHLKl857J7FXOk7ZUU1tZpF9vWnEWkS+hbJzoMPLVkAwKI2VjUBOJjJ/GnGE3TzFkhOe7phMRDzVxnMFBSqY3wPPY91SErLxzpYWXoRlkqeJPN9GyWTHpjy1ROaWPLZpZr6qpfrn801Apd1usjRHIFLOVC+QKJMmNg10Q3WJu//hPWYlitL8mKCEFQQmiRFAdxHTwzEWjIOHGt+rbVwbWdSCVRB9bmGrjN95fD8u58RQsmFKhObWj31kc3Y/827bjow0PEeSA34mtKQIDAQAB-----END PUBLIC KEY-----"
student_ID ="e223232"
password = "gmNLngJZGSAHBZe"
    
#info
info = {
"student_id": student_ID,
"passwd": password,
"public_key": public_key
}
#turn str
info_from_json = json.dumps(info)
    

temporary_key = get_random_bytes(AES.block_size)
iv = get_random_bytes(AES.block_size)
    
    
cipher = AES.new(temporary_key, AES.MODE_CBC, iv) 
cipher_text = b64encode( cipher.encrypt(pad(info_from_json.encode('utf-8'),  AES.block_size,style='pkcs7')))
    
    
s=open("gradecoin.pub","rb").read()
    
cipher = RSA.importKey(s)
key_cipher = PKCS1_OAEP.new(cipher,hashAlgo=SHA256)
key_ciphertext = key_cipher.encrypt(temporary_key)
    

iv = b64encode(iv) 
    

key_ciphertext = b64encode(key_ciphertext) 
send = { "c": str(cipher_text.decode('ascii')), "iv": str(iv.decode('ascii')), "key": str(key_ciphertext.decode('ascii')) }
r = requests.post("https://gradecoin.xyz/register",json=send)
print(r.text)

    

    
    
#{"res":"Success","message":"You have authenticated to use Gradecoin with identifier 14045fd01835e32d33afff34c074aff895bc8347da0d35ff60ec1413d5210af2"}