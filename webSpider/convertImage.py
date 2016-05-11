import os, base64, sys;


def convert(img):
    with open(img, 'rb') as i:
        data = i.read();
    return base64.b64encode(data);


if __name__ == "__main__":
    strImg = convert(sys.argv[1]);
    print(type(strImg));
    # 'data:image/png;base64,'
    with open("test.img", "w", encoding="utf-8") as w:
        w.write(strImg.decode("utf-8"));

