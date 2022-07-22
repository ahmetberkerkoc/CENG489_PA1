
import textwrap
import json
import hashlib
import jwt
from numpy import s_
import requests 
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta, timezone
from requests.structures import CaseInsensitiveDict
import calendar

#private_key = "-----BEGIN PRIVATE KEY-----MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCS/tbfi19rs+lervP94En7EUPCNTxHvVIxaTZnMWJFr3JEnoKliJhUEfCoYczWcdU4HYPPGC7cegNLmJJIJrLOeHFGVot7/zlVlDaopNRfUHzOkQWMv4Gag4Fbk4Ij4hMpJl8vp2wf5U6yHfgZ5KMznU3WvrIyFkQv3uPlgZfuBWIm5PvdAZTokT1tc9m0ImbMFDv/W/6k+3xHOWkLcZOHTwZub4JqcodMCSH2XteQmZE4xaJVM765fUws4oKszCR0/QMzbYPgFVofEpKLmMVs6g/GdnIqOyjZh+/LF0kGkmHqklPBY/5MuLgI65FyPiOhDXeROENTIGDqOKGdC0LRAgMBAAECggEAUWsuASvlcnZ4cKVfJ+Ovloz9hviNpv7KI+wu4gGMeSSwmiliG+YI2agGMH3bQ3xRqX9Pnsm6SwyZ/qlHfQdSSuKTe248XDYFv80UaVzC9PhT6OaSuF7qnnbwk5SkpNN34XcLig2l6hTM/gNzhIQLkW8zyhpeATgsFIfUmy6oxIEDAcoQqnUhdSEfs0p3JTzous3Jdv+yKQwsnyC22BHimpUNpQTl8+rauI388rPF3KQI9OHIAu7zw8bFJlH8sqOTIMiFf19/vZGpZ6yMYs6+DLc5QV6kOFSjbc8X+LqYs7AHWTudf+nrgbAK2ZWoryzKj/kwK4PL8t0hJ1CzMdKbsQKBgQDwS3MCKdYnBKFqJ5ZUbRFNojWCVWyq3K1v+ycv4ZsgfeQwkGZTbBOUQAVEYsBITERAhCrWGhwROldklzKy3btD1bIe8rN87VlhUYokpLjzmfDL7eooYc1bmMFhI1rWd9wDqcQGvDziSnHAs1Uo+TlTpHNfmYc0aTssTM/nE7IoRwKBgQCcmlSXlYJJV+MnRwjq6wTtGkCjWDt8APYF5gdK2F0oj44m5fHclpx0lqi9GlBjM3NgC3+Y/2FtGokcRamyfrINpFD4AAkar+yyWsqqGu09wckDWud6VqeMTD0xex53BtKc0Ag5P6nARll+9BelvNLenzsOJU5xLSOMUI2/9o/gJwKBgDtqnJSDXcWmGneSNFTJ50Zn/o0srEMPb/9JfeYUBfShzGPJwNON3MWCkwrW1C7MVPAS/jiUmi4UW/mufUXHF//s/i8y2fjhA4HR1LO821K41NbIDGdRz6J/ggmP4W04k/l/5822i+N0fu4kKcGI5ojtF+4im1D1WEFa+OltcFcPAoGAcIfBo49OqM9brhywPsaUqqADtJyxWeEC6Kgrs0+YWY4WcsMnMgCT+n9MT156R15wWKLKlLFmW9UGk2dHkrjRz1W0zRCRejjSWDM/kE57DbaTcDLBRTrBeOJL0qOK97LSYtZmImUp4L1sj/psh68Qw+IduIN8Q31RHwG/aiKNrl8CgYEAzAsb/s24H3Iadr0bYAuoIF6/JHctp0oVIO3uG1wjWGt8iwogNdcC9oQ/QTuYimuuM0cABUbFTjHYmi2vfFuOKbQFBP4D4BwHqgLfxeXtP7g2YjGI0Otxz1GItAPDHya1WfQn6vxAGUleZ20sSvtxTa11HAuC4xvPIiMWIV6y0do=-----END PRIVATE KEY-----"

