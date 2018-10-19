from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import random
import math, string
from django.shortcuts import HttpResponse,render

# 字体的位置，不同版本的系统会有不同
font_path = 'usr/share/fonts/opentype/stix/STIXGeneral-Bold.otf'
# font_path = '/Library/Fonts/Hanzipen.ttc'
number = 4
# 14 #生成验证码图片的高度和宽度
size = (100, 30)



def gen_text():
    source = list(string.ascii_letters)
    for index in range(0, 10):
        source.append(str(index))
    return ''.join(random.sample(source, number))  # number是生成验证码的位数


# 用来绘制干扰线
def gene_line(draw, width, height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))


def verifycode(request):
    width, height = size  # 宽和高
    image = Image.new('RGBA', (width, height), (random.randint(100, 225), random.randint(100, 255), random.randint(100, 255)))  # 创建图片

    font = ImageFont.truetype(font_path, 25)  # 验证码的字体和字体大小
    # font = ImageFont.truetype(25) #验证码的字体和字体大小
    draw = ImageDraw.Draw(image)  # 创建画笔
    # text = "我是中国人" #生成字符串
    text = gen_text()  # 生成字符串
    print(text)
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number), text, \
              font=font, fill=(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)))  # 填充字符串

    # 加入干扰线条数的上下限
    line_number = random.randint(1, 5)

    for i in range(1, line_number):
        gene_line(draw, width, height)

    del draw

    # 存入session，用于做进一步验证
    request.session['verifycode'] = text

    image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0),
                                Image.BILINEAR)  # 创建扭曲
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强

    # // 禁止图像缓存。
    # response.setHeader("Pragma", "no-cache");
    # response.setHeader("Cache-Control", "no-cache");
    # response.setDateHeader("Expires", 0);

    buf = io.BytesIO()
    image.save(buf, 'png')  # 保存验证码图片
    return HttpResponse(buf.getvalue(), 'image/png')


def home(request):
    return render(request, "myApp/home.html")


def homeyanzheng(request):
    yzm = request.POST['yzm']
    print(yzm)
    print(request.session['verifycode'])
    if yzm.upper() == request.session['verifycode'].upper():
        return HttpResponse('ok')
    else:
        return HttpResponse('no')