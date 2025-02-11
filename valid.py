import validators

url = "https://drive.google.com/file/d/1IpCLUAXMurHcVC9SQBFrQnRc2Q9lHD7g/view?usp=sharing"
if validators.url(url):
 print("URL is valid")
else:
  print("URL is invalid")