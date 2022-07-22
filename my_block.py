import json 
from datetime import datetime
from datetime import timedelta
import hashlib
import requests
from cryptography.hazmat.primitives import serialization
import textwrap
import jwt
import calendar
from requests.structures import CaseInsensitiveDict

private_key = textwrap.dedent("""\
    -----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCS/tbfi19rs+lervP94En7EUPCNTxHvVIxaTZnMWJFr3JEnoKliJhUEfCoYczWcdU4HYPPGC7cegNLmJJIJrLOeHFGVot7/zlVlDaopNRfUHzOkQWMv4Gag4Fbk4Ij4hMpJl8vp2wf5U6yHfgZ5KMznU3WvrIyFkQv3uPlgZfuBWIm5PvdAZTokT1tc9m0ImbMFDv/W/6k+3xHOWkLcZOHTwZub4JqcodMCSH2XteQmZE4xaJVM765fUws4oKszCR0/QMzbYPgFVofEpKLmMVs6g/GdnIqOyjZh+/LF0kGkmHqklPBY/5MuLgI65FyPiOhDXeROENTIGDqOKGdC0LRAgMBAAECggEAUWsuASvlcnZ4cKVfJ+Ovloz9hviNpv7KI+wu4gGMeSSwmiliG+YI2agGMH3bQ3xRqX9Pnsm6SwyZ/qlHfQdSSuKTe248XDYFv80UaVzC9PhT6OaSuF7qnnbwk5SkpNN34XcLig2l6hTM/gNzhIQLkW8zyhpeATgsFIfUmy6oxIEDAcoQqnUhdSEfs0p3JTzous3Jdv+yKQwsnyC22BHimpUNpQTl8+rauI388rPF3KQI9OHIAu7zw8bFJlH8sqOTIMiFf19/vZGpZ6yMYs6+DLc5QV6kOFSjbc8X+LqYs7AHWTudf+nrgbAK2ZWoryzKj/kwK4PL8t0hJ1CzMdKbsQKBgQDwS3MCKdYnBKFqJ5ZUbRFNojWCVWyq3K1v+ycv4ZsgfeQwkGZTbBOUQAVEYsBITERAhCrWGhwROldklzKy3btD1bIe8rN87VlhUYokpLjzmfDL7eooYc1bmMFhI1rWd9wDqcQGvDziSnHAs1Uo+TlTpHNfmYc0aTssTM/nE7IoRwKBgQCcmlSXlYJJV+MnRwjq6wTtGkCjWDt8APYF5gdK2F0oj44m5fHclpx0lqi9GlBjM3NgC3+Y/2FtGokcRamyfrINpFD4AAkar+yyWsqqGu09wckDWud6VqeMTD0xex53BtKc0Ag5P6nARll+9BelvNLenzsOJU5xLSOMUI2/9o/gJwKBgDtqnJSDXcWmGneSNFTJ50Zn/o0srEMPb/9JfeYUBfShzGPJwNON3MWCkwrW1C7MVPAS/jiUmi4UW/mufUXHF//s/i8y2fjhA4HR1LO821K41NbIDGdRz6J/ggmP4W04k/l/5822i+N0fu4kKcGI5ojtF+4im1D1WEFa+OltcFcPAoGAcIfBo49OqM9brhywPsaUqqADtJyxWeEC6Kgrs0+YWY4WcsMnMgCT+n9MT156R15wWKLKlLFmW9UGk2dHkrjRz1W0zRCRejjSWDM/kE57DbaTcDLBRTrBeOJL0qOK97LSYtZmImUp4L1sj/psh68Qw+IduIN8Q31RHwG/aiKNrl8CgYEAzAsb/s24H3Iadr0bYAuoIF6/JHctp0oVIO3uG1wjWGt8iwogNdcC9oQ/QTuYimuuM0cABUbFTjHYmi2vfFuOKbQFBP4D4BwHqgLfxeXtP7g2YjGI0Otxz1GItAPDHya1WfQn6vxAGUleZ20sSvtxTa11HAuC4xvPIiMWIV6y0do=
    -----END PRIVATE KEY-----
    """)
transactions = requests.get("https://gradecoin.xyz/transaction")
transactions = json.loads(transactions.text)
my_id_list = []
for id in transactions:
  
    if transactions[id]["source"] == "14045fd01835e32d33afff34c074aff895bc8347da0d35ff60ec1413d5210af2":
        my_id_list.insert(0,id)
    else:
        my_id_list.append(id)
        
config_info =  requests.get('https://gradecoin.xyz/config')
config_info_json = config_info.json()
hash_zeros = config_info_json["hash_zeros"]
min_number_of_transaction = config_info_json["block_transaction_count"]

if len(my_id_list) >= min_number_of_transaction:
    nonce=0
    while(True):
        block_field = {"transaction_list":my_id_list,"nonce":nonce,"timestamp":str(datetime.now().isoformat())}
        block_field_json = json.dumps(block_field,separators=(',',':'))
        black2s_result = hashlib.blake2s(block_field_json.encode("utf-8"),digest_size=32).hexdigest()
    
        if black2s_result[:hash_zeros] == "0"*hash_zeros:
            break
        
        nonce+=1
        
        
    block_field["hash"] = black2s_result
    block_field2 = json.dumps(block_field,separators=(',',':'))

    key = serialization.load_pem_private_key(private_key.encode(),password=None) #private key serialization
    jwt_data = {"tha": black2s_result,"iat": calendar.timegm(datetime.utcnow().utctimetuple()),"exp":calendar.timegm((datetime.utcnow() + timedelta(minutes=1)).utctimetuple())}
    jwt_token = jwt.encode(
        payload = jwt_data,
        key = key,
        algorithm = 'RS256',  #RS256 algorithm 
    ) 

    new_header = CaseInsensitiveDict()
    new_header["Authorization"] = "Bearer {}".format(jwt_token)
    post_r = requests.post('https://gradecoin.xyz/block',data=block_field2,headers=new_header)
    print(post_r)
    print(post_r.text)
    

else:
    print("add {}".format( min_number_of_transaction-len(my_id_list)))