# public and private key
public_key = "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkv7W34tfa7PpXq7z/eBJ+xFDwjU8R71SMWk2ZzFiRa9yRJ6CpYiYVBHwqGHM1nHVOB2Dzxgu3HoDS5iSSCayznhxRlaLe/85VZQ2qKTUX1B8zpEFjL+BmoOBW5OCI+ITKSZfL6dsH+VOsh34GeSjM51N1r6yMhZEL97j5YGX7gViJuT73QGU6JE9bXPZtCJmzBQ7/1v+pPt8RzlpC3GTh08Gbm+CanKHTAkh9l7XkJmROMWiVTO+uX1MLOKCrMwkdP0DM22D4BVaHxKSi5jFbOoPxnZyKjso2YfvyxdJBpJh6pJTwWP+TLi4COuRcj4joQ13kThDUyBg6jihnQtC0QIDAQAB-----END PUBLIC KEY-----"
# format private key
private_key = textwrap.dedent("""\
    -----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCS/tbfi19rs+lervP94En7EUPCNTxHvVIxaTZnMWJFr3JEnoKliJhUEfCoYczWcdU4HYPPGC7cegNLmJJIJrLOeHFGVot7/zlVlDaopNRfUHzOkQWMv4Gag4Fbk4Ij4hMpJl8vp2wf5U6yHfgZ5KMznU3WvrIyFkQv3uPlgZfuBWIm5PvdAZTokT1tc9m0ImbMFDv/W/6k+3xHOWkLcZOHTwZub4JqcodMCSH2XteQmZE4xaJVM765fUws4oKszCR0/QMzbYPgFVofEpKLmMVs6g/GdnIqOyjZh+/LF0kGkmHqklPBY/5MuLgI65FyPiOhDXeROENTIGDqOKGdC0LRAgMBAAECggEAUWsuASvlcnZ4cKVfJ+Ovloz9hviNpv7KI+wu4gGMeSSwmiliG+YI2agGMH3bQ3xRqX9Pnsm6SwyZ/qlHfQdSSuKTe248XDYFv80UaVzC9PhT6OaSuF7qnnbwk5SkpNN34XcLig2l6hTM/gNzhIQLkW8zyhpeATgsFIfUmy6oxIEDAcoQqnUhdSEfs0p3JTzous3Jdv+yKQwsnyC22BHimpUNpQTl8+rauI388rPF3KQI9OHIAu7zw8bFJlH8sqOTIMiFf19/vZGpZ6yMYs6+DLc5QV6kOFSjbc8X+LqYs7AHWTudf+nrgbAK2ZWoryzKj/kwK4PL8t0hJ1CzMdKbsQKBgQDwS3MCKdYnBKFqJ5ZUbRFNojWCVWyq3K1v+ycv4ZsgfeQwkGZTbBOUQAVEYsBITERAhCrWGhwROldklzKy3btD1bIe8rN87VlhUYokpLjzmfDL7eooYc1bmMFhI1rWd9wDqcQGvDziSnHAs1Uo+TlTpHNfmYc0aTssTM/nE7IoRwKBgQCcmlSXlYJJV+MnRwjq6wTtGkCjWDt8APYF5gdK2F0oj44m5fHclpx0lqi9GlBjM3NgC3+Y/2FtGokcRamyfrINpFD4AAkar+yyWsqqGu09wckDWud6VqeMTD0xex53BtKc0Ag5P6nARll+9BelvNLenzsOJU5xLSOMUI2/9o/gJwKBgDtqnJSDXcWmGneSNFTJ50Zn/o0srEMPb/9JfeYUBfShzGPJwNON3MWCkwrW1C7MVPAS/jiUmi4UW/mufUXHF//s/i8y2fjhA4HR1LO821K41NbIDGdRz6J/ggmP4W04k/l/5822i+N0fu4kKcGI5ojtF+4im1D1WEFa+OltcFcPAoGAcIfBo49OqM9brhywPsaUqqADtJyxWeEC6Kgrs0+YWY4WcsMnMgCT+n9MT156R15wWKLKlLFmW9UGk2dHkrjRz1W0zRCRejjSWDM/kE57DbaTcDLBRTrBeOJL0qOK97LSYtZmImUp4L1sj/psh68Qw+IduIN8Q31RHwG/aiKNrl8CgYEAzAsb/s24H3Iadr0bYAuoIF6/JHctp0oVIO3uG1wjWGt8iwogNdcC9oQ/QTuYimuuM0cABUbFTjHYmi2vfFuOKbQFBP4D4BwHqgLfxeXtP7g2YjGI0Otxz1GItAPDHya1WfQn6vxAGUleZ20sSvtxTa11HAuC4xvPIiMWIV6y0do=
    -----END PRIVATE KEY-----
    """)


#get amount

get_r = requests.get('https://gradecoin.xyz/config')
get_json = get_r.json()
tx_traffic_reward = get_json["tx_traffic_reward"]

#pay_load
pload1 =  {"source":"14045fd01835e32d33afff34c074aff895bc8347da0d35ff60ec1413d5210af2","target":"f82ac3b61f85cf6a7f352d3fedf9a29dd686409faa1727382544234a48676c67","amount":1,"timestamp":str(datetime.now().isoformat())}
pload2 = json.dumps(pload1,separators=(',',':'))
md5_pload = hashlib.md5(pload2.encode('utf-8')).hexdigest() 


jwt_data = {"tha": md5_pload,"iat": calendar.timegm(datetime.utcnow().utctimetuple()),"exp":calendar.timegm((datetime.utcnow() + timedelta(minutes=1)).utctimetuple())}
jwt_data1 = json.dumps(jwt_data)

key = serialization.load_pem_private_key(private_key.encode(),password=None) #private key serialization
jwt_token = jwt.encode(
    payload = jwt_data,
    key = key,
    algorithm = 'RS256',  #RS256 algorithm 
) 


#get_transaction = requests.get('https://gradecoin.xyz/transaction')

new_header = CaseInsensitiveDict()
new_header["Authorization"] = "Bearer {}".format(jwt_token)

post_r = requests.post('https://gradecoin.xyz/transaction',data=pload2,headers=new_header)
print(post_r.text)
print(post_r)
result = requests.get("https://gradecoin.xyz/transaction")
print(result.text)


