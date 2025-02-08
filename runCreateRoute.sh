#!/bin/bash
curl 'http://localhost:3000/api/createRoute' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -b 'next-auth.csrf-token=618be1aba326b5721adf31e06db980c5523c2899dc399c6bd90236ffb96fd3b7%7C92dcf9c1f20249d96a8cd938d6731433f34f0b6391be7db9e149df3cce4c772f; next-auth.callback-url=http%3A%2F%2Flocalhost%3A3000%2Fauth%2Flogin; next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..Oirw3Ck-5rDoylbm.iD9O2prbcoVQHWA0TGnvC5Tm-y0BbHlpRjwx1BRRnDE8Pg41QObI6W2Kg-Bp3LzEgoR9T0Qf5Sf2julZeqhkbhidu1ORkdj_p8CJSvq1GNu13TfGnAffGUAF65l3BpeDbjaTYs1YeEmSizPBI5SAHU7D1vk_tsZLjr5hBd6H1ZLHaWw7IIGFPKnv46RmznIM5os_Ji1dt7JaXEoNV6U1JrLEyT2m5dSz4nvdN6b7c4d6D7bKjoNQbQG2Yka_osfFFl0PVaU-VEPPvg5VjqkljP3soqLaNvmL2hAhqu4iP6l6Nzl5rcW2j9K2rhRrc2crWdYKEXodL09K9UCH_I51IwW8YMEZPF7torIlDVxAw7DH.RtgnRNDmbkRq4a80DnYM7Q' \
  -H 'Origin: http://localhost:3000' \
  -H 'Referer: http://localhost:3000/createRoute' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-GPC: 1' \
  -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1' \
  --data-raw $'{"questionsList":[{"_id":"67a774e18de6194037644bb4","aiGeneratedQuestion":false,"questionText":"Are you travelling in a group?","permittedResponses":["Yes","No"],"responseType":"multipleChoice","answer":"No"},{"_id":"67a775378de6194037644bb5","aiGeneratedQuestion":false,"questionText":"What\'s your budget?","permittedResponses":["£0","£5","£10","£15","£20","£25"],"responseType":"multipleChoice","answer":"£10"},{"_id":"67a775bd8de6194037644bb6","aiGeneratedQuestion":false,"questionText":"How much time can you spare?","permittedResponses":["30 Mins","1 Hour","2 Hours","3 Hours","4 Hours","5 Hours","6 Hours"],"responseType":"multipleChoice","answer":"1 Hour"},{"_id":"67a776028de6194037644bb7","aiGeneratedQuestion":false,"questionText":"Do you want to grab food on the way?","permittedResponses":["Yes","No"],"responseType":"multipleChoice","answer":"No"},{"_id":"67a776158de6194037644bb8","aiGeneratedQuestion":false,"questionText":"What are your main interests?","permittedResponses":["History","Food","Nature","Art","Mathematics"],"responseType":"multipleChoiceMultiple","answer":["Mathematics","Food","Nature"]},{"_id":"67a7764f8de6194037644bb9","aiGeneratedQuestion":true,"responseType":"text","seed":230332408,"questionText":"Are you looking for indoor or outdoor activities?","answer":"outdoor"}]}